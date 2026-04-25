"""
Small CLI for OpenDOC reference implementation.

Examples:
    python cli.py init out.sodf --title "Hello"
    python cli.py inspect out.sodf

Copyright (c) 2026 Poniek Labs, All rights reserved.
SPDX-License-Identifier: GPL-3.0-only
"""

from __future__ import annotations

import argparse
import json

try:
    from interpreter import OpenDOCInterpreter
except ImportError:
    from .interpreter import OpenDOCInterpreter


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="OpenDOC .sodf tool")
    sub = parser.add_subparsers(dest="command", required=True)

    init_cmd = sub.add_parser("init", help="Create a new .sodf file")
    init_cmd.add_argument("output", help="Path to .sodf")
    init_cmd.add_argument("--title", default="", help="Document title")
    init_cmd.add_argument("--html", default="<p>Hello OpenDOC</p>", help="Initial HTML body")

    inspect_cmd = sub.add_parser("inspect", help="Inspect .sodf metadata and manifest")
    inspect_cmd.add_argument("input", help="Path to .sodf")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    interpreter = OpenDOCInterpreter()

    if args.command == "init":
        doc = interpreter.new_document(title=args.title, html=args.html)
        out = interpreter.save(args.output, doc)
        print(f"Created {out}")
        return 0

    if args.command == "inspect":
        doc = interpreter.load(args.input)
        print(json.dumps(interpreter.snapshot(doc), indent=2))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
