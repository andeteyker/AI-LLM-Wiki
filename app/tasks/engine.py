from __future__ import annotations

import json
import re
from pathlib import Path
from uuid import uuid4

from app.core.schemas import KnowledgeEntry, TaskEntity
from app.core.settings import settings

TASK_FILE = settings.knowledge_dir / "aufgaben" / "tasks.json"


class TaskExtractionEngine:
    PRIORITY_PATTERNS = {
        "high": [r"\burgent\b", r"\bsofort\b", r"\basap\b"],
        "medium": [r"\btodo\b", r"\btask\b", r"\baufgabe\b"],
        "low": [r"\boptional\b", r"\blater\b"],
    }

    def extract(self, entry: KnowledgeEntry) -> list[TaskEntity]:
        tasks: list[TaskEntity] = []
        for text in entry.extracted_tasks:
            lower = text.lower()
            priority = "medium"
            for level, patterns in self.PRIORITY_PATTERNS.items():
                if any(re.search(pattern, lower) for pattern in patterns):
                    priority = level
                    break
            due_hint = self._extract_due_hint(text)
            tasks.append(
                TaskEntity(
                    text=text,
                    due_hint=due_hint,
                    confidence=entry.confidence,
                    priority=priority,
                    status="open",
                    source_entry_id=entry.id,
                    source_path=entry.source_path,
                )
            )
        return tasks

    def _extract_due_hint(self, text: str) -> str | None:
        match = re.search(r"\b(\d{4}-\d{2}-\d{2}|morgen|heute|freitag|montag)\b", text.lower())
        return match.group(0) if match else None


def _load_tasks() -> list[dict]:
    if not TASK_FILE.exists():
        return []
    return json.loads(TASK_FILE.read_text(encoding="utf-8"))


def save_tasks(tasks: list[TaskEntity]) -> None:
    current = _load_tasks()
    for task in tasks:
        task_id = getattr(task, "id", None) or str(uuid4())
        payload = task.model_dump()
        payload["id"] = task_id
        current.append(payload)
    TASK_FILE.parent.mkdir(parents=True, exist_ok=True)
    TASK_FILE.write_text(json.dumps(current, indent=2, ensure_ascii=False), encoding="utf-8")


def list_tasks(status: str | None = None, priority: str | None = None) -> list[dict]:
    tasks = _load_tasks()
    if status:
        tasks = [task for task in tasks if task.get("status") == status]
    if priority:
        tasks = [task for task in tasks if task.get("priority") == priority]
    return tasks
