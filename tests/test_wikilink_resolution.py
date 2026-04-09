from llm_wiki.utils import extract_wikilinks


def test_extract_wikilinks():
    text = "See [[alpha]] and [[beta concept]]."
    links = extract_wikilinks(text)
    assert links == ["alpha", "beta concept"]
