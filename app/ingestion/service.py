from __future__ import annotations

from pathlib import Path
from app.core.schemas import InboxItem


def detect_type(path: Path) -> str:
    suffix = path.suffix.lower()
    mapping = {
        ".pdf": "pdf",
        ".txt": "text",
        ".md": "markdown",
        ".json": "json",
        ".csv": "csv",
        ".png": "image",
        ".jpg": "image",
        ".jpeg": "image",
        ".webp": "image",
        ".xlsx": "excel",
        ".xls": "excel",
    }
    return mapping.get(suffix, "unknown")


def create_inbox_item(path: Path) -> InboxItem:
    return InboxItem(path=path, detected_type=detect_type(path))
