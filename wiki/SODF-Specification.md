# SODF Specification

Copyright (c) 2026 Poniek Labs, All rights reserved.  
SPDX-License-Identifier: GPL-3.0-only

## Container

`.sodf` is a ZIP archive.

## Required Entries

- `content/document.html`
- `meta/metadata.json`
- `meta/styles.json`
- `meta/manifest.json`

## Versioning

- `metadata.version` is protocol version
- Current reference implementation supports version `1`
- Loader must reject unknown higher versions unless explicitly supported

## Encoding

- JSON files: UTF-8
- HTML: UTF-8
- Asset paths: forward-slash normalized

