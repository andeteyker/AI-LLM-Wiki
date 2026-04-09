from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from llm_wiki.utils import extract_wikilinks, parse_frontmatter


class LintEngine:
    def __init__(self, root: Path):
        self.root = root
        self.wiki = root / "wiki"

    def lint(self) -> dict[str, list[str]]:
        pages = [p for p in self.wiki.rglob("*.md") if p.is_file()]
        names = {p.stem: p for p in pages}
        issues: dict[str, list[str]] = defaultdict(list)
        inbound = defaultdict(int)

        for page in pages:
            text = page.read_text(errors="ignore")
            fm, body = parse_frontmatter(text)
            if len(body.strip()) == 0:
                issues["empty_pages"].append(str(page.relative_to(self.root)))
            for link in extract_wikilinks(body):
                if link not in names:
                    issues["broken_wikilinks"].append(f"{page.stem} -> {link}")
                else:
                    inbound[link] += 1
            if fm.get("freshness") == "stale":
                issues["stale_pages"].append(str(page.relative_to(self.root)))

        for page in pages:
            if page.stem not in inbound and page.name not in {"index.md", "log.md"}:
                issues["orphan_pages"].append(str(page.relative_to(self.root)))

        index = self.wiki / "index.md"
        if index.exists():
            idx = index.read_text()
            missing = [p.stem for p in pages if p.stem not in idx and p.name not in {"index.md", "log.md"}]
            if missing:
                issues["index_drift"].extend(missing)

        concept_titles = defaultdict(list)
        for page in (self.wiki / "concepts").glob("*.md"):
            fm, _ = parse_frontmatter(page.read_text(errors="ignore"))
            concept_titles[(fm.get("title") or "").strip().lower()].append(page.stem)
        for _, dupes in concept_titles.items():
            if len(dupes) > 1:
                issues["duplicate_concepts"].append(", ".join(sorted(dupes)))

        for page in pages:
            _, body = parse_frontmatter(page.read_text(errors="ignore"))
            if "contested" in body.lower() and "superseded" in body.lower():
                issues["conflicting_claims"].append(str(page.relative_to(self.root)))

        return dict(issues)
