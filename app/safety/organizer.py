from __future__ import annotations

from pathlib import Path

from app.core.settings import settings
from app.safety.service import audit_log


def suggest_organization(path: Path) -> dict:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt"}:
        target = settings.knowledge_dir / "wissensthemen" / path.name
        rule = "text_to_wissensthemen"
    elif suffix in {".pdf"}:
        target = settings.knowledge_dir / "dateien" / path.name
        rule = "pdf_to_dateien"
    else:
        target = settings.knowledge_dir / "dateien" / path.name
        rule = "default_to_dateien"

    action = {
        "mode": "simulate" if settings.safe_mode else "execute",
        "rule": rule,
        "from": str(path),
        "to": str(target),
    }
    audit_log(
        action="organizer_suggestion",
        reason=rule,
        source_path=str(path),
        target_path=str(target),
        confidence=0.7,
        details={"mode": action["mode"]},
    )
    return action
