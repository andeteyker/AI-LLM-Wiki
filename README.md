# LLM Wiki Compiler (Local-First Personal Knowledge OS)

Production-ready Python CLI that compiles raw captures into a persistent, interlinked Markdown wiki (Obsidian-compatible), inspired by the LLM Wiki pattern and optimized for long-term personal knowledge management.

## Features

- Strict storage separation:
  - `inbox/` unprocessed captures
  - `raw/` immutable normalized sources
  - `wiki/` generated knowledge artifacts
  - `memory/` stable distilled insights
  - `state/` manifests, hashes, graph and diagnostics
- Incremental compile via SHA-256 source hashes.
- Two-phase compile:
  1. Extract concepts/entities/topics/claims from changed sources.
  2. Merge concepts and update pages order-independently.
- Obsidian compatibility:
  - `[[wikilinks]]`
  - backlink-aware linting
  - `wiki/index.md`
  - append-only `wiki/log.md`
- Frontmatter on generated pages:
  `title`, `type`, `summary`, `created_at`, `updated_at`, `source_refs`, `related`, `confidence`, `freshness`, `status`.
- Paragraph/section provenance via source footnotes (`[^src-...]`).
- Lint and repair flows.
- Query against compiled wiki first; optional `--save` writes to `wiki/queries/`.

## Page Types

Implemented page types:
- `entity`
- `concept`
- `source-summary`
- `project-state`
- `decision-record`
- `procedure`
- `query-answer`
- `timeline-entry`

Knowledge distinction schema for claims:
- factual knowledge
- personal preferences
- open questions
- decisions
- tasks
- speculative ideas

## Project Structure

```text
project-root/
├─ inbox/
├─ raw/
├─ wiki/
│  ├─ index.md
│  ├─ log.md
│  ├─ dashboards/
│  ├─ entities/
│  ├─ concepts/
│  ├─ projects/
│  ├─ decisions/
│  ├─ procedures/
│  ├─ queries/
│  └─ sources/
├─ memory/
├─ state/
├─ prompts/
├─ tests/
├─ AGENTS.md
├─ config.yaml
└─ README.md
```

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[test]
```

## CLI Commands

```bash
wiki ingest <url|file|text>
wiki compile
wiki query "<question>"
wiki query "<question>" --save
wiki lint
wiki repair
wiki watch
wiki status
```

## Example Workflow

```bash
wiki ingest "Project Atlas decision: prioritize deterministic compilation"
wiki compile
wiki query "What did we decide about embeddings?" --save
wiki lint
wiki status
```

## Extensibility Roadmap

Support-ready ingestion architecture prepared for future connectors:
- email
- meeting notes
- chat exports
- bookmarked websites
- PDFs
- local markdown vaults
- screenshots / OCR placeholders

Suggested module pattern for each connector:
- `normalize(input) -> markdown`
- `metadata(input) -> source attributes`
- `ingest(normalized, metadata) -> raw immutable source`

## Determinism + LLM Optionality

Core pipeline is deterministic and testable. LLM calls are isolated behind `llm.py` provider abstraction (OpenAI-compatible endpoint support) and can remain disabled for reproducibility.

## Development

Run tests:

```bash
pytest
```

## Notes

- Raw sources are immutable after ingestion.
- Oversize sources are truncated with explicit marker, never silently hidden.
- Conflicting claims should be marked contested/superseded/unresolved rather than overwriting historical evidence.
