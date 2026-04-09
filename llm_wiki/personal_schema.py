from __future__ import annotations

from llm_wiki.pydantic_compat import BaseModel, Field


class PreferenceProfile(BaseModel):
    person: str = "self"
    preferences: list[str] = Field(default_factory=list)


class ProjectProfile(BaseModel):
    name: str
    goals: list[str] = Field(default_factory=list)
    recurring_tasks: list[str] = Field(default_factory=list)


class DecisionEntry(BaseModel):
    decision: str
    rationale: str
    status: str = "active"


class RelationshipEntry(BaseModel):
    person: str
    relationship: str
    notes: list[str] = Field(default_factory=list)


class LearningTopic(BaseModel):
    topic: str
    current_level: str = "unknown"
    next_steps: list[str] = Field(default_factory=list)


class ActionItem(BaseModel):
    task: str
    due: str | None = None
    status: str = "open"
