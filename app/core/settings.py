from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="AIOS_")

    env: str = "development"
    base_dir: Path = Field(default=Path("./data"))
    safe_mode: bool = True
    log_level: str = "INFO"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5:7b"

    @property
    def inbox_dir(self) -> Path:
        return self.base_dir / "inbox"

    @property
    def knowledge_dir(self) -> Path:
        return self.base_dir / "knowledge"

    @property
    def logs_dir(self) -> Path:
        return self.base_dir / "logs"

    @property
    def trash_dir(self) -> Path:
        return self.base_dir / "trash"


settings = Settings()
