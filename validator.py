"""
Validation helpers for `.sodf` archives and in-memory document objects.

Copyright (c) 2026 Poniek Labs, All rights reserved.
SPDX-License-Identifier: GPL-3.0-only
"""

from __future__ import annotations

import re
from typing import Any

try:
    from constants import (
        CONTENT_HTML_PATH,
        MANIFEST_PATH,
        METADATA_PATH,
        SODF_FORMAT_NAME,
        SODF_VERSION,
        STYLES_PATH,
    )
    from models import OpenDOCDocument
except ImportError:
    from .constants import (
        CONTENT_HTML_PATH,
        MANIFEST_PATH,
        METADATA_PATH,
        SODF_FORMAT_NAME,
        SODF_VERSION,
        STYLES_PATH,
    )
    from .models import OpenDOCDocument


class SODFValidationError(ValueError):
    pass


class SODFValidator:
    REQUIRED_ARCHIVE_PATHS = {CONTENT_HTML_PATH, METADATA_PATH, STYLES_PATH, MANIFEST_PATH}

    def validate_archive_paths(self, namelist: list[str]) -> None:
        missing = sorted(self.REQUIRED_ARCHIVE_PATHS - set(namelist))
        if missing:
            raise SODFValidationError(f"SODF archive missing required entries: {missing}")

    def validate_metadata(self, metadata: dict[str, Any]) -> None:
        if metadata.get("format") != SODF_FORMAT_NAME:
            raise SODFValidationError("Invalid metadata.format for SODF")
        version = int(metadata.get("version", -1))
        if version <= 0 or version > SODF_VERSION:
            raise SODFValidationError(
                f"Unsupported SODF version {version}. Supported up to {SODF_VERSION}."
            )

        for key in ("created", "modified"):
            value = metadata.get(key, "")
            if not isinstance(value, str) or not value.strip():
                raise SODFValidationError(f"metadata.{key} must be a non-empty ISO timestamp string")

    def validate_manifest(self, manifest: dict[str, Any], assets: dict[str, bytes]) -> None:
        files = manifest.get("files", [])
        if not isinstance(files, list):
            raise SODFValidationError("manifest.files must be a list")

        for entry in files:
            path = entry.get("path")
            if not path:
                raise SODFValidationError("manifest entry missing path")
            if path not in assets:
                raise SODFValidationError(f"Manifest references missing asset: {path}")

    def validate_html_asset_refs(self, html: str, assets: dict[str, bytes]) -> None:
        refs = set(re.findall(r'''src=["']([^"']+)["']''', html))
        for ref in refs:
            if ref.startswith("assets/") and ref not in assets:
                raise SODFValidationError(f"HTML references missing asset: {ref}")

    def validate_document(self, document: OpenDOCDocument) -> None:
        self.validate_metadata(document.metadata.to_dict())
        self.validate_manifest(document.manifest, document.assets)
        self.validate_html_asset_refs(document.content_html, document.assets)
