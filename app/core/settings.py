from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="AIOS_", extra="ignore")

    env: str = "development"
    base_dir: Path = Field(default=Path("./data"))

    inbox_subdir: str = "inbox"
    knowledge_subdir: str = "knowledge"
    logs_subdir: str = "logs"
    trash_subdir: str = "trash"
    cache_subdir: str = "cache"
    memory_subdir: str = "memory"

    safe_mode: bool = True
    log_level: str = "INFO"

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5:7b"
    ollama_timeout_sec: int = 20

    active_parsers: str = "text,json,csv,pdf,image_stub,excel_stub,fallback"

    @property
    def inbox_dir(self) -> Path:
        return self.base_dir / self.inbox_subdir

    @property
    def knowledge_dir(self) -> Path:
        return self.base_dir / self.knowledge_subdir

    @property
    def logs_dir(self) -> Path:
        return self.base_dir / self.logs_subdir

    @property
    def trash_dir(self) -> Path:
        return self.base_dir / self.trash_subdir

    @property
    def cache_dir(self) -> Path:
        return self.base_dir / self.cache_subdir

    @property
    def memory_dir(self) -> Path:
        return self.base_dir / self.memory_subdir

    @property
    def active_parser_list(self) -> list[str]:
        return [parser.strip() for parser in self.active_parsers.split(",") if parser.strip()]


settings = Settings()
