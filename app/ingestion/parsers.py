from __future__ import annotations

import csv
import json
from pathlib import Path
from uuid import uuid4

from app.core.schemas import RawDocument, SourceReference
from app.ingestion.framework import BaseParser, ParserRegistry


def _build_raw(title: str, content: str, source: SourceReference, detected: str, tags: list[str]) -> RawDocument:
    return RawDocument(
        id=str(uuid4()),
        title=title,
        content=content,
        source=source,
        detected_types=[detected],
        tags=tags,
    )


class TextParser(BaseParser):
    name = "text"
    supported_suffixes = {".txt", ".md", ".log", ".py", ".js", ".ts", ".yaml", ".yml"}

    def parse(self, path: Path, source: SourceReference) -> RawDocument:
        content = path.read_text(encoding="utf-8", errors="ignore")
        return _build_raw(path.stem, content, source, "text", [path.suffix.lower().lstrip(".")])


class JsonParser(BaseParser):
    name = "json"
    supported_suffixes = {".json"}

    def parse(self, path: Path, source: SourceReference) -> RawDocument:
        content = json.dumps(json.loads(path.read_text(encoding="utf-8")), indent=2, ensure_ascii=False)
        return _build_raw(path.stem, content, source, "json", ["json"])


class CsvParser(BaseParser):
    name = "csv"
    supported_suffixes = {".csv"}

    def parse(self, path: Path, source: SourceReference) -> RawDocument:
        rows: list[str] = []
        with path.open("r", encoding="utf-8", errors="ignore", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                rows.append(" | ".join(row))
        return _build_raw(path.stem, "\n".join(rows), source, "csv", ["csv"])


class PdfParser(BaseParser):
    name = "pdf"
    supported_suffixes = {".pdf"}

    def parse(self, path: Path, source: SourceReference) -> RawDocument:
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise RuntimeError("PDF support not installed. Install with: pip install -e .[pdf]") from exc

        reader = PdfReader(str(path))
        content = "\n\n".join(page.extract_text() or "" for page in reader.pages)
        return _build_raw(path.stem, content, source, "pdf", ["pdf"])


class ImageMetadataParser(BaseParser):
    name = "image_stub"
    supported_suffixes = {".png", ".jpg", ".jpeg", ".webp"}

    def parse(self, path: Path, source: SourceReference) -> RawDocument:
        stat = path.stat()
        content = f"Image file: {path.name}\nSize: {stat.st_size} bytes"
        return _build_raw(path.stem, content, source, "image", ["image"])


class ExcelMetadataParser(BaseParser):
    name = "excel_stub"
    supported_suffixes = {".xlsx", ".xls"}

    def parse(self, path: Path, source: SourceReference) -> RawDocument:
        stat = path.stat()
        content = f"Excel file: {path.name}\nSize: {stat.st_size} bytes"
        return _build_raw(path.stem, content, source, "excel", ["excel"])


class FallbackParser(BaseParser):
    name = "fallback"
    supported_suffixes = set()

    def can_parse(self, path: Path) -> bool:
        return True

    def parse(self, path: Path, source: SourceReference) -> RawDocument:
        return _build_raw(path.stem, "", source, "unknown", ["unknown"])


def build_default_registry() -> ParserRegistry:
    registry = ParserRegistry()
    registry.register(TextParser())
    registry.register(JsonParser())
    registry.register(CsvParser())
    registry.register(PdfParser())
    registry.register(ImageMetadataParser())
    registry.register(ExcelMetadataParser())
    registry.register(FallbackParser())
    return registry
