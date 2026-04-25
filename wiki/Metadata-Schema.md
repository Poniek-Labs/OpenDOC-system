# Metadata Schema

Copyright (c) 2026 Poniek Labs, All rights reserved.  
SPDX-License-Identifier: GPL-3.0-only

## Required Fields

```json
{
  "format": "sodf",
  "version": 1,
  "app": "OpenDOC",
  "title": "",
  "created": "",
  "modified": ""
}
```

## Extended Fields

- `author` (string)
- `description` (string)
- `tags` (array of strings)

## Notes

- `created` and `modified` should be ISO 8601 timestamps in UTC
- `format` must be exactly `sodf`

