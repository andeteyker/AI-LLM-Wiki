from __future__ import annotations

from pathlib import Path

from llm_wiki.linting import LintEngine
from llm_wiki.models import CompileState, Manifest


def build_status(root: Path) -> dict:
    manifest_path = root / "state" / "manifest.json"
    compile_path = root / "state" / "compile_state.json"
    manifest = Manifest()
    state = CompileState()
    if manifest_path.exists():
        manifest = Manifest.model_validate_json(manifest_path.read_text())
    if compile_path.exists():
        state = CompileState.model_validate_json(compile_path.read_text())
    issues = LintEngine(root).lint()
    return {
        "sources": len(manifest.sources),
        "compiled_sources": len(state.source_hashes),
        "concept_pages": len(list((root / "wiki" / "concepts").glob("*.md"))),
        "last_compile_at": state.last_compile_at,
        "lint_issue_types": sorted(issues.keys()),
    }
