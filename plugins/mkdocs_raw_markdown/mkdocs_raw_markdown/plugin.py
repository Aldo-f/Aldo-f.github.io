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
        for file in list(files):
            # Only process markdown source files (skip blog directory which has its own plugin)
            if file.src_path.endswith(".md") and not file.src_path.startswith(
                "blog/posts/"
            ):
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
