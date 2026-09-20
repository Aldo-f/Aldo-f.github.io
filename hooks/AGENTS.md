# PROJECT KNOWLEDGE BASE – hooks

**Generated:** 2026-09-20

## OVERVIEW
Build‑time hook scripts that augment MkDocs generation (slugmap, custom markdown handling, etc.).

## STRUCTURE
```
06-apps-aldo-f-github-io/
└── hooks/
    ├── slugmap.py          # Generates slugmap.json & language‑switch interceptor
    └── other_hook.py       # Additional build‑time utilities (placeholder)
```

## WHERE TO LOOK
| File | Purpose |
|------|---------|
| `slugmap.py` | Emits `slugmap.json` for language‑aware navigation |
| `other_hook.py` | Placeholder for future hooks |

## CONVENTIONS
- Hooks are pure Python scripts invoked by `mkdocs` via the `plugins` configuration.
- No side‑effects outside the build directory.

## ANTI‑PATTERNS (THIS PROJECT)
- Do not commit generated `slugmap.json` – it is recreated on each build.

## COMMANDS
```bash
# Run hooks via MkDocs build (automatically invoked)
mkdocs build -f mkdocs.en.yml
```
