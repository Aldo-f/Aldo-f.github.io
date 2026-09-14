# AGENTS.md — yt-dlp fork

## OVERVIEW

This is a fork of [yt-dlp](https://github.com/yt-dlp/yt-dlp) (~1131 Python source files), a feature-rich command-line audio/video downloader supporting thousands of sites. It is itself a fork of youtube-dl. The CLI is the primary interface; there is no web UI or database.

Python 3.10+ required (CPython). Dependency management uses **uv** (`uv.lock` present). Build uses **hatchling**.

---

## STRUCTURE

```
yt-dlp/                          ← git submodule root (do not re-init)
├── yt_dlp/                      ← main package
│   ├── YoutubeDL.py             ← core download orchestrator
│   ├── extractor/               ← ~942 site extractors (one per file)
│   │   ├── lazy_extractors.py   ← generated, do not edit
│   │   └── _base.py             ← InfoExtractor base class
│   ├── downloader/              ← download backends (native, ffmpeg, aria2c, etc.)
│   ├── postprocessor/           ← FFmpegExtractAudio, Metadata, etc.
│   ├── networking/              ← HTTP client abstraction layer
│   ├── dependencies/            ← optional dep registry
│   └── compat/                  ← Python version compatibility shims
├── devscripts/                  ← build/test/doc helpers
│   ├── run_tests.py             ← test runner
│   ├── make_lazy_extractors.py  ← regens lazy_extractors.py
│   ├── cli_to_api.py            ← CLI → embeddable API translation
│   └── install_deps.py          ← dependency installer
├── test/                        ← pytest suite
├── bundle/                      ← PyInstaller build config
├── pyproject.toml               ← hatch + ruff + pytest config
├── uv.lock                      ← pinned deps
└── Makefile                     ← build targets (make, make yt-dlp, make test)
```

---

## WHERE TO LOOK

| Task | Go here |
|------|---------|
| Add / fix a site extractor | `yt_dlp/extractor/<site>.py` |
| Change download behavior | `yt_dlp/downloader/` or `yt_dlp/YoutubeDL.py` |
| Post-processing (transcode, embed meta) | `yt_dlp/postprocessor/` |
| HTTP / network layer changes | `yt_dlp/networking/` |
| Run tests | `pytest test/` or `make test` |
| Regenerate lazy extractors | `python devscripts/make_lazy_extractors.py` |
| Build source dist | `make pypi-files && python -m build` |
| Build standalone binary | `python -m bundle.pyinstaller` |
| CLI help / option definitions | `yt_dlp/options.py` |

---

## CONVENTIONS

- **Extractor pattern**: each file defines one class ending in `IE`, subclassing `_InfoExtractor`. Class name must match filename (e.g. `YoutubeIE` in `youtube.py`). See `yt_dlp/extractor/_base.py` for the base class contract.
- **Lazy loading**: run `make lazy-extractors` after adding new extractors. Do not commit changes to `lazy_extractors.py` by hand.
- **No external deps without justification**: all dependencies declared in `pyproject.toml` extras. Use `dependencies.Dependency` registry, not bare `import`.
- **Line length**: 120 chars. Ruff is the linter, autopep8 for formatting.
- **String formatting**: use `%`-style (project convention), not f-strings, in extractors.
- **Upstream compatibility**: keep changes backwards-compatible with youtube-dl where feasible. Use `--compat-options` for behavior toggles. Never break existing CLI flags.
- **Tests**: add tests in `test/` alongside any extractor change. Network tests use `test_download.py`; unit tests live in `test_test*.py` files.
- **NO_AI marker**: `yt-dlp/.NO_AI` exists. Do not route AI-generated commits into this subtree without explicit approval.

---

## COMMANDS

```bash
# Install deps (includes default + curl-cffi extras)
uv sync --all-extras

# Run all tests
pytest test/ -n auto

# Run a single extractor test
pytest test/test_download.py -k YouTube

# Regenerate lazy extractors
python devscripts/make_lazy_extractors.py

# Build standalone binary (any platform)
python devscripts/install_deps.py --include-group pyinstaller
python devscripts/make_lazy_extractors.py
python -m bundle.pyinstaller

# Lint / format check
ruff check .
autopep8 --diff .
```
