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
    
    # Check if pagefind is configured in plugins and create proper pagefind index structure
    if 'search' in config.plugins:
        # Ensure pagefind directory exists
        pagefind_dir = site_dir / 'pagefind'
        pagefind_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created {pagefind_dir} for Pagefind search index")
    
    return config