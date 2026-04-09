from __future__ import annotations

from pathlib import Path

from llm_wiki.compile import Compiler
from llm_wiki.linting import LintEngine
from llm_wiki.utils import extract_wikilinks, parse_frontmatter


class RepairEngine:
    def __init__(self, root: Path):
        self.root = root
        self.wiki = root / "wiki"

    def repair(self, fix_links: bool = True, merge_duplicates: bool = True, rebuild_stale: bool = True) -> dict[str, int]:
        lint = LintEngine(self.root)
        issues = lint.lint()
        fixed_links = 0
        merged = 0
        rebuilt = 0

        if fix_links:
            existing = {p.stem for p in self.wiki.rglob("*.md")}
            for page in self.wiki.rglob("*.md"):
                text = page.read_text(errors="ignore")
                fm, body = parse_frontmatter(text)
                for link in extract_wikilinks(body):
                    if link not in existing:
                        fallback = link.replace("_", "-").lower()
                        if fallback in existing:
                            body = body.replace(f"[[{link}]]", f"[[{fallback}]]")
                            fixed_links += 1
                if fixed_links:
                    head = "---\n" + __import__("llm_wiki.yaml_compat", fromlist=['safe_dump']).safe_dump(fm, sort_keys=False).strip() + "\n---\n"
                    page.write_text(head + body)

        if merge_duplicates:
            dupes = issues.get("duplicate_concepts", [])
            for dup in dupes:
                items = [d.strip() for d in dup.split(",") if d.strip()]
                if len(items) >= 2:
                    canonical = items[0]
                    canonical_path = self.wiki / "concepts" / f"{canonical}.md"
                    for other in items[1:]:
                        other_path = self.wiki / "concepts" / f"{other}.md"
                        if other_path.exists() and canonical_path.exists():
                            other_text = other_path.read_text(errors="ignore")
                            with canonical_path.open("a") as cf:
                                cf.write("\n\n## Merged Evidence\n" + other_text)
                            other_path.rename(other_path.with_suffix(".merged.md"))
                            merged += 1

        if rebuild_stale and (issues.get("stale_pages") or issues.get("index_drift")):
            rebuilt = Compiler(self.root).compile()["updated_pages"]

        return {"fixed_links": fixed_links, "merged_duplicates": merged, "rebuilt_pages": rebuilt}
