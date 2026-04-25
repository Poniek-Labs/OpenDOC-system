# Interpreter API

Copyright (c) 2026 Poniek Labs, All rights reserved.  
SPDX-License-Identifier: GPL-3.0-only

## Class

- `OpenDOCInterpreter`

## Main Methods

1. `new_document(...) -> OpenDOCDocument`
2. `add_asset(document, source_path, bucket="images", target_name=None) -> str`
3. `save(path, document) -> str`
4. `load(path) -> OpenDOCDocument`
5. `render_html(document, embed_assets=False) -> str`
6. `snapshot(document) -> dict`

## Integration Pattern

Create document -> add assets -> save `.sodf` -> reload -> render/export.

