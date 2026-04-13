from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

EntityType = Literal["Note", "Task", "Event", "File", "Project", "Person", "Topic", "Decision"]
StatusType = Literal["new", "review_needed", "confirmed", "conflict", "archived"]
InboxStatus = Literal["neu", "analysiert", "kompiliert", "unsicher", "review_noetig", "archiviert"]


class SourceReference(BaseModel):
    source: str = "local_file"
    source_path: str
    file_type: str
    checksum_sha256: str
    imported_at: datetime = Field(default_factory=datetime.utcnow)


class Relation(BaseModel):
    relation_type: str
    target_id: str
    confidence: float = 0.5


class VersionInfo(BaseModel):
    version: int = 1
    previous_version_path: str | None = None
    changed_at: datetime = Field(default_factory=datetime.utcnow)


class RawDocument(BaseModel):
    id: str
    title: str
    content: str
    source: SourceReference
    detected_types: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PersonEntity(BaseModel):
    name: str
    role: str | None = None
    responsibility: str | None = None
    related_projects: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)
    communication_context: list[str] = Field(default_factory=list)
    confidence: float = 0.5


class ProjectEntity(BaseModel):
    name: str
    related_files: list[str] = Field(default_factory=list)
    related_people: list[str] = Field(default_factory=list)
    related_tasks: list[str] = Field(default_factory=list)
    related_events: list[str] = Field(default_factory=list)
    related_topics: list[str] = Field(default_factory=list)
    confidence: float = 0.5


class TaskEntity(BaseModel):
    text: str
    due_hint: str | None = None
    confidence: float = 0.5
    priority: Literal["low", "medium", "high"] = "medium"
    status: Literal["open", "in_progress", "done"] = "open"
    source_entry_id: str | None = None
    source_path: str | None = None


class EventEntity(BaseModel):
    text: str
    when_hint: str | None = None
    confidence: float = 0.5
    status: Literal["detected", "confirmed", "uncertain"] = "detected"
    source_entry_id: str | None = None
    source_path: str | None = None


class KnowledgeEntry(BaseModel):
    id: str
    title: str
    summary_short: str
    summary_long: str
    content: str
    types: list[EntityType] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    source: str = "local_file"
    source_path: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    confidence: float = 0.5
    related_projects: list[str] = Field(default_factory=list)
    related_people: list[str] = Field(default_factory=list)
    related_files: list[str] = Field(default_factory=list)
    related_topics: list[str] = Field(default_factory=list)
    extracted_tasks: list[str] = Field(default_factory=list)
    extracted_events: list[str] = Field(default_factory=list)
    relations: list[Relation] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)
    next_steps: list[str] = Field(default_factory=list)
    version_info: VersionInfo = Field(default_factory=VersionInfo)
    status: StatusType = "new"
    source_meta: SourceReference


class InboxItem(BaseModel):
    id: str
    path: Path
    original_path: Path
    detected_type: str | None = None
    imported_at: datetime = Field(default_factory=datetime.utcnow)
    checksum_sha256: str | None = None
    status: InboxStatus = "neu"
    error_message: str | None = None


class SearchResult(BaseModel):
    entry_id: str
    title: str
    summary_short: str
    score: int
    source_path: str
    status: StatusType


class ChatAnswer(BaseModel):
    answer: str
    sources: list[str] = Field(default_factory=list)
    related_entries: list[str] = Field(default_factory=list)
    related_files: list[str] = Field(default_factory=list)
    next_steps: list[str] = Field(default_factory=list)
    uncertainty: str | None = None
