from __future__ import annotations

import json
from datetime import datetime

from app.core.settings import settings

PREF_FILE = settings.memory_dir / "preferences.json"
BEHAVIOR_FILE = settings.memory_dir / "behavior_rules.json"
FEEDBACK_FILE = settings.memory_dir / "feedback_hooks.jsonl"


def _load_json(path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def get_preferences() -> dict:
    settings.memory_dir.mkdir(parents=True, exist_ok=True)
    return _load_json(PREF_FILE, {"response_style": "practical", "organization_mode": "safe"})


def set_preferences(prefs: dict) -> dict:
    current = get_preferences()
    current.update(prefs)
    PREF_FILE.write_text(json.dumps(current, indent=2, ensure_ascii=False), encoding="utf-8")
    return current


def get_behavior_rules() -> dict:
    settings.memory_dir.mkdir(parents=True, exist_ok=True)
    return _load_json(BEHAVIOR_FILE, {"auto_actions": False, "review_threshold": 0.6})


def record_feedback(event_type: str, payload: dict) -> None:
    settings.memory_dir.mkdir(parents=True, exist_ok=True)
    with FEEDBACK_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps({"at": datetime.utcnow().isoformat(), "type": event_type, "payload": payload}, ensure_ascii=False) + "\n")
