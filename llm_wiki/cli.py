from __future__ import annotations

import json
import time
from pathlib import Path

try:
    import typer
except Exception:  # pragma: no cover
    class _TyperShim:
        class Typer:
            def __init__(self, *args, **kwargs):
                pass
            def command(self, *args, **kwargs):
                def deco(fn):
                    return fn
                return deco
        @staticmethod
        def Option(default, *args, **kwargs):
            return default
        @staticmethod
        def echo(msg):
            print(msg)
    typer = _TyperShim()

from llm_wiki.compile import Compiler
from llm_wiki.config import load_config
from llm_wiki.ingest import IngestService
from llm_wiki.linting import LintEngine
from llm_wiki.query import QueryEngine
from llm_wiki.repair import RepairEngine
from llm_wiki.status import build_status

app = typer.Typer(help="Local-first LLM Wiki Compiler")


def ensure_layout(root: Path) -> None:
    for p in [
        "inbox",
        "raw",
        "wiki/dashboards",
        "wiki/entities",
        "wiki/concepts",
        "wiki/projects",
        "wiki/decisions",
        "wiki/procedures",
        "wiki/queries",
        "wiki/sources",
        "memory",
        "state",
        "prompts",
        "tests",
    ]:
        (root / p).mkdir(parents=True, exist_ok=True)


@app.command()
def ingest(value: str, root: Path = typer.Option(Path("."), help="Project root")) -> None:
    """wiki ingest <url|file|text>"""
    ensure_layout(root)
    config = load_config(root / "config.yaml")
    rec = IngestService(root, config).ingest(value)
    typer.echo(json.dumps(rec.model_dump(mode="json"), indent=2))


@app.command()
def compile(root: Path = typer.Option(Path("."), help="Project root")) -> None:
    """wiki compile"""
    ensure_layout(root)
    result = Compiler(root).compile()
    typer.echo(json.dumps(result, indent=2))


@app.command()
def query(question: str, save: bool = typer.Option(False, "--save"), root: Path = typer.Option(Path("."), help="Project root")) -> None:
    """wiki query '<question>' [--save]"""
    ensure_layout(root)
    result = QueryEngine(root).query(question, save=save)
    typer.echo(json.dumps(result.model_dump(), indent=2))


@app.command()
def lint(root: Path = typer.Option(Path("."), help="Project root")) -> None:
    """wiki lint"""
    ensure_layout(root)
    issues = LintEngine(root).lint()
    typer.echo(json.dumps(issues, indent=2))


@app.command()
def repair(
    fix_links: bool = typer.Option(True),
    merge_duplicates: bool = typer.Option(True),
    rebuild_stale: bool = typer.Option(True),
    root: Path = typer.Option(Path("."), help="Project root"),
) -> None:
    """wiki repair"""
    ensure_layout(root)
    result = RepairEngine(root).repair(fix_links=fix_links, merge_duplicates=merge_duplicates, rebuild_stale=rebuild_stale)
    typer.echo(json.dumps(result, indent=2))


@app.command()
def watch(root: Path = typer.Option(Path("."), help="Project root")) -> None:
    """wiki watch"""
    ensure_layout(root)
    config = load_config(root / "config.yaml")
    typer.echo("Watching raw/ for changes (Ctrl+C to stop)...")
    prev = None
    try:
        while True:
            current = sorted((p.name, p.stat().st_mtime_ns) for p in (root / "raw").glob("*.md"))
            if prev is not None and current != prev:
                typer.echo("Change detected. Running compile...")
                typer.echo(json.dumps(Compiler(root).compile(), indent=2))
            prev = current
            time.sleep(config.watch_interval_seconds)
    except KeyboardInterrupt:
        typer.echo("Stopped watcher.")


@app.command()
def status(root: Path = typer.Option(Path("."), help="Project root")) -> None:
    """wiki status"""
    ensure_layout(root)
    typer.echo(json.dumps(build_status(root), indent=2))


if __name__ == "__main__":
    app()
