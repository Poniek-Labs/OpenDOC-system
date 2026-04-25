"""
Serializer for OpenDOC `.sodf` files.

Copyright (c) 2026 Poniek Labs, All rights reserved.
SPDX-License-Identifier: GPL-3.0-only
"""

from __future__ import annotations

import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from constants import (
        CONTENT_HTML_PATH,
        DEFAULT_STYLES,
        MANIFEST_PATH,
        METADATA_PATH,
        SODF_EXTENSION,
        STYLES_PATH,
    )
    from models import OpenDOCDocument, OpenDOCMetadata
    from validator import SODFValidator
except ImportError:
    from .constants import (
        CONTENT_HTML_PATH,
        DEFAULT_STYLES,
        MANIFEST_PATH,
        METADATA_PATH,
        SODF_EXTENSION,
        STYLES_PATH,
    )
    from .models import OpenDOCDocument, OpenDOCMetadata
    from .validator import SODFValidator


class SODFSerializer:
    def __init__(self):
        self.validator = SODFValidator()

    @staticmethod
    def _iso_now() -> str:
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _sha256(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def build_manifest(self, assets: dict[str, bytes]) -> dict[str, Any]:
        files = []
        for path, payload in sorted(assets.items()):
            files.append(
                {
                    "path": path,
                    "size": len(payload),
                    "sha256": self._sha256(payload),
                }
            )
        return {"files": files}

    def save(self, file_path: str, document: OpenDOCDocument) -> str:
        output = Path(file_path)
        if output.suffix.lower() != SODF_EXTENSION:
            output = output.with_suffix(SODF_EXTENSION)

        document.metadata.modified = self._iso_now()
        if not document.styles:
            document.styles = dict(DEFAULT_STYLES)
        document.manifest = self.build_manifest(document.assets)

        self.validator.validate_document(document)

        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr(CONTENT_HTML_PATH, document.content_html)
            archive.writestr(METADATA_PATH, json.dumps(document.metadata.to_dict(), indent=2))
            archive.writestr(STYLES_PATH, json.dumps(document.styles, indent=2))
            archive.writestr(MANIFEST_PATH, json.dumps(document.manifest, indent=2))

            for asset_path, payload in document.assets.items():
                archive.writestr(asset_path, payload)

        return str(output)

    def load(self, file_path: str) -> OpenDOCDocument:
        with zipfile.ZipFile(file_path, "r") as archive:
            namelist = archive.namelist()
            self.validator.validate_archive_paths(namelist)

            metadata_raw = json.loads(archive.read(METADATA_PATH).decode("utf-8"))
            self.validator.validate_metadata(metadata_raw)

            content_html = archive.read(CONTENT_HTML_PATH).decode("utf-8")
            styles = json.loads(archive.read(STYLES_PATH).decode("utf-8"))
            manifest = json.loads(archive.read(MANIFEST_PATH).decode("utf-8"))

            assets: dict[str, bytes] = {}
            for name in namelist:
                if name.startswith("assets/"):
                    assets[name] = archive.read(name)

            doc = OpenDOCDocument(
                metadata=OpenDOCMetadata.from_dict(metadata_raw),
                content_html=content_html,
                styles=styles,
                manifest=manifest,
                assets=assets,
            )
            self.validator.validate_document(doc)
            return doc
