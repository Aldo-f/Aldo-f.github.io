import logging
import os
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
from mkdocs.structure.files import File

log = logging.getLogger("mkdocs.plugins")


class RawMarkdownPlugin(BasePlugin):
    config_scheme = (
        ("suffix", config_options.Type(str, default=".md")),
    )

    def on_files(self, files, config):
        """Add virtual .md files for each markdown page."""
        suffix = self.config["suffix"]
        docs_dir = config["docs_dir"]
        new_files = []

        for file in files:
            # Only process markdown source files
            if file.src_path.endswith(".md"):
                # Create virtual path with suffix (e.g., "page" -> "page.md")
                base_path = file.src_path[:-3]  # Remove existing .md
                virtual_path = base_path + suffix

                # Create new File with virtual path
                new_file = File(
                    virtual_path,
                    docs_dir,
                    file.dest_dir,
                    file.use_directory_urls,
                )
                new_files.append(new_file)

        # Add virtual files to collection
        for nf in new_files:
            files.append(nf)

        return files

    def on_page_read_source(self, page, config):
        """Serve raw markdown content for virtual .md files."""
        suffix = self.config["suffix"]
        docs_dir = config["docs_dir"]

        # Check if this is a virtual .md file (path ends with suffix but isn't a real .md)
        src_path = page.file.src_path
        if src_path.endswith(suffix):
            # Remove suffix to get the base path
            base_path = src_path[: -len(suffix)]
            # If base path doesn't end with .md, it's a virtual file
            if not base_path.endswith(".md"):
                # Construct the real source path
                real_path = os.path.join(docs_dir, base_path + ".md")
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
