from __future__ import annotations

import json
from datetime import datetime

from app.core.schemas import ChatAnswer, SearchResult
from app.knowledge.storage import INDEX_FILE


def _load_entries() -> list[dict]:
    if not INDEX_FILE.exists():
        return []
    payload = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    return payload.get("entries", [])


def _within_date(entry: dict, date_from: str | None, date_to: str | None) -> bool:
    if not date_from and not date_to:
        return True
    created = entry.get("created_at")
    if not created:
        return True
    d = datetime.fromisoformat(created).date()
    if date_from and d < datetime.fromisoformat(date_from).date():
        return False
    if date_to and d > datetime.fromisoformat(date_to).date():
        return False
    return True


def search_entries(
    query: str,
    limit: int = 10,
    type_filter: str | None = None,
    project_filter: str | None = None,
    person_filter: str | None = None,
    source_filter: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
) -> list[SearchResult]:
    terms = [term.lower() for term in query.split() if term.strip()]
    scored: list[SearchResult] = []
    for entry in _load_entries():
        if type_filter and type_filter not in entry.get("types", []):
            continue
        if project_filter and project_filter not in entry.get("related_projects", []):
            continue
        if person_filter and person_filter not in entry.get("related_people", []):
            continue
        if source_filter and source_filter not in entry.get("source_path", ""):
            continue
        if not _within_date(entry, date_from, date_to):
            continue

        haystack = " ".join(
            [
                entry.get("title", ""),
                entry.get("summary_short", ""),
                " ".join(entry.get("tags", [])),
                " ".join(entry.get("types", [])),
                " ".join(entry.get("related_people", [])),
                " ".join(entry.get("related_projects", [])),
            ]
        ).lower()
        score = sum(2 for term in terms if term in haystack)
        if query and score == 0:
            continue
        scored.append(
            SearchResult(
                entry_id=entry["id"],
                title=entry["title"],
                summary_short=entry.get("summary_short", ""),
                score=score,
                source_path=entry.get("source_path", ""),
                status=entry.get("status", "new"),
            )
        )

    return sorted(scored, key=lambda item: item.score, reverse=True)[:limit]


def answer_question(question: str) -> ChatAnswer:
    hits = search_entries(question, limit=5)
    if not hits:
        return ChatAnswer(
            answer="Ich habe dazu noch kein passendes Wissen gefunden.",
            next_steps=["Dateien importieren", "Frage präzisieren"],
            uncertainty="Kein Treffer im Knowledge Index.",
        )

    bullets = [f"- {hit.title}: {hit.summary_short}" for hit in hits[:3]]
    return ChatAnswer(
        answer="Relevante Wissenseinträge:\n" + "\n".join(bullets),
        sources=[hit.source_path for hit in hits[:3]],
        related_entries=[hit.entry_id for hit in hits[:3]],
        related_files=[hit.source_path for hit in hits[:3]],
        next_steps=["Verlinkte Einträge prüfen", "Aufgaben in Planner übernehmen"],
        uncertainty=None if all(hit.status == "confirmed" for hit in hits[:3]) else "Einige Treffer sind noch unbestätigt.",
    )
