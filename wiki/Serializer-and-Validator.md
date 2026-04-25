# Serializer and Validator

Copyright (c) 2026 Poniek Labs, All rights reserved.  
SPDX-License-Identifier: GPL-3.0-only

## Serializer

`SODFSerializer` is responsible for:

- Building manifest checksums
- Writing required archive structure
- Reading and reconstructing `OpenDOCDocument`

## Validator

`SODFValidator` enforces:

- Required archive entries
- Metadata format and version
- Manifest integrity
- HTML asset references

## Failure Behavior

Validation failures raise `SODFValidationError`.

