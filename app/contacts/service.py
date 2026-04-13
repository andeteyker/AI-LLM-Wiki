from __future__ import annotations

import json
from pathlib import Path

from app.core.schemas import KnowledgeEntry, PersonEntity
from app.core.settings import settings

PEOPLE_FILE = settings.knowledge_dir / "personen" / "people.json"


def _load_people() -> list[dict]:
    if not PEOPLE_FILE.exists():
        return []
    return json.loads(PEOPLE_FILE.read_text(encoding="utf-8"))


def update_people_index(entry: KnowledgeEntry) -> None:
    current = _load_people()
    by_name = {item["name"]: item for item in current}

    for person_name in entry.related_people:
        existing = by_name.get(person_name)
        if existing is None:
            entity = PersonEntity(
                name=person_name,
                related_projects=entry.related_projects,
                sources=[entry.source_path],
                communication_context=[entry.summary_short],
                confidence=entry.confidence,
            )
            by_name[person_name] = entity.model_dump()
        else:
            existing.setdefault("sources", [])
            if entry.source_path not in existing["sources"]:
                existing["sources"].append(entry.source_path)
            existing.setdefault("related_projects", [])
            for project in entry.related_projects:
                if project not in existing["related_projects"]:
                    existing["related_projects"].append(project)

    PEOPLE_FILE.parent.mkdir(parents=True, exist_ok=True)
    PEOPLE_FILE.write_text(json.dumps(list(by_name.values()), indent=2, ensure_ascii=False), encoding="utf-8")


def list_people() -> list[dict]:
    return _load_people()
