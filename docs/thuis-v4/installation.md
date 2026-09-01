---
sidebar_position: 2
---

# Installation

## Requirements

- Python 3.8 or newer
- git
- A VRT MAX account (free or paid)

## Steps

Open a terminal and run:

```bash
# Clone the repository
git clone https://github.com/Aldo-f/thuis.git
cd thuis

# Create a virtual environment (recommended)
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

This installs a [patched version of yt-dlp](https://github.com/Aldo-f/yt-dlp) (tag `v2026.06.09-patch1`) that can handle VRT MAX's login flow.

### Using `uv` (recommended)

```bash
# Create virtual environment with hardlink mode (disk efficient)
uv venv --link-mode=hardlink

# Install dependencies
uv pip install -r requirements.txt --python .venv/bin/python
```

### Using `pip`

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Verify the installation

```bash
.venv/bin/yt-dlp --version
```

You should see:

```
2026.06.09
```
