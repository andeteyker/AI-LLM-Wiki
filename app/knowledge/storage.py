from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from slugify import slugify

from app.core.schemas import KnowledgeEntry
from app.core.settings import settings
from app.safety.service import audit_log

INDEX_FILE = settings.knowledge_dir / "index.json"


def _atomic_write(path: Path, content: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


def _target_folder(entry: KnowledgeEntry) -> Path:
    if "Task" in entry.types:
        return settings.knowledge_dir / "aufgaben"
    if "Event" in entry.types:
        return settings.knowledge_dir / "termine"
    if "Person" in entry.types:
        return settings.knowledge_dir / "personen"
    if "Project" in entry.types:
        return settings.knowledge_dir / "projekte"
    if "File" in entry.types:
        return settings.knowledge_dir / "dateien"
    return settings.knowledge_dir / "wissensthemen"


def _load_index() -> dict:
    if not INDEX_FILE.exists():
        return {"entries": [], "relations": {}, "by_type": {}, "by_tag": {}, "by_person": {}, "by_project": {}}
    return json.loads(INDEX_FILE.read_text(encoding="utf-8"))


def _prepare_version(md_path: Path, json_path: Path) -> tuple[int, str | None]:
    if not md_path.exists() or not json_path.exists():
        return 1, None

    versions_dir = settings.knowledge_dir / "archiv" / "versions"
    versions_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    old_md = versions_dir / f"{md_path.stem}-{stamp}.md"
    old_json = versions_dir / f"{json_path.stem}-{stamp}.json"
    old_md.write_text(md_path.read_text(encoding="utf-8"), encoding="utf-8")
    old_json.write_text(json_path.read_text(encoding="utf-8"), encoding="utf-8")

    previous = json.loads(json_path.read_text(encoding="utf-8"))
    previous_version = previous.get("version_info", {}).get("version", 1)
    return previous_version + 1, str(old_json)


def _append_bucket(index: dict, bucket: str, key: str, entry_id: str) -> None:
    index.setdefault(bucket, {})
    index[bucket].setdefault(key, [])
    if entry_id not in index[bucket][key]:
        index[bucket][key].append(entry_id)


def _update_index(entry: KnowledgeEntry, md_path: Path, json_path: Path) -> None:
    index = _load_index()
    index["entries"] = [e for e in index["entries"] if e["id"] != entry.id]
    payload = {
        "id": entry.id,
        "title": entry.title,
        "types": entry.types,
        "tags": entry.tags,
        "summary_short": entry.summary_short,
        "source_path": entry.source_path,
        "status": entry.status,
        "created_at": entry.created_at.isoformat(),
        "markdown_path": str(md_path),
        "metadata_path": str(json_path),
        "related_people": entry.related_people,
        "related_projects": entry.related_projects,
    }
    index["entries"].append(payload)
    index["relations"][entry.id] = {
        "projects": entry.related_projects,
        "people": entry.related_people,
        "topics": entry.related_topics,
        "files": entry.related_files,
        "tasks": entry.extracted_tasks,
        "events": entry.extracted_events,
    }

    for entity_type in entry.types:
        _append_bucket(index, "by_type", entity_type, entry.id)
    for tag in entry.tags:
        _append_bucket(index, "by_tag", tag, entry.id)
    for person in entry.related_people:
        _append_bucket(index, "by_person", person, entry.id)
    for project in entry.related_projects:
        _append_bucket(index, "by_project", project, entry.id)

    _atomic_write(INDEX_FILE, json.dumps(index, indent=2, ensure_ascii=False))


def save_entry(entry: KnowledgeEntry) -> tuple[Path, Path]:
    folder = _target_folder(entry)
    folder.mkdir(parents=True, exist_ok=True)
    stem = slugify(entry.title) or entry.id
    md_path = folder / f"{stem}.md"
    json_path = folder / f"{stem}.json"

    version, previous_version_path = _prepare_version(md_path, json_path)
    entry.version_info.version = version
    entry.version_info.previous_version_path = previous_version_path

    md = f"# {entry.title}\n\n"
    md += f"**Short Summary:** {entry.summary_short}\n\n"
    md += f"**Long Summary:** {entry.summary_long}\n\n"
    md += f"**Status:** {entry.status}\n\n"
    md += f"**Types:** {', '.join(entry.types)}\n\n"
    md += f"**Tags:** {', '.join(entry.tags)}\n\n"
    md += f"**Source:** {entry.source_path}\n\n"
    md += f"**Source Type:** {entry.source_meta.file_type}\n\n"
    md += f"**Imported At:** {entry.source_meta.imported_at.isoformat()}\n\n"
    md += f"**Confidence:** {entry.confidence}\n\n"
    md += f"**Version:** {entry.version_info.version}\n\n"
    md += "## Open Questions\n\n" + ("\n".join(f"- {q}" for q in entry.open_questions) or "- None") + "\n\n"
    md += "## Next Steps\n\n" + ("\n".join(f"- {s}" for s in entry.next_steps) or "- None") + "\n\n"
    md += "## Content\n\n" + entry.content.strip() + "\n"

    _atomic_write(md_path, md)
    _atomic_write(json_path, entry.model_dump_json(indent=2))
    _update_index(entry, md_path, json_path)
    audit_log(
        action="knowledge_saved",
        reason="entry_compiled",
        source_path=entry.source_path,
        target_path=str(json_path),
        confidence=entry.confidence,
        details={"entry_id": entry.id},
    )
    return md_path, json_path
