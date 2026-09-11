# Specification: Tool Structure (SDD)

This specification defines the JSON schema for a "Tool". A tool is a logical grouping of multiple API endpoints, UI configurations, and metadata designed to be self-describing and executable.

## Tool Definition Schema (tool-schema.json)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ToolDefinition",
  "type": "object",
  "required": ["id", "name", "description", "apis"],
  "properties": {
    "id": { "type": "string", "pattern": "^[a-z0-9-]+$" },
    "name": { "type": "string" },
    "description": { "type": "string" },
    "version": { "type": "string", "default": "1.0.0" },
    "apis": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/apiEntry"
      }
    },
    "ui": {
      "type": "object",
      "properties": {
        "layout": { "type": "string" },
        "theme": { "type": "string" }
      }
    }
  },
  "definitions": {
    "apiEntry": {
      "type": "object",
      "required": ["id", "method", "path"],
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" },
        "method": { "enum": ["GET", "POST", "PUT", "DELETE"] },
        "path": { "type": "string" },
        "parameters": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["name", "type"],
            "properties": {
              "name": { "type": "string" },
              "type": { "enum": ["string", "number", "boolean", "file"] },
              "required": { "type": "boolean" }
            }
          }
        }
      }
    }
  }
}
```
