from __future__ import annotations

from pathlib import Path

from llm_wiki.models import QueryResult
from llm_wiki.utils import extract_wikilinks, now_iso, parse_frontmatter, slugify


class QueryEngine:
    def __init__(self, root: Path):
        self.root = root
        self.wiki = root / "wiki"

    def query(self, question: str, save: bool = False) -> QueryResult:
        pages = list(self.wiki.rglob("*.md"))
        scored: list[tuple[int, Path]] = []
        import re
        words = [w.lower() for w in re.findall(r"[a-zA-Z0-9]+", question) if len(w) > 2]
        for page in pages:
            text = page.read_text(errors="ignore")
            score = sum(text.lower().count(w) for w in words)
            if score > 0:
                scored.append((score, page))
        scored.sort(reverse=True, key=lambda x: x[0])
        top = [p for _, p in scored[:5]]

        answer_lines = [f"Answer synthesized from {len(top)} wiki page(s):"]
        wiki_refs = []
        source_refs = []
        for page in top:
            fm, body = parse_frontmatter(page.read_text(errors="ignore"))
            snippet = " ".join(body.split()[:35])
            answer_lines.append(f"- {page.stem}: {snippet}")
            wiki_refs.append(str(page.relative_to(self.root)))
            source_refs.extend(fm.get("source_refs", []))
            for link in extract_wikilinks(body):
                wiki_refs.append(f"wiki/{link}.md")

        result = QueryResult(
            question=question,
            answer="\n".join(answer_lines) if top else "No matching compiled wiki pages found.",
            wiki_refs=sorted(set(wiki_refs)),
            source_refs=sorted(set(source_refs)),
        )
        if save:
            self._save_query(result)
        return result

    def _save_query(self, result: QueryResult) -> None:
        qdir = self.wiki / "queries"
        qdir.mkdir(parents=True, exist_ok=True)
        name = f"query-{slugify(result.question)[:50]}"
        path = qdir / f"{name}.md"
        refs = "\n".join([f"- {r}" for r in result.wiki_refs])
        sources = "\n".join([f"- {s}" for s in result.source_refs])
        text = (
            "---\n"
            f"title: {name}\n"
            "type: query-answer\n"
            f"summary: saved query answer\n"
            f"created_at: {now_iso()}\n"
            f"updated_at: {now_iso()}\n"
            f"source_refs: {result.source_refs}\n"
            "related: []\n"
            "confidence: 0.5\n"
            "freshness: derived\n"
            "status: active\n"
            "---\n"
            f"# Question\n{result.question}\n\n"
            f"# Answer\n{result.answer}\n\n"
            f"# Wiki References\n{refs}\n\n"
            f"# Source References\n{sources}\n"
        )
        path.write_text(text)

        index = self.wiki / "index.md"
        if index.exists():
            content = index.read_text()
            link = f"- [[{name}]]"
            if link not in content:
                index.write_text(content.rstrip() + "\n" + link + "\n")
