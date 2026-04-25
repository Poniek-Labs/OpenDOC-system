# CLI Guide

Copyright (c) 2026 Poniek Labs, All rights reserved.  
SPDX-License-Identifier: GPL-3.0-only

## Create a New SODF

```bash
python cli.py init out.sodf --title "My Doc"
```

## Inspect Existing SODF

```bash
python cli.py inspect out.sodf
```

## Notes

- `init` writes minimal valid document structure
- `inspect` prints metadata, styles, manifest, and asset count
