#!/usr/bin/env bash
set -euo pipefail

# Build the site
rm -rf docs/temp_dir site/
./venv/bin/mkdocs build -f mkdocs.en.yml >/dev/null 2>&1

# Verify blanky assets exist
test -f site/assets/javascripts/blanky.umd.js
test -f site/assets/javascripts/blanky-init.js

# Verify HTML references both scripts
grep -q 'blanky.umd.js' site/index.html
grep -q 'blanky-init.js' site/index.html

# Verify init script calls window.blanky.blanky
grep -q 'window.blanky.blanky' site/assets/javascripts/blanky-init.js

echo "blanky integration OK"
