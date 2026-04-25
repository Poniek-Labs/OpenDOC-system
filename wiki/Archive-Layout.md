# Archive Layout

Copyright (c) 2026 Poniek Labs, All rights reserved.  
SPDX-License-Identifier: GPL-3.0-only

## Canonical Structure

```text
content/
  document.html
meta/
  metadata.json
  styles.json
  manifest.json
assets/
  images/
  attachments/
```

## Rules

- `content/document.html` is the rich text body
- `meta/metadata.json` is required and authoritative
- `meta/manifest.json` must track every asset
- Assets referenced in HTML must exist in archive

