from __future__ import annotations

from app.core.schemas import KnowledgeEntry


def extract_candidates(entry: KnowledgeEntry) -> dict:
    text = entry.content.lower()
    return {
        "possible_tasks": ["Review extracted content"] if "todo" in text or "task" in text else [],
        "possible_events": ["Potential event mentioned"] if "meeting" in text or "termin" in text else [],
    }
