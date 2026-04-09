from __future__ import annotations

import os
from typing import Protocol


from llm_wiki.config import LLMConfig


class LLMProvider(Protocol):
    def complete(self, prompt: str) -> str: ...


class NoopProvider:
    def complete(self, prompt: str) -> str:
        return "LLM disabled; deterministic pipeline used."


class OpenAICompatibleProvider:
    def __init__(self, config: LLMConfig):
        self.config = config

    def complete(self, prompt: str) -> str:
        api_key = os.getenv(self.config.api_key_env, "")
        headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        payload = {
            "model": self.config.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0,
        }
        try:
            import httpx  # type: ignore
            with httpx.Client(timeout=30.0) as client:
                res = client.post(f"{self.config.base_url}/chat/completions", json=payload, headers=headers)
                res.raise_for_status()
                data = res.json()
        except Exception as exc:
            raise RuntimeError("LLM provider call failed; install httpx or disable llm") from exc
        return data["choices"][0]["message"]["content"]


def get_provider(config: LLMConfig) -> LLMProvider:
    if not config.enabled:
        return NoopProvider()
    return OpenAICompatibleProvider(config)
