from pathlib import Path

from app.core.bootstrap import ensure_runtime_layout
from app.core.schemas import RawDocument, SourceReference
from app.core.settings import settings
from app.ingestion.parsers import build_default_registry
from app.knowledge.compiler import compile_document
from app.knowledge.query import search_entries
from app.knowledge.storage import save_entry
from app.safety.organizer import suggest_organization
from app.safety.service import list_undo_actions, move_to_trash


def test_parser_registry_resolves_txt(tmp_path: Path) -> None:
    file = tmp_path / "a.txt"
    file.write_text("hello")
    registry = build_default_registry()
    parser = registry.resolve(file)
    assert parser is not None
    source = SourceReference(source_path=str(file), file_type="text", checksum_sha256="x")
    raw = parser.parse(file, source)
    assert raw.content == "hello"


def test_compiler_storage_search_flow(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(settings, "base_dir", tmp_path / "data")
    ensure_runtime_layout()

    raw = RawDocument(
        id="1",
        title="projekt_roadmap",
        content="TODO: Budget planen\nMeeting am Freitag",
        source=SourceReference(source_path="/tmp/projekt_roadmap.txt", file_type="text", checksum_sha256="abc"),
        detected_types=["text"],
        tags=["txt"],
    )
    entry = compile_document(raw)
    md_path, json_path = save_entry(entry)
    assert md_path.exists()
    assert json_path.exists()

    results = search_entries("Budget", project_filter=None)
    assert any("Projekt Roadmap" in item.title for item in results)


def test_safe_mode_organizer_and_undo(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(settings, "base_dir", tmp_path / "data")
    monkeypatch.setattr(settings, "safe_mode", True)
    ensure_runtime_layout()

    file = tmp_path / "note.txt"
    file.write_text("demo")
    hint = suggest_organization(file)
    assert hint["mode"] == "simulate"

    target = move_to_trash(file, "test")
    assert target.name == file.name
    assert len(list_undo_actions()) >= 1
