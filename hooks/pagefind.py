import os
from pathlib import Path

def on_post_build(config):
    site_dir = Path(config.site_dir).resolve()
    hooks_dir = Path(__file__).parent.resolve()
    # Copy the pagefind-init.js to site/js/pagefind-init.js
    src_js = hooks_dir / 'pagefind-init.js'
    dst_js = site_dir / 'js' / 'pagefind-init.js'
    dst_js.parent.mkdir(parents=True, exist_ok=True)
    dst_js.write_bytes(src_js.read_bytes())
    print(f"Copied {src_js} to {dst_js}")
    return config