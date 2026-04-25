"""
Interpreter layer for OpenDOC.

This is the ergonomic API you call from apps:
- create documents
- add assets
- save/load `.sodf`
- render html with optional data-URI embedded assets

Copyright (c) 2026 Poniek Labs, All rights reserved.
SPDX-License-Identifier: GPL-3.0-only
"""

from __future__ import annotations

import base64
import mimetypes
from pathlib import Path
from typing import Any

try:
    from constants import ASSETS_ATTACHMENTS_ROOT, ASSETS_IMAGES_ROOT, DEFAULT_STYLES
    from models import OpenDOCDocument, OpenDOCMetadata
    from serializer import SODFSerializer
except ImportError:
    from .constants import ASSETS_ATTACHMENTS_ROOT, ASSETS_IMAGES_ROOT, DEFAULT_STYLES
    from .models import OpenDOCDocument, OpenDOCMetadata
    from .serializer import SODFSerializer


class OpenDOCInterpreter:
    def __init__(self):
        self.serializer = SODFSerializer()

    def new_document(
        self,
        title: str = "",
        html: str = "",
        author: str = "",
        description: str = "",
        tags: list[str] | None = None,
    ) -> OpenDOCDocument:
        metadata = OpenDOCMetadata(
            title=title,
            author=author,
            description=description,
            tags=tags or [],
        )
        return OpenDOCDocument(
            metadata=metadata,
            content_html=html,
            styles=dict(DEFAULT_STYLES),
            manifest={"files": []},
            assets={},
        )

    def add_asset(
        self,
        document: OpenDOCDocument,
        source_path: str,
        bucket: str = "images",
        target_name: str | None = None,
    ) -> str:
        src = Path(source_path)
        if not src.exists():
            raise FileNotFoundError(source_path)

        data = src.read_bytes()
        filename = target_name or src.name
        if bucket == "images":
            asset_path = f"{ASSETS_IMAGES_ROOT}/{filename}"
        else:
            asset_path = f"{ASSETS_ATTACHMENTS_ROOT}/{filename}"

        document.assets[asset_path] = data
        document.manifest = self.serializer.build_manifest(document.assets)
        return asset_path

    def save(self, path: str, document: OpenDOCDocument) -> str:
        return self.serializer.save(path, document)

    def load(self, path: str) -> OpenDOCDocument:
        return self.serializer.load(path)

    def render_html(self, document: OpenDOCDocument, embed_assets: bool = False) -> str:
        if not embed_assets:
            return document.content_html

        html = document.content_html
        for asset_path, payload in document.assets.items():
            mime, _ = mimetypes.guess_type(asset_path)
            mime = mime or "application/octet-stream"
            encoded = base64.b64encode(payload).decode("ascii")
            data_uri = f"data:{mime};base64,{encoded}"
            html = html.replace(asset_path, data_uri)
        return html

    def snapshot(self, document: OpenDOCDocument) -> dict[str, Any]:
        return {
            "metadata": document.metadata.to_dict(),
            "styles": document.styles,
            "manifest": document.manifest,
            "asset_count": len(document.assets),
        }
