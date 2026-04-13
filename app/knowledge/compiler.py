from __future__ import annotations

import re
from uuid import uuid4

from app.core.schemas import KnowledgeEntry, RawDocument, Relation

TASK_PATTERNS = [r"\btodo\b", r"\btask\b", r"\baction item\b", r"\baufgabe\b"]
EVENT_PATTERNS = [r"\bmeeting\b", r"\btermin\b", r"\bdeadline\b", r"\bworkshop\b"]


def _extract_people(text: str) -> list[str]:
    return sorted(set(re.findall(r"\b[A-Z][a-z]+\s[A-Z][a-z]+\b", text)))[:10]


def _extract_projects(text: str) -> list[str]:
    projects = []
    for line in text.splitlines():
        if "project" in line.lower() or "projekt" in line.lower():
            projects.append(line[:80])
    return projects[:5]


def _extract_topics(title: str, text: str) -> list[str]:
    words = re.findall(r"[A-Za-zÄÖÜäöüß]{5,}", text)
    return [title.lower(), *sorted(set(w.lower() for w in words))[:8]]


def _extract_tasks(text: str) -> list[str]:
    lines = [line.strip("-• ") for line in text.splitlines() if line.strip()]
    return [line for line in lines if any(re.search(pattern, line.lower()) for pattern in TASK_PATTERNS)][:10]


def _extract_events(text: str) -> list[str]:
    lines = [line.strip("-• ") for line in text.splitlines() if line.strip()]
    return [line for line in lines if any(re.search(pattern, line.lower()) for pattern in EVENT_PATTERNS)][:10]


def compile_document(raw: RawDocument) -> KnowledgeEntry:
    cleaned = raw.content.strip()
    summary_short = (cleaned[:180].replace("\n", " ").strip() + "...") if cleaned else f"Imported file: {raw.title}"
    summary_long = (cleaned[:800] + "...") if len(cleaned) > 800 else cleaned or "No text extracted."

    tasks = _extract_tasks(cleaned)
    events = _extract_events(cleaned)
    people = _extract_people(cleaned)
    projects = _extract_projects(cleaned)
    topics = _extract_topics(raw.title, cleaned)

    types = ["File", "Note"]
    if tasks:
        types.append("Task")
    if events:
        types.append("Event")
    if projects:
        types.append("Project")

    confidence = 0.8 if cleaned else 0.4
    status = "review_needed" if confidence < 0.5 else "confirmed"

    relations = [Relation(relation_type="person", target_id=name, confidence=0.7) for name in people]
    relations += [Relation(relation_type="project", target_id=name, confidence=0.6) for name in projects]

    return KnowledgeEntry(
        id=str(uuid4()),
        title=raw.title.replace("_", " ").replace("-", " ").title(),
        summary_short=summary_short,
        summary_long=summary_long,
        content=cleaned or "No content extracted",
        types=sorted(set(types)),
        tags=sorted(set(raw.tags + raw.detected_types)),
        source_path=raw.source.source_path,
        confidence=confidence,
        related_projects=projects,
        related_people=people,
        related_files=[raw.source.source_path],
        related_topics=topics,
        extracted_tasks=tasks,
        extracted_events=events,
        relations=relations,
        open_questions=["Bitte Zuordnung prüfen"] if status == "review_needed" else [],
        next_steps=["Eintrag freigeben", "Aufgaben prüfen"] if tasks else ["Tags prüfen"],
        status=status,
        source_meta=raw.source,
    )


def compile_file_to_entry(path, original_path=None, file_type: str = "unknown"):
    # backward compatible shim for older imports
    from app.ingestion.service import ingest_file

    _, raw = ingest_file(original_path or path)
    return compile_document(raw)
