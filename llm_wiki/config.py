from __future__ import annotations

from pathlib import Path

from llm_wiki import yaml_compat as yaml
from llm_wiki.pydantic_compat import BaseModel, Field


class LLMConfig(BaseModel):
    provider: str = "openai-compatible"
    base_url: str = "http://localhost:11434/v1"
    model: str = "llama3.1"
    api_key_env: str = "OPENAI_API_KEY"
    enabled: bool = False


class AppConfig(BaseModel):
    project_name: str = "LLM Wiki Compiler"
    llm: LLMConfig = Field(default_factory=LLMConfig)
    max_source_chars: int = 12000
    watch_interval_seconds: int = 2


DEFAULT_CONFIG = AppConfig()


def load_config(path: Path) -> AppConfig:
    if not path.exists():
        return DEFAULT_CONFIG
    data = yaml.safe_load(path.read_text()) or {}
    return AppConfig.model_validate(data)
