# Manifest and Assets

Copyright (c) 2026 Poniek Labs, All rights reserved.  
SPDX-License-Identifier: GPL-3.0-only

## Manifest Purpose

`meta/manifest.json` tracks asset integrity and traceability.

## Entry Structure

```json
{
  "path": "assets/images/photo.png",
  "size": 12345,
  "sha256": "..."
}
```

## Asset Buckets

- `assets/images/`: image resources used in document HTML
- `assets/attachments/`: optional non-rendered attached files

## Validation Contract

- Every manifest entry path must exist in archive
- Every HTML `src="assets/..."` reference must exist in archive

