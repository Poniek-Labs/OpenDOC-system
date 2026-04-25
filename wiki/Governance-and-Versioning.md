# Governance and Versioning

Copyright (c) 2026 Poniek Labs, All rights reserved.  
SPDX-License-Identifier: GPL-3.0-only

## Governance Goals

- Keep SODF stable and app-agnostic
- Allow additive evolution without breaking old files

## Version Rules

- Increment minor fields with additive metadata/style changes
- Increment major protocol version for breaking archive/schema changes

## Compatibility Strategy

- Readers should accept same-version files
- Readers may reject higher unsupported versions with clear errors
- Writers should emit current stable version unless explicitly configured

