# AGENTS.md — LLM Wiki Compiler Operational Contract

This repository uses AGENTS.md as an execution contract for automated agents and humans.

## Mission
Compile raw sources into a persistent, interlinked, Obsidian-compatible wiki that compounds over time.

## Canonical Data Zones
- `inbox/`: unprocessed captures.
- `raw/`: immutable normalized source material. Never edit in place after ingestion.
- `wiki/`: generated and maintained knowledge artifacts.
- `memory/`: stable long-term distilled insights and preference snapshots.
- `state/`: manifests, hashes, graph metadata, diagnostics.

## Compile Contract
1. Phase 1 extraction from all changed sources (`state/phase1_extractions.json`).
2. Phase 2 page generation from merged concept sets (order independent).
3. Incremental rebuild based on SHA-256 (`state/compile_state.json`).

## Knowledge Semantics
Never collapse all notes into one type. Preserve distinctions:
- Factual knowledge
- Personal preferences
- Open questions
- Decisions
- Tasks
- Speculative ideas

Use dedicated page types and/or claim tags to encode these differences.

## Safety Rules
- Do not silently delete source evidence.
- Contradictions must mark contested/superseded/unresolved state.
- Truncation must be explicit with a marker.

## Markdown Requirements
All generated pages must include YAML frontmatter fields:
`title`, `type`, `summary`, `created_at`, `updated_at`, `source_refs`, `related`, `confidence`, `freshness`, `status`.

Also include paragraph-level provenance markers referencing `raw/` sources.

## Extensibility Readiness
Keep ingestion interfaces ready for:
email, meetings, chat exports, bookmarks, PDFs, vault imports, screenshots/OCR placeholders.
