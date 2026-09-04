## Multirepo fix (2026-09-04, session)

Repo: `Aldo-f/Aldo-f.github.io`
Bug: `mkdocs.en.yml` nav pointed to `opencode-multi-model-fallback/docs/index.md` but `nav_repos` had no import entry.

Fix applied to `mkdocs.en.yml` (line 50-53):
```yaml
- name: opencode-multi-model-fallback
  import_url: https://github.com/Aldo-f/opencode-multi-model-fallback?branch=main
  imports:
    - docs
```

Also had to restore accidentally-removed `blanky-v1` import and `nav:` header (patch failure recovery).

Deploy verified with `gh run list` — `completed success` (52s, no warnings, strict mode passed).
Live site: `https://aldo-f.github.io/projects/` shows OpenCode section.

Ctrl+K shortcut added to `hooks/pagefind-init.js`; `pagefind.js` serves 200.
