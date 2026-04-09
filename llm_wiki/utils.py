from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from llm_wiki import yaml_compat as yaml


WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def slugify(text: str) -> str:
    out = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return out or "untitled"


def dump_yaml_frontmatter(data: dict[str, Any]) -> str:
    return "---\n" + yaml.safe_dump(data, sort_keys=False).strip() + "\n---\n"


def parse_frontmatter(markdown: str) -> tuple[dict[str, Any], str]:
    if not markdown.startswith("---\n"):
        return {}, markdown
    end = markdown.find("\n---\n", 4)
    if end == -1:
        return {}, markdown
    fm_text = markdown[4:end]
    body = markdown[end + 5 :]
    return (yaml.safe_load(fm_text) or {}), body


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text())


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def extract_wikilinks(text: str) -> list[str]:
    return [m.group(1).strip() for m in WIKILINK_RE.finditer(text)]
