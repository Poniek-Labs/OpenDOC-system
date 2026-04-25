# Examples

Copyright (c) 2026 Poniek Labs, All rights reserved.  
SPDX-License-Identifier: GPL-3.0-only

## Programmatic Save/Load

```python
from interpreter import OpenDOCInterpreter

api = OpenDOCInterpreter()
doc = api.new_document(
    title="Design Notes",
    html="<h1>Design Notes</h1><p>v1 planning</p>",
    author="Poniek Labs"
)

api.save("design.sodf", doc)
loaded = api.load("design.sodf")
print(api.snapshot(loaded))
```

## Add Image Asset

```python
asset_path = api.add_asset(doc, "diagram.png", bucket="images")
doc.content_html += f'<p><img src="{asset_path}" /></p>'
api.save("design_with_image.sodf", doc)
```
