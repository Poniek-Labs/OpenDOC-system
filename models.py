"""
Core data models for OpenDOC.

Copyright (c) 2026 Poniek Labs, All rights reserved.
SPDX-License-Identifier: GPL-3.0-only
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

try:
    from constants import OPENDOC_APP_NAME, SODF_FORMAT_NAME, SODF_VERSION
except ImportError:
    from .constants import OPENDOC_APP_NAME, SODF_FORMAT_NAME, SODF_VERSION


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class OpenDOCMetadata:
    format: str = SODF_FORMAT_NAME
    version: int = SODF_VERSION
    app: str = OPENDOC_APP_NAME
    title: str = ""
    created: str = field(default_factory=utc_now_iso)
    modified: str = field(default_factory=utc_now_iso)
    author: str = ""
    description: str = ""
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "format": self.format,
            "version": self.version,
            "app": self.app,
            "title": self.title,
            "created": self.created,
            "modified": self.modified,
            "author": self.author,
            "description": self.description,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "OpenDOCMetadata":
        return cls(
            format=raw.get("format", SODF_FORMAT_NAME),
            version=int(raw.get("version", SODF_VERSION)),
            app=raw.get("app", OPENDOC_APP_NAME),
            title=raw.get("title", ""),
            created=raw.get("created", utc_now_iso()),
            modified=raw.get("modified", utc_now_iso()),
            author=raw.get("author", ""),
            description=raw.get("description", ""),
            tags=list(raw.get("tags", [])),
        )


@dataclass
class OpenDOCDocument:
    metadata: OpenDOCMetadata = field(default_factory=OpenDOCMetadata)
    content_html: str = ""
    styles: dict[str, Any] = field(default_factory=dict)
    manifest: dict[str, Any] = field(default_factory=dict)
    assets: dict[str, bytes] = field(default_factory=dict)
