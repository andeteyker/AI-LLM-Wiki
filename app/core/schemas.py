from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

EntityType = Literal["Note", "Task", "Event", "File", "Project", "Person", "Topic", "Decision"]


class SourceRef(BaseModel):
    path: str
    kind: str = "local_file"


class KnowledgeEntry(BaseModel):
    id: str
    title: str
    summary: str
    content: str
    entity_types: list[EntityType] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    linked_projects: list[str] = Field(default_factory=list)
    linked_people: list[str] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)
    next_steps: list[str] = Field(default_factory=list)
    confidence: float = 0.5
    source: SourceRef
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class InboxItem(BaseModel):
    path: Path
    detected_type: str | None = None
    imported_at: datetime = Field(default_factory=datetime.utcnow)
