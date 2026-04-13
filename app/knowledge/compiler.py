from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from app.core.schemas import KnowledgeEntry, SourceRef
from app.ingestion.parsers import parse_file


def compile_file_to_entry(path: Path) -> KnowledgeEntry:
    raw = parse_file(path)
    title = path.stem.replace("_", " ").replace("-", " ").strip().title() or path.name
    summary = (raw[:240].replace("\n", " ").strip() + "...") if raw else f"Imported file: {path.name}"
    entity_types = ["File", "Topic"] if raw else ["File"]

    return KnowledgeEntry(
        id=str(uuid4()),
        title=title,
        summary=summary,
        content=raw or f"Binary or unsupported file placeholder for {path.name}",
        entity_types=entity_types,
        tags=[path.suffix.lower().lstrip(".") or "unknown"],
        source=SourceRef(path=str(path)),
    )
