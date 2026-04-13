from __future__ import annotations

import httpx

from app.core.settings import settings


class OllamaClient:
    def __init__(self) -> None:
        self.base_url = settings.ollama_base_url.rstrip("/")
        self.model = settings.ollama_model
        self.timeout = settings.ollama_timeout_sec

    def generate(self, prompt: str, system: str = "You are a helpful assistant") -> str | None:
        try:
            response = httpx.post(
                f"{self.base_url}/api/generate",
                json={"model": self.model, "prompt": f"{system}\n\n{prompt}", "stream": False},
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json().get("response")
        except Exception:
            return None
