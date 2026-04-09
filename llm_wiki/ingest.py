from __future__ import annotations

import re
from pathlib import Path


from llm_wiki.config import AppConfig
from llm_wiki.models import Manifest, SourceRecord
from llm_wiki.utils import now_iso, sha256_bytes, slugify


class IngestService:
    def __init__(self, root: Path, config: AppConfig):
        self.root = root
        self.config = config
        self.raw_dir = root / "raw"
        self.state_dir = root / "state"
        self.manifest_path = self.state_dir / "manifest.json"
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.state_dir.mkdir(parents=True, exist_ok=True)

    def _load_manifest(self) -> Manifest:
        if not self.manifest_path.exists():
            return Manifest()
        return Manifest.model_validate_json(self.manifest_path.read_text())

    def _save_manifest(self, manifest: Manifest) -> None:
        self.manifest_path.write_text(manifest.model_dump_json(indent=2))

    def ingest(self, value: str) -> SourceRecord:
        if re.match(r"^https?://", value):
            return self._ingest_url(value)
        path = Path(value)
        if path.exists():
            return self._ingest_file(path)
        return self._ingest_text(value)

    def _save_source(self, original: str, source_type: str, content: str) -> SourceRecord:
        data = content.encode("utf-8", errors="ignore")
        truncated = False
        if len(data) > self.config.max_source_chars:
            content = content[: self.config.max_source_chars]
            content += "\n\n[TRUNCATED: source exceeded max_source_chars]"
            data = content.encode("utf-8")
            truncated = True
        digest = sha256_bytes(data)
        source_id = slugify(f"{source_type}-{digest[:12]}")
        raw_path = self.raw_dir / f"{source_id}.md"
        if not raw_path.exists():
            raw_path.write_text(content)

        record = SourceRecord(
            source_id=source_id,
            original=original,
            raw_path=str(raw_path.relative_to(self.root)),
            source_type=source_type,
            sha256=digest,
            truncated=truncated,
        )
        manifest = self._load_manifest()
        manifest.sources[source_id] = record
        self._save_manifest(manifest)
        return record

    def _ingest_url(self, url: str) -> SourceRecord:
        try:
            import httpx  # type: ignore
            res = httpx.get(url, timeout=20)
            res.raise_for_status()
            text = res.text
        except Exception:
            from urllib.request import urlopen
            with urlopen(url, timeout=20) as r:
                text = r.read().decode("utf-8", errors="ignore")
        normalized = f"# URL Capture\n\nSource: {url}\nCaptured: {now_iso()}\n\n{text}"
        return self._save_source(url, "url", normalized)

    def _ingest_file(self, path: Path) -> SourceRecord:
        content = path.read_text(errors="ignore")
        normalized = f"# File Capture\n\nSource: {path.resolve()}\nCaptured: {now_iso()}\n\n{content}"
        return self._save_source(str(path), "file", normalized)

    def _ingest_text(self, text: str) -> SourceRecord:
        normalized = f"# Text Capture\n\nCaptured: {now_iso()}\n\n{text}\n"
        return self._save_source("inline-text", "text", normalized)
