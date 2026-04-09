from pathlib import Path

from llm_wiki.compile import Compiler


def test_incremental_compile_only_changed_sources(tmp_path: Path):
    (tmp_path / "raw").mkdir(parents=True)
    (tmp_path / "wiki").mkdir(parents=True)
    (tmp_path / "state").mkdir(parents=True)
    (tmp_path / "raw" / "a.md").write_text("# Alpha\nAlpha concept.")

    c = Compiler(tmp_path)
    first = c.compile()
    assert first["changed_sources"] == 1

    second = c.compile()
    assert second["changed_sources"] == 0

    (tmp_path / "raw" / "a.md").write_text("# Alpha\nAlpha concept changed.")
    third = c.compile()
    assert third["changed_sources"] == 1
