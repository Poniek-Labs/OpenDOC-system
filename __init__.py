"""
OpenDOC package

OpenDOC is an open document protocol and reference implementation for `.sodf`
(Source OpenDOC Format) files.

Copyright (c) 2026 Poniek Labs, All rights reserved.
SPDX-License-Identifier: GPL-3.0-only
"""

from .constants import (
    OPENDOC_APP_NAME,
    SODF_EXTENSION,
    SODF_FORMAT_NAME,
    SODF_VERSION,
)
from .interpreter import OpenDOCInterpreter
from .models import OpenDOCDocument, OpenDOCMetadata
from .serializer import SODFSerializer
from .validator import SODFValidator

__all__ = [
    "OPENDOC_APP_NAME",
    "SODF_EXTENSION",
    "SODF_FORMAT_NAME",
    "SODF_VERSION",
    "OpenDOCDocument",
    "OpenDOCMetadata",
    "OpenDOCInterpreter",
    "SODFSerializer",
    "SODFValidator",
]
