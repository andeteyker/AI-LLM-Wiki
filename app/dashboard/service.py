from __future__ import annotations

import json
from collections import Counter
from datetime import datetime

from app.core.settings import settings
from app.knowledge.storage import INDEX_FILE


def load_dashboard() -> dict:
    inbox_items = sorted(settings.inbox_dir.glob("*.json"))
    entries: list[dict] = []
    if INDEX_FILE.exists():
        entries = json.loads(INDEX_FILE.read_text(encoding="utf-8")).get("entries", [])

    type_counter = Counter()
    unresolved = 0
    people = set()
    title_counter = Counter(entry.get("title", "") for entry in entries)

    for entry in entries:
        for entry_type in entry.get("types", []):
            type_counter[entry_type] += 1
        if entry.get("status") in {"review_needed", "conflict"}:
            unresolved += 1
        for person in entry.get("related_people", []):
            people.add(person)

    duplicates = sum(1 for _, count in title_counter.items() if count > 1)
    report = f"{datetime.utcnow().date().isoformat()}: {len(entries)} Einträge, {unresolved} ungeklärt, {duplicates} Duplikatwarnungen."

    return {
        "safe_mode": settings.safe_mode,
        "inbox_count": len(inbox_items),
        "knowledge_entries": len(entries),
        "new_files": len(inbox_items),
        "open_tasks": type_counter.get("Task", 0),
        "detected_events": type_counter.get("Event", 0),
        "unresolved_links": unresolved,
        "duplicate_warnings": duplicates,
        "people_contacts": len(people),
        "entry_types": dict(type_counter),
        "daily_report": report,
        "system_hints": [
            "Review benötigte Einträge prüfen" if unresolved else "Keine offenen Review-Fälle",
            "Duplikate prüfen" if duplicates else "Keine Duplikate erkannt",
        ],
    }
