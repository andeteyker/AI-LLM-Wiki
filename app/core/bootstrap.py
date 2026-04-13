from pathlib import Path

from app.core.logging import configure_logging
from app.core.settings import settings


def ensure_runtime_layout() -> None:
    required = [
        settings.base_dir,
        settings.inbox_dir,
        settings.knowledge_dir,
        settings.logs_dir,
        settings.trash_dir,
        settings.base_dir / "memory",
        settings.base_dir / "cache",
    ]
    for path in required:
        Path(path).mkdir(parents=True, exist_ok=True)
    for name in [
        "arbeit",
        "privat",
        "projekte",
        "wissensthemen",
        "aufgaben",
        "termine",
        "personen",
        "dateien",
        "archiv",
    ]:
        (settings.knowledge_dir / name).mkdir(parents=True, exist_ok=True)
    configure_logging(settings.logs_dir, settings.log_level)
