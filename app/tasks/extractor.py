from __future__ import annotations

from app.core.schemas import KnowledgeEntry


def extract_candidates(entry: KnowledgeEntry) -> dict:
    return {
        "possible_tasks": entry.extracted_tasks,
        "possible_events": entry.extracted_events,
    }
