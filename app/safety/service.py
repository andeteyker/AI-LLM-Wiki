from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path

from app.core.settings import settings

AUDIT_LOG_FILE = settings.logs_dir / "audit.jsonl"
ERROR_LOG_FILE = settings.logs_dir / "errors.jsonl"
UNDO_FILE = settings.logs_dir / "undo_stack.json"


def _write_jsonl(path: Path, payload: dict) -> None:
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _load_undo() -> list[dict]:
    if not UNDO_FILE.exists():
        return []
    return json.loads(UNDO_FILE.read_text(encoding="utf-8"))


def push_undo(action: dict) -> None:
    stack = _load_undo()
    stack.append({"at": datetime.utcnow().isoformat(), **action})
    UNDO_FILE.write_text(json.dumps(stack, indent=2, ensure_ascii=False), encoding="utf-8")


def list_undo_actions() -> list[dict]:
    return _load_undo()[-50:]


def audit_log(
    action: str,
    reason: str,
    source_path: str,
    target_path: str | None,
    confidence: float,
    details: dict | None = None,
) -> None:
    _write_jsonl(
        AUDIT_LOG_FILE,
        {
            "when": datetime.utcnow().isoformat(),
            "what": action,
            "why": reason,
            "from": source_path,
            "to": target_path,
            "confidence": confidence,
            "details": details or {},
        },
    )


def error_log(scope: str, message: str, details: dict | None = None) -> None:
    _write_jsonl(
        ERROR_LOG_FILE,
        {
            "when": datetime.utcnow().isoformat(),
            "scope": scope,
            "message": message,
            "details": details or {},
        },
    )


def move_to_trash(path: Path, reason: str) -> Path:
    target = settings.trash_dir / path.name
    if not settings.safe_mode:
        shutil.move(str(path), str(target))
    push_undo({"action": "move_to_trash", "from": str(path), "to": str(target), "reason": reason})
    audit_log(
        action="move_to_trash",
        reason=reason,
        source_path=str(path),
        target_path=str(target),
        confidence=1.0,
        details={"safe_mode": settings.safe_mode},
    )
    return target
