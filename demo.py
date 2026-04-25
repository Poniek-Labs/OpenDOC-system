"""
OpenDOC demo script.

Run:
    python demo.py

Copyright (c) 2026 Poniek Labs, All rights reserved.
SPDX-License-Identifier: GPL-3.0-only
"""

from __future__ import annotations

from pathlib import Path

try:
    from interpreter import OpenDOCInterpreter
except ImportError:
    from .interpreter import OpenDOCInterpreter


def main() -> None:
    api = OpenDOCInterpreter()
    doc = api.new_document(
        title="OpenDOC Demo",
        html="<h1>OpenDOC</h1><p>This is a .sodf demo document.</p>",
        author="Poniek Labs",
    )

    output = Path("opendoc_demo.sodf")
    saved_path = api.save(str(output), doc)
    loaded = api.load(saved_path)
    print("Created:", saved_path)
    print("Snapshot:", api.snapshot(loaded))


if __name__ == "__main__":
    main()
