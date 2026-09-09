# Plan to fix GitHub Actions deployment error

## Goal
Fix the GitHub Actions deployment failure by installing missing dependencies and fixing the mkdocs_raw_markdown plugin to work with multirepo imports.

## Current context / assumptions
- The deploy workflow fails because the mkdocs_pivot_table plugin is not installed (missing from requirements.txt).
- The mkdocs_raw_markdown plugin throws "source not found" errors when trying to read source files from multirepo imports (e.g., thuis, vaultwarden-backup).
- The repository uses a venv for local development, and GitHub Actions installs dependencies from requirements.txt.
- The mkdocs_raw_markdown plugin is located at plugins/mkdocs_raw_markdown/ and has a pyproject.toml suitable for editable installation.
- The mkdocs_pivot_table plugin is located at plugins/mkdocs_pivot_table/ and has a pyproject.toml suitable for editable installation.

## Architecture / proposed approach
1. Update requirements.txt to install both local plugins in editable mode (`-e ./plugins/<plugin>`).
2. Modify the mkdocs_raw_markdown plugin to:
   - During `on_files`, store a mapping from each virtual file's src_path to the original file's absolute source path (`abs_src_path`).
   - During `on_page_read_source`, if the page is a virtual file (src_path ends with the configured suffix), look up the original path from the mapping and read its content.
   - If the original path is not available (e.g., for local files), fall back to constructing the path from the docs_dir.
3. Verify the fix with a local build (non-strict and strict) before pushing to trigger GitHub Actions.

## Step-by-step tasks

### Task 1: Update requirements.txt to install local plugins
Edit `/home/aldo/dev/06-apps-aldo-f-github-io/requirements.txt` to include the two plugins as editable installs.

```diff
 mkdocs
 mkdocs-material
 mkdocs-multirepo-plugin
 mkdocs-section-index
 mkdocs-autotranslate
 mkdocs-mermaid2-plugin
 pagefind
+-e ./plugins/mkdocs_pivot_table
+-e ./plugins/mkdocs_raw_markdown
```

Verification:
```bash
source /home/aldo/dev/06-apps-aldo-f-github-io/venv/bin/activate
pip install -r requirements.txt
```
Expected output: Successfully installed mkdocs-pivot-table and mkdocs-raw-markdown (shown in the install log).

### Task 2: Fix the mkdocs_raw_markdown plugin
Replace the content of `/home/aldo/dev/06-apps-aldo-f-github-io/plugins/mkdocs_raw_markdown/mkdocs_raw_markdown/plugin.py` with the following:

```python
import logging
import os
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
from mkdocs.structure.files import File

log = logging.getLogger("mkdocs.plugins")

class RawMarkdownPlugin(BasePlugin):
    config_scheme = (("suffix", config_options.Type(str, default=".md")),)

    def on_files(self, files, config):
        """Add virtual .md files for each markdown page."""
        suffix = self.config["suffix"]
        self._virtual_files = {}  # Maps virtual src_path to original abs_src_path
        for file in files:
            # Only process markdown source files
            if file.src_path.endswith(".md"):
                # Create virtual path with suffix (e.g., "index.md" -> "index.md.md")
                virtual_path = file.src_path + suffix
                # Store the original file's absolute source path
                self._virtual_files[virtual_path] = file.abs_src_path

                # Create new File with virtual path
                new_file = File(
                    virtual_path,
                    file.src_dir,
                    file.dest_dir,
                    file.use_directory_urls,
                )
                files.append(new_file)
        return files

    def on_page_read_source(self, page, config):
        """Serve raw markdown content for virtual .md files."""
        suffix = self.config["suffix"]
        src_path = page.file.src_path
        if src_path.endswith(suffix):
            # This is a virtual file, look up the original file's abs_src_path
            abs_src_path = self._virtual_files.get(src_path)
            if abs_src_path and os.path.isfile(abs_src_path):
                try:
                    with open(abs_src_path, "r", encoding="utf-8") as f:
                        return f.read()
                except Exception as e:
                    log.error(f"RawMarkdownPlugin: error reading {abs_src_path}: {e}")
                    return ""
            else:
                # Fallback: try to construct the path from the virtual path (for local files)
                # Remove the suffix to get the base path
                base_path = src_path[: -len(suffix)]
                # If the base path doesn't end with .md, it's a virtual file
                if not base_path.endswith(".md"):
                    # Construct the real source path by adding .md
                    real_path = os.path.join(config["docs_dir"], base_path + ".md")
                    try:
                        with open(real_path, "r", encoding="utf-8") as f:
                            return f.read()
                    except FileNotFoundError:
                        log.error(f"RawMarkdownPlugin: source not found: {real_path}")
                        return ""
                    except Exception as e:
                        log.error(f"RawMarkdownPlugin: error reading {real_path}: {e}")
                        return ""
        return None
```

Verification:
```bash
source /home/aldo/dev/06-apps-aldo-f-github-io/venv/bin/activate
mkdocs build -f mkdocs.en.yml -d site 2>&1 | grep -i "error\|warning" | head -20
```
Expected output: No errors related to "source not found" or "mkdocs_pivot_table not installed". Warnings about MkDocs 2.0 are expected and can be ignored.

### Task 3: Verify the fix with a strict build
```bash
source /home/aldo/dev/06-apps-aldo-f-github-io/venv/bin/activate
mkdocs build --strict -f mkdocs.en.yml -d site-strict 2>&1 | grep -i "error\|warning" | head -20
```
Expected output: No errors (the build should succeed or fail only for unrelated reasons).

Repeat for the NL build:
```bash
mkdocs build --strict -f mkdocs.nl.yml -d site-nl 2>&1 | grep -i "error\|warning" | head -20
```

After local verification, commit and push to trigger GitHub Actions:
```bash
git add requirements.txt plugins/mkdocs_raw_markdown/mkdocs_raw_markdown/plugin.py
git commit -m "Fix GitHub Actions: install missing plugins and fix raw markdown plugin for multirepo"
git push
```

## Tests / validation
- Task 1: Verify plugins are installed via pip list or by attempting to import them in a Python shell.
- Task 2: Verify no plugin-related errors appear in local build logs.
- Task 3: Verify strict builds complete without errors (except expected MkDocs 2.0 warnings).
- Final validation: GitHub Actions workflow for deploy completes successfully.

## Risks, tradeoffs, and open questions
- Risk: The plugin fix assumes that `file.abs_src_path` is set and valid during `on_files` for all markdown files (including multirepo imports). This is true because the multirepo plugin sets `abs_src_path` to the cloned repo's file path.
- Tradeoff: The fallback to local file system (`docs_dir`) is only needed for local files; multirepo files should be handled by the `abs_src_path` lookup.
- Open question: If the plugin is used in a context where `abs_src_path` is not set (unlikely with multirepo), the fallback may produce incorrect results. However, the plugin is only used in this repository with known multirepo configuration.
- Risk: Editable installation of plugins in GitHub Actions may fail if the plugins have unmet dependencies. We rely on the fact that the dependencies (mkdocs, beautifulsoup4) are already installed via requirements.txt or transitive dependencies.