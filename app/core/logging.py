from __future__ import annotations

import logging
from pathlib import Path


def _make_file_handler(path: Path, level: int) -> logging.FileHandler:
    handler = logging.FileHandler(path, encoding="utf-8")
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
    return handler


def configure_logging(log_dir: Path, level: str = "INFO") -> None:
    log_dir.mkdir(parents=True, exist_ok=True)
    log_level = getattr(logging, level.upper(), logging.INFO)

    root = logging.getLogger()
    root.setLevel(log_level)
    root.handlers.clear()

    stream = logging.StreamHandler()
    stream.setLevel(log_level)
    stream.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
    root.addHandler(stream)

    root.addHandler(_make_file_handler(log_dir / "ai-os.log", log_level))

    scoped = {
        "ingestion": "ingestion.log",
        "knowledge": "knowledge.log",
        "errors": "errors.log",
        "file_actions": "file_actions.log",
        "agent_decisions": "agent_decisions.log",
    }
    for logger_name, filename in scoped.items():
        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)
        logger.handlers.clear()
        logger.propagate = True
        logger.addHandler(_make_file_handler(log_dir / filename, log_level))
