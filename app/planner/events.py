from __future__ import annotations

import json
import re
from pathlib import Path
from uuid import uuid4

from app.core.schemas import EventEntity, KnowledgeEntry
from app.core.settings import settings

EVENTS_FILE = settings.knowledge_dir / "termine" / "events.json"


class EventExtractionEngine:
    def extract(self, entry: KnowledgeEntry) -> list[EventEntity]:
        events: list[EventEntity] = []
        for text in entry.extracted_events:
            when_hint = self._extract_when(text)
            status = "uncertain" if when_hint is None else "detected"
            events.append(
                EventEntity(
                    text=text,
                    when_hint=when_hint,
                    confidence=entry.confidence if when_hint else min(entry.confidence, 0.45),
                    status=status,
                    source_entry_id=entry.id,
                    source_path=entry.source_path,
                )
            )
        return events

    def _extract_when(self, text: str) -> str | None:
        match = re.search(r"\b(\d{4}-\d{2}-\d{2}|morgen|heute|montag|dienstag|mittwoch|donnerstag|freitag)\b", text.lower())
        return match.group(0) if match else None


def _load_events() -> list[dict]:
    if not EVENTS_FILE.exists():
        return []
    return json.loads(EVENTS_FILE.read_text(encoding="utf-8"))


def save_events(events: list[EventEntity]) -> None:
    current = _load_events()
    for event in events:
        payload = event.model_dump()
        payload["id"] = str(uuid4())
        current.append(payload)
    EVENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    EVENTS_FILE.write_text(json.dumps(current, indent=2, ensure_ascii=False), encoding="utf-8")


def list_events(status: str | None = None) -> list[dict]:
    events = _load_events()
    if status:
        events = [event for event in events if event.get("status") == status]
    return events
