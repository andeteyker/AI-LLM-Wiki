from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from uuid import uuid4

from app.core.schemas import InboxItem, RawDocument, SourceReference
from app.core.settings import settings
from app.ingestion.parsers import build_default_registry
from app.safety.service import audit_log


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


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ingest_file(path: Path) -> tuple[InboxItem, RawDocument]:
    inbox_id = str(uuid4())
    target = settings.inbox_dir / f"{inbox_id}{path.suffix.lower()}"
    shutil.copy2(path, target)

    checksum = _sha256(target)
    detected = detect_type(path)
    source = SourceReference(
        source_path=str(path),
        file_type=detected,
        checksum_sha256=checksum,
    )

    inbox_item = InboxItem(
        id=inbox_id,
        path=target,
        original_path=path,
        detected_type=detected,
        checksum_sha256=checksum,
        status="analysiert",
    )

    registry = build_default_registry()
    parser = registry.resolve(target)
    if parser is None:
        raise RuntimeError("No parser found")

    try:
        raw = parser.parse(target, source)
        raw.title = path.stem
        inbox_item.status = "kompiliert"
    except Exception as exc:  # parser failures should not crash all flow
        inbox_item.status = "unsicher"
        inbox_item.error_message = str(exc)
        audit_log(
            action="ingestion_error",
            reason="parser_failed",
            source_path=str(path),
            target_path=str(target),
            confidence=0.0,
            details={"error": str(exc)},
        )
        raise

    inbox_meta = settings.inbox_dir / f"{inbox_id}.json"
    inbox_meta.write_text(inbox_item.model_dump_json(indent=2), encoding="utf-8")

    audit_log(
        action="ingestion_success",
        reason="file_imported_and_parsed",
        source_path=str(path),
        target_path=str(target),
        confidence=0.9,
        details={"parser": parser.name},
    )

    return inbox_item, raw


def import_to_inbox(path: Path) -> InboxItem:
    inbox, _ = ingest_file(path)
    return inbox
