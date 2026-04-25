# OpenDOC Reference Framework

Copyright (c) 2026 Poniek Labs, All rights reserved.
SPDX-License-Identifier: GPL-3.0-only

`OpenDOC` is an open-source document protocol and Python reference implementation.

- Format name: `SODF` (Source OpenDOC Format)
- File extension: `.sodf`
- Container: ZIP archive

## SODF Layout

```text
content/document.html
meta/metadata.json
meta/styles.json
meta/manifest.json
assets/images/*
assets/attachments/*
```

## Quick Usage

```python
from interpreter import OpenDOCInterpreter

api = OpenDOCInterpreter()
doc = api.new_document(title="My First OpenDOC", html="<h1>Hello</h1><p>Open format.</p>")
path = api.save("my_doc.sodf", doc)
loaded = api.load(path)
print(api.snapshot(loaded))
```

## Run Without Packaging

Place all `opendoc/*.py` files in your app folder (or a subfolder) and import directly.

From the `opendoc` folder:

```bash
python demo.py
python cli.py init test.sodf --title "Test"
python cli.py inspect test.sodf
```

## Push To GitHub

From the `opendoc` folder:

```powershell
.\push_to_github.ps1 -InitRepo -GitUserName "Your Name" -GitUserEmail "you@example.com"
```

The script will ask:

- `1` Major release: bumps whole number (`1.0 -> 2.0`)
- `2` Minor release: bumps decimal (`1.0 -> 1.1`)

It updates `VERSION`, commits, creates a tag (`vX.Y`), and pushes to:

`https://github.com/Poniek-Labs/OpenDOC-system.git`

After first setup, future pushes can be:

```powershell
.\push_to_github.ps1
```

If GitHub rejects push because remote `main` already has commits:

```powershell
.\push_to_github.ps1 -ForceWithLease
```

Non-interactive examples:

```powershell
.\push_to_github.ps1 -ReleaseType major
.\push_to_github.ps1 -ReleaseType minor
.\push_to_github.ps1 -ReleaseType none -CommitMessage "docs: update wiki"
```

## Goals

1. Open and inspectable document archive
2. App-independent metadata + manifest
3. Clean Python interpreter for integration with editors and services

## License

This project is licensed under GNU GPL v3.0.
See [LICENSE](c:\Users\eswen\Programming\docu\opendoc\LICENSE).

## Wiki

Full local documentation wiki:
[wiki/Home.md](c:\Users\eswen\Programming\docu\opendoc\wiki\Home.md)
