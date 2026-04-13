from __future__ import annotations

import argparse
from pathlib import Path
from pprint import pprint

from app.core.bootstrap import ensure_runtime_layout
from app.agents.manager import ManagerAgent


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest a file into AI-OS")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    ensure_runtime_layout()
    manager = ManagerAgent()
    result = manager.ingest_path(args.path)
    pprint(result)


if __name__ == "__main__":
    main()
