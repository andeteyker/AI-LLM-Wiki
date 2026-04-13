from __future__ import annotations

import json

from app.core.schemas import KnowledgeEntry, ProjectEntity
from app.core.settings import settings

PROJECTS_FILE = settings.knowledge_dir / "projekte" / "projects.json"


def _load_projects() -> list[dict]:
    if not PROJECTS_FILE.exists():
        return []
    return json.loads(PROJECTS_FILE.read_text(encoding="utf-8"))


def update_project_index(entry: KnowledgeEntry) -> None:
    current = _load_projects()
    by_name = {item["name"]: item for item in current}

    for project_name in entry.related_projects:
        existing = by_name.get(project_name)
        if existing is None:
            entity = ProjectEntity(
                name=project_name,
                related_files=entry.related_files,
                related_people=entry.related_people,
                related_tasks=entry.extracted_tasks,
                related_events=entry.extracted_events,
                related_topics=entry.related_topics,
                confidence=entry.confidence,
            )
            by_name[project_name] = entity.model_dump()
        else:
            for key, values in {
                "related_files": entry.related_files,
                "related_people": entry.related_people,
                "related_tasks": entry.extracted_tasks,
                "related_events": entry.extracted_events,
                "related_topics": entry.related_topics,
            }.items():
                existing.setdefault(key, [])
                for value in values:
                    if value not in existing[key]:
                        existing[key].append(value)

    PROJECTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROJECTS_FILE.write_text(json.dumps(list(by_name.values()), indent=2, ensure_ascii=False), encoding="utf-8")


def list_projects() -> list[dict]:
    return _load_projects()
