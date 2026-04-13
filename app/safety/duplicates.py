from __future__ import annotations

import json
from collections import defaultdict

from app.core.settings import settings


def detect_duplicates() -> list[dict]:
    inbox_items = []
    for meta in settings.inbox_dir.glob("*.json"):
        try:
            inbox_items.append(json.loads(meta.read_text(encoding="utf-8")))
        except Exception:
            continue

    by_hash: dict[str, list[dict]] = defaultdict(list)
    for item in inbox_items:
        checksum = item.get("checksum_sha256")
        if checksum:
            by_hash[checksum].append(item)

    duplicates: list[dict] = []
    for checksum, items in by_hash.items():
        if len(items) > 1:
            duplicates.append({"checksum": checksum, "items": items, "action": "review_only"})
    return duplicates
