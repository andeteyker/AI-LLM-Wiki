from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass
class NormalizedSource:
    source_kind: str
    external_id: str
    markdown: str
    metadata: dict


class IngestionConnector(Protocol):
    name: str

    def normalize(self, payload: str) -> NormalizedSource:
        """Convert provider payload into normalized markdown + metadata."""


class EmailConnector:
    name = "email"

    def normalize(self, payload: str) -> NormalizedSource:
        return NormalizedSource("email", "placeholder", f"# Email\n\n{payload}", {"ready": False})


class MeetingNotesConnector:
    name = "meeting-notes"

    def normalize(self, payload: str) -> NormalizedSource:
        return NormalizedSource("meeting-notes", "placeholder", f"# Meeting Notes\n\n{payload}", {"ready": False})


class ChatExportConnector:
    name = "chat-export"

    def normalize(self, payload: str) -> NormalizedSource:
        return NormalizedSource("chat-export", "placeholder", f"# Chat Export\n\n{payload}", {"ready": False})


class BookmarkConnector:
    name = "bookmarked-websites"

    def normalize(self, payload: str) -> NormalizedSource:
        return NormalizedSource("bookmark", "placeholder", f"# Bookmark\n\n{payload}", {"ready": False})


class PDFConnector:
    name = "pdf"

    def normalize(self, payload: str) -> NormalizedSource:
        return NormalizedSource("pdf", "placeholder", f"# PDF Placeholder\n\n{payload}", {"ocr_ready": True})


class VaultConnector:
    name = "local-markdown-vault"

    def normalize(self, payload: str) -> NormalizedSource:
        return NormalizedSource("vault", "placeholder", f"# Vault Import\n\n{payload}", {"ready": False})


class ScreenshotOCRConnector:
    name = "screenshot-ocr"

    def normalize(self, payload: str) -> NormalizedSource:
        return NormalizedSource("screenshot", "placeholder", f"# Screenshot OCR Placeholder\n\n{payload}", {"ocr_ready": True})
