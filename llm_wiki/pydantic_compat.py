from __future__ import annotations

from dataclasses import MISSING, asdict, dataclass, field, fields
import json
from typing import Any, Callable


try:
    from pydantic import BaseModel, Field  # type: ignore
except Exception:  # pragma: no cover
    def Field(default: Any = MISSING, default_factory: Callable[[], Any] | None = None):
        if default_factory is not None:
            return field(default_factory=default_factory)
        if default is MISSING:
            return field()
        return field(default=default)

    class BaseModel:
        def __init_subclass__(cls) -> None:
            dataclass(cls)

        @classmethod
        def _coerce(cls, data: dict[str, Any]):
            converted = dict(data)
            ann = getattr(cls, "__annotations__", {})
            for f in fields(cls):
                name = f.name
                t = ann.get(name)
                if name in converted and isinstance(converted[name], dict) and hasattr(t, "model_validate"):
                    converted[name] = t.model_validate(converted[name])
            return converted

        @classmethod
        def model_validate_json(cls, text: str):
            return cls(**cls._coerce(json.loads(text)))

        @classmethod
        def model_validate(cls, data: dict[str, Any]):
            return cls(**cls._coerce(data))

        def model_dump(self, mode: str | None = None):
            return asdict(self)

        def model_dump_json(self, indent: int | None = None):
            return json.dumps(self.model_dump(), indent=indent, default=str)
