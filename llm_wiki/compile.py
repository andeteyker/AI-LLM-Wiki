from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

from llm_wiki.models import CompileState, ConceptExtraction, ExtractionClaim, KnowledgeKind, PageFrontmatter, PageType
from llm_wiki.utils import dump_yaml_frontmatter, now_iso, parse_frontmatter, sha256_bytes, slugify


class Compiler:
    def __init__(self, root: Path):
        self.root = root
        self.raw = root / "raw"
        self.wiki = root / "wiki"
        self.state_dir = root / "state"
        self.compile_path = self.state_dir / "compile_state.json"
        self.phase1_path = self.state_dir / "phase1_extractions.json"
        self.state_dir.mkdir(parents=True, exist_ok=True)

    def _load_state(self) -> CompileState:
        if not self.compile_path.exists():
            return CompileState()
        return CompileState.model_validate_json(self.compile_path.read_text())

    def _save_state(self, state: CompileState) -> None:
        self.compile_path.write_text(state.model_dump_json(indent=2))

    def _extract_from_markdown(self, source_id: str, text: str) -> list[ConceptExtraction]:
        headers = [h.strip() for h in re.findall(r"^#\s+(.+)$", text, flags=re.M)]
        candidates = set(headers)
        for m in re.findall(r"\b[A-Z][a-z]{3,}(?:\s+[A-Z][a-z]{2,})*\b", text):
            candidates.add(m)
        concepts: list[ConceptExtraction] = []
        for c in sorted(candidates):
            if len(c) < 4:
                continue
            claim_text = f"{c} appears in source {source_id}."
            kind = KnowledgeKind.factual
            lc = c.lower()
            if "prefer" in text.lower() and "preference" in lc:
                kind = KnowledgeKind.preference
            claim = ExtractionClaim(text=claim_text, knowledge_kind=kind, source_refs=[source_id])
            concepts.append(ConceptExtraction(concept=c, claims=[claim], source_refs=[source_id]))
        return concepts

    def compile(self) -> dict[str, int]:
        state = self._load_state()
        changed_sources: dict[str, str] = {}
        for raw_file in sorted(self.raw.glob("*.md")):
            source_id = raw_file.stem
            digest = sha256_bytes(raw_file.read_bytes())
            if state.source_hashes.get(source_id) != digest:
                changed_sources[source_id] = digest

        if not changed_sources:
            self._ensure_index(state)
            return {"changed_sources": 0, "updated_pages": 0}

        phase1: dict[str, list[dict]] = {}
        concept_map: dict[str, ConceptExtraction] = {}

        for source_id, digest in changed_sources.items():
            text = (self.raw / f"{source_id}.md").read_text(errors="ignore")
            extractions = self._extract_from_markdown(source_id, text)
            phase1[source_id] = [e.model_dump() for e in extractions]
            for ext in extractions:
                key = slugify(ext.concept)
                current = concept_map.get(key)
                if current is None:
                    concept_map[key] = ext
                else:
                    current.source_refs.extend([r for r in ext.source_refs if r not in current.source_refs])
                    current.claims.extend(ext.claims)

            source_page = self._write_source_summary(source_id, text)
            state.source_to_pages[source_id] = [source_page]
            state.source_hashes[source_id] = digest

        updated_pages = 0
        impacted_sources = set(changed_sources.keys())
        for key, concept in concept_map.items():
            page = self._write_concept_page(key, concept)
            updated_pages += 1
            for src in concept.source_refs:
                state.source_to_pages.setdefault(src, [])
                if page not in state.source_to_pages[src]:
                    state.source_to_pages[src].append(page)
            state.concept_to_page[key] = page

        self.phase1_path.write_text(__import__("json").dumps(phase1, indent=2))
        state.last_compile_at = now_iso()
        self._ensure_index(state)
        self._append_log(f"compile completed: {len(changed_sources)} changed source(s), {updated_pages} concept page(s)")
        self._save_state(state)
        return {"changed_sources": len(changed_sources), "updated_pages": updated_pages, "impacted_sources": len(impacted_sources)}

    def _page_path(self, category: str, name: str) -> Path:
        folder = self.wiki / category
        folder.mkdir(parents=True, exist_ok=True)
        return folder / f"{name}.md"

    def _write_source_summary(self, source_id: str, text: str) -> str:
        name = f"source-{source_id}"
        path = self._page_path("sources", name)
        summary = " ".join(text.split()[:40])
        body = (
            "## Summary\n"
            f"{summary}\n\n"
            f"[^src-{source_id}]: raw/{source_id}.md\n"
        )
        self._write_page(
            path,
            PageFrontmatter(
                title=name,
                type=PageType.source_summary,
                summary=f"Summary for source {source_id}",
                created_at=now_iso(),
                updated_at=now_iso(),
                source_refs=[source_id],
                related=[],
                confidence=0.7,
                freshness="fresh",
                status="active",
            ),
            body,
        )
        return str(path.relative_to(self.root))

    def _write_concept_page(self, key: str, concept: ConceptExtraction) -> str:
        path = self._page_path("concepts", key)
        existed = path.exists()
        existing_fm = {}
        if existed:
            existing_fm, _ = parse_frontmatter(path.read_text())
        related = [f"[[source-{src}]]" for src in sorted(set(concept.source_refs))]
        claims_lines = []
        statuses = {c.status for c in concept.claims}
        overall_status = "contested" if "contested" in statuses else "active"
        for i, claim in enumerate(concept.claims, start=1):
            refs = ", ".join(f"[^src-{r}]" for r in claim.source_refs)
            claims_lines.append(f"- ({claim.knowledge_kind.value}) {claim.text} {refs}")
        footnotes = "\n".join([f"[^src-{r}]: raw/{r}.md" for r in sorted(set(concept.source_refs))])
        body = (
            f"## Concept\n{concept.concept}\n\n"
            f"## Claims\n" + "\n".join(claims_lines) + "\n\n"
            f"## Related\n" + "\n".join(related) + "\n\n"
            + footnotes
            + "\n"
        )
        self._write_page(
            path,
            PageFrontmatter(
                title=concept.concept,
                type=PageType.concept,
                summary=f"Compiled concept page for {concept.concept}",
                created_at=existing_fm.get("created_at", now_iso()),
                updated_at=now_iso(),
                source_refs=sorted(set(concept.source_refs)),
                related=sorted(set(related)),
                confidence=0.6,
                freshness="fresh",
                status=overall_status,
            ),
            body,
        )
        return str(path.relative_to(self.root))

    def _write_page(self, path: Path, fm: PageFrontmatter, body: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        text = dump_yaml_frontmatter(fm.model_dump()) + body
        path.write_text(text)

    def _ensure_index(self, state: CompileState) -> None:
        self.wiki.mkdir(parents=True, exist_ok=True)
        index_path = self.wiki / "index.md"
        links = []
        for page in sorted(state.concept_to_page.values()):
            links.append(f"- [[{Path(page).stem}]]")
        for source_pages in state.source_to_pages.values():
            for page in source_pages:
                links.append(f"- [[{Path(page).stem}]]")
        unique = sorted(set(links))
        text = "# Wiki Index\n\n## Pages\n" + "\n".join(unique) + "\n"
        index_path.write_text(text)

    def _append_log(self, line: str) -> None:
        log = self.wiki / "log.md"
        if not log.exists():
            log.write_text("# Compilation Log\n\n")
        with log.open("a") as f:
            f.write(f"- {now_iso()} {line}\n")
