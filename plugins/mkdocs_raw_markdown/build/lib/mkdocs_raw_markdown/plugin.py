import logging
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
from mkdocs.structure.files import File

log = logging.getLogger("mkdocs.plugins")


class RawMarkdownPlugin(BasePlugin):
    config_scheme = (
        ("suffix", config_options.Type(str, default=".md")),
        ("cache_seconds", config_options.Type(int, default=0)),
    )

    def on_files(self, files, config):
        # Register a virtual file for each page that ends with the suffix.
        suffix = self.config["suffix"]
        new_files = []
        docs_dir = config["docs_dir"]
        for file in files:
            if file.src_path.endswith(".md"):
                # original markdown already exists; we add a virtual .md URL.
                virtual_path = file.src_path + suffix
                # File(path, src_dir, dest_dir, use_directory_urls)
                new_file = File(
                    virtual_path,
                    docs_dir,
                    file.dest_dir,
                    file.use_directory_urls,
                    dest_uri=None,
                )
                new_files.append(new_file)
        files.extend(new_files)
        return files

    def on_page_read_source(self, page, config):
        # When a request matches the virtual .md suffix, serve raw source.
        suffix = self.config["suffix"]
        if page.file.src_path.endswith(suffix):
            # map back to original markdown file
            original_path = page.file.src_path[: -len(suffix)]
            docs_dir = config["docs_dir"]
            src_file = docs_dir + "/" + original_path
            try:
                with open(src_file, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                log.error(f"RawMarkdownPlugin: cannot read {src_file}: {e}")
                return ""
        return None
