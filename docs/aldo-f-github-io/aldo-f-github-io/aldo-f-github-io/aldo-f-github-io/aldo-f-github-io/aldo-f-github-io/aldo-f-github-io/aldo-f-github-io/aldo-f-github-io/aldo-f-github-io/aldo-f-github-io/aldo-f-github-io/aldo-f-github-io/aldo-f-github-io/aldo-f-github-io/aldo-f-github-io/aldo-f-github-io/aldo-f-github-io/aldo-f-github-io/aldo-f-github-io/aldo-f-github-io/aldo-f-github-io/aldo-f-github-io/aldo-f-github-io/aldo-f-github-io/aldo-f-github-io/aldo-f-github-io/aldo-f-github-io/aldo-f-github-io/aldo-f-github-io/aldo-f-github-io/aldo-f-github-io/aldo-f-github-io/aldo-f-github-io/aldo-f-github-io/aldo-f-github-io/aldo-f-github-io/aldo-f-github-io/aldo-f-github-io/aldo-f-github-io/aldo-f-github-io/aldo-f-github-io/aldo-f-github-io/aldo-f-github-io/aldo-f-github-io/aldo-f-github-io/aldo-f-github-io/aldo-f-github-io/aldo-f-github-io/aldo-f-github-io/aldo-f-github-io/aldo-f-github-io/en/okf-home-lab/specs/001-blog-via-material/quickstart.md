# Quickstart: Verify the blog feature end-to-end

Prerequisites: repo venv at `./venv` (or any Python 3 with mkdocs-material
installed). No extra packages needed by the verifier itself.

```bash
cd ~/dev/06-apps-aldo-f-github-io

# Full RED→GREEN verification harness (build + serve + HTTP assertions)
./venv/bin/python tests/verify_blog.py            # or: python3 tests/verify_blog.py

# Manual browsing check
mkdocs serve   # http://localhost:8000/blog/
```

Expected outcomes when GREEN:

1. Script prints one PASS line per check and ends with
   `ALL CHECKS PASSED`; exit code 0.
2. Checks covered, mapped to spec criteria:
   - strict build exit 0 + zero WARNING lines (Constitution I)
   - probe-post appears after being added, count +1 (FR-2/FR-3, SC-2)
   - served routes 200 + body markers for `/`, `/about/`, `/projects/`,
     `/thuis/docs/`, `/blog/`, seed post, category page (SC-3/SC-4)
   - draft post absent from built site (FR-6, SC-5)
   - search index contains distinctive post body token (FR-9)
3. In the browser: Blog visible in nav → listing shows 2 published posts,
   newest first → each post shows prev/next links → categories resolve →
   draft is nowhere.

CI equivalence: pushing `main` runs the same `mkdocs build` via GitHub Actions;
the workflow needs no changes.
