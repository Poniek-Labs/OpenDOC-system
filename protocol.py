"""
OpenDOC protocol description in Python form.

The `.sodf` (Source OpenDOC Format) container is a ZIP archive with this layout:

- content/document.html
- meta/metadata.json
- meta/styles.json
- meta/manifest.json
- assets/images/*
- assets/attachments/*

Copyright (c) 2026 Poniek Labs, All rights reserved.
SPDX-License-Identifier: GPL-3.0-only
"""

from __future__ import annotations

from dataclasses import dataclass

try:
    from constants import (
        CONTENT_HTML_PATH,
        MANIFEST_PATH,
        METADATA_PATH,
        SODF_EXTENSION,
        SODF_FORMAT_NAME,
        SODF_VERSION,
        STYLES_PATH,
    )
except ImportError:
    from .constants import (
        CONTENT_HTML_PATH,
        MANIFEST_PATH,
        METADATA_PATH,
        SODF_EXTENSION,
        SODF_FORMAT_NAME,
        SODF_VERSION,
        STYLES_PATH,
    )


@dataclass(frozen=True)
class OpenDOCProtocol:
    name: str = SODF_FORMAT_NAME
    extension: str = SODF_EXTENSION
    version: int = SODF_VERSION
    content_path: str = CONTENT_HTML_PATH
    metadata_path: str = METADATA_PATH
    styles_path: str = STYLES_PATH
    manifest_path: str = MANIFEST_PATH

    def describe(self) -> dict[str, str | int]:
        return {
            "name": self.name,
            "extension": self.extension,
            "version": self.version,
            "content_path": self.content_path,
            "metadata_path": self.metadata_path,
            "styles_path": self.styles_path,
            "manifest_path": self.manifest_path,
        }
