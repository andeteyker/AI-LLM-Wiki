from pathlib import Path

from llm_wiki.query import QueryEngine


def test_query_save_flow(tmp_path: Path):
    wiki = tmp_path / "wiki"
    (wiki / "concepts").mkdir(parents=True)
    (wiki / "queries").mkdir(parents=True)
    (wiki / "index.md").write_text("# Wiki Index\n")
    (wiki / "concepts" / "atlas.md").write_text(
        "---\n"
        "title: Atlas\n"
        "type: concept\n"
        "summary: Atlas summary\n"
        "created_at: 2026-01-01T00:00:00+00:00\n"
        "updated_at: 2026-01-01T00:00:00+00:00\n"
        "source_refs: [example]\n"
        "related: []\n"
        "confidence: 0.8\n"
        "freshness: fresh\n"
        "status: active\n"
        "---\n"
        "Atlas is local first."
    )
    result = QueryEngine(tmp_path).query("What is Atlas?", save=True)
    assert result.wiki_refs
    saved = list((wiki / "queries").glob("*.md"))
    assert len(saved) == 1
    assert saved[0].read_text().find("What is Atlas?") != -1
