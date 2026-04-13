from __future__ import annotations

from pathlib import Path

from app.ingestion.service import create_inbox_item
from app.knowledge.compiler import compile_file_to_entry
from app.knowledge.storage import save_entry
from app.tasks.extractor import extract_candidates


class ManagerAgent:
    def ingest_path(self, path: Path) -> dict:
        inbox_item = create_inbox_item(path)
        entry = compile_file_to_entry(path)
        md_path, json_path = save_entry(entry)
        task_hints = extract_candidates(entry)
        return {
            "inbox_item": inbox_item.model_dump(mode="json"),
            "entry_id": entry.id,
            "markdown_path": str(md_path),
            "metadata_path": str(json_path),
            "task_hints": task_hints,
        }
