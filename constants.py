"""
OpenDOC protocol constants.

Copyright (c) 2026 Poniek Labs, All rights reserved.
SPDX-License-Identifier: GPL-3.0-only
"""

SODF_FORMAT_NAME = "sodf"
SODF_EXTENSION = ".sodf"
SODF_VERSION = 1
OPENDOC_APP_NAME = "OpenDOC"

# Archive structure
CONTENT_HTML_PATH = "content/document.html"
METADATA_PATH = "meta/metadata.json"
STYLES_PATH = "meta/styles.json"
MANIFEST_PATH = "meta/manifest.json"

ASSETS_ROOT = "assets"
ASSETS_IMAGES_ROOT = "assets/images"
ASSETS_ATTACHMENTS_ROOT = "assets/attachments"

# Defaults
DEFAULT_STYLES = {
    "theme": "default",
    "page": {"size": "A4", "margin_mm": 20},
}
