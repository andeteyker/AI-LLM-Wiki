from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from app.core.schemas import RawDocument, SourceReference


class BaseParser(ABC):
    name: str
    supported_suffixes: set[str]

    def can_parse(self, path: Path) -> bool:
        return path.suffix.lower() in self.supported_suffixes

    @abstractmethod
    def parse(self, path: Path, source: SourceReference) -> RawDocument:
        raise NotImplementedError


class ParserRegistry:
    def __init__(self) -> None:
        self._parsers: list[BaseParser] = []

    def register(self, parser: BaseParser) -> None:
        self._parsers.append(parser)

    def resolve(self, path: Path) -> BaseParser | None:
        for parser in self._parsers:
            if parser.can_parse(path):
                return parser
        return None

    @property
    def parser_names(self) -> list[str]:
        return [parser.name for parser in self._parsers]
