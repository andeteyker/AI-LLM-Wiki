from pathlib import Path

from llm_wiki.linting import LintEngine


def test_lint_detects_broken_wikilinks(tmp_path: Path):
    wiki = tmp_path / "wiki"
    wiki.mkdir(parents=True)
    (wiki / "index.md").write_text("# Index")
    (wiki / "a.md").write_text("---\ntitle: A\n---\nSee [[missing]].")
    issues = LintEngine(tmp_path).lint()
    assert "broken_wikilinks" in issues
    assert issues["broken_wikilinks"]
