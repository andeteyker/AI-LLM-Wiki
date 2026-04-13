from __future__ import annotations

import json
from pathlib import Path
from slugify import slugify

from app.core.schemas import KnowledgeEntry
from app.core.settings import settings


def _target_folder(entry: KnowledgeEntry) -> Path:
    if "Task" in entry.entity_types:
        return settings.knowledge_dir / "aufgaben"
    if "Event" in entry.entity_types:
        return settings.knowledge_dir / "termine"
    if "Person" in entry.entity_types:
        return settings.knowledge_dir / "personen"
    if "Project" in entry.entity_types:
        return settings.knowledge_dir / "projekte"
    if "File" in entry.entity_types:
        return settings.knowledge_dir / "dateien"
    return settings.knowledge_dir / "wissensthemen"


def save_entry(entry: KnowledgeEntry) -> tuple[Path, Path]:
    folder = _target_folder(entry)
    folder.mkdir(parents=True, exist_ok=True)
    stem = slugify(entry.title) or entry.id
    md_path = folder / f"{stem}.md"
    json_path = folder / f"{stem}.json"

    md = f"# {entry.title}\n\n"
    md += f"**Summary:** {entry.summary}\n\n"
    md += f"**Types:** {', '.join(entry.entity_types)}\n\n"
    md += f"**Tags:** {', '.join(entry.tags)}\n\n"
    md += f"**Source:** {entry.source.path}\n\n"
    md += "## Content\n\n"
    md += entry.content.strip() + "\n"

    md_path.write_text(md, encoding="utf-8")
    json_path.write_text(entry.model_dump_json(indent=2), encoding="utf-8")
    return md_path, json_path
