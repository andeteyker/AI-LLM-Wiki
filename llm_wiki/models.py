from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Literal

from llm_wiki.pydantic_compat import BaseModel, Field


class PageType(str, Enum):
    entity = "entity"
    concept = "concept"
    source_summary = "source-summary"
    project_state = "project-state"
    decision_record = "decision-record"
    procedure = "procedure"
    query_answer = "query-answer"
    timeline_entry = "timeline-entry"


class KnowledgeKind(str, Enum):
    factual = "factual-knowledge"
    preference = "personal-preference"
    open_question = "open-question"
    decision = "decision"
    task = "task"
    speculation = "speculative-idea"


class SourceRecord(BaseModel):
    source_id: str
    original: str
    raw_path: str
    source_type: Literal["url", "file", "text"]
    sha256: str
    ingested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    normalized_format: str = "markdown"
    truncated: bool = False


class ExtractionClaim(BaseModel):
    text: str
    knowledge_kind: KnowledgeKind = KnowledgeKind.factual
    confidence: float = 0.6
    status: Literal["active", "contested", "superseded", "unresolved"] = "active"
    source_refs: list[str] = Field(default_factory=list)


class ConceptExtraction(BaseModel):
    concept: str
    aliases: list[str] = Field(default_factory=list)
    entities: list[str] = Field(default_factory=list)
    claims: list[ExtractionClaim] = Field(default_factory=list)
    topics: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)


class PageFrontmatter(BaseModel):
    title: str
    type: PageType
    summary: str
    created_at: str
    updated_at: str
    source_refs: list[str] = Field(default_factory=list)
    related: list[str] = Field(default_factory=list)
    confidence: float = 0.6
    freshness: str = "current"
    status: str = "active"


class Manifest(BaseModel):
    sources: dict[str, SourceRecord] = Field(default_factory=dict)


class CompileState(BaseModel):
    source_hashes: dict[str, str] = Field(default_factory=dict)
    source_to_pages: dict[str, list[str]] = Field(default_factory=dict)
    concept_to_page: dict[str, str] = Field(default_factory=dict)
    page_hashes: dict[str, str] = Field(default_factory=dict)
    last_compile_at: str | None = None


class QueryResult(BaseModel):
    question: str
    answer: str
    wiki_refs: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)


class WikiPaths(BaseModel):
    root: Path
    inbox: Path
    raw: Path
    wiki: Path
    memory: Path
    state: Path
