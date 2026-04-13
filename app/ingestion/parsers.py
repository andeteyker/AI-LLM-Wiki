from __future__ import annotations

from pathlib import Path
import json
import csv


def parse_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def parse_json_file(path: Path) -> str:
    return json.dumps(json.loads(path.read_text(encoding="utf-8")), indent=2, ensure_ascii=False)


def parse_csv_file(path: Path) -> str:
    rows: list[str] = []
    with path.open("r", encoding="utf-8", errors="ignore", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(" | ".join(row))
    return "\n".join(rows)


def parse_pdf_file(path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("PDF support not installed. Install with: pip install -e .[pdf]") from exc

    reader = PdfReader(str(path))
    texts = [page.extract_text() or "" for page in reader.pages]
    return "\n\n".join(texts)


def parse_file(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md", ".log", ".py", ".js", ".ts", ".yaml", ".yml"}:
        return parse_text_file(path)
    if suffix == ".json":
        return parse_json_file(path)
    if suffix == ".csv":
        return parse_csv_file(path)
    if suffix == ".pdf":
        return parse_pdf_file(path)
    return ""
