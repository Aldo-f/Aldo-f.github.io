---
title: "JS & Python Package Managers Compared: npm, pnpm, Bun, pip, uv"
date: 2026-09-07
tags: [tooling, javascript, python]
---

Choosing the right package manager isn't just about convenience—it's about disk space, install speed, and reproducible builds. The wrong choice can bloat your project with duplicate files, while the right one keeps your workspace lean and your CI pipelines humming.

## Quick comparison

| Tool | Ecosystem | Global store / cache location | Linking mechanism | Fallback method if linking unsupported | Lockfile support | Install speed | Also acts as runtime? | Maturity / ecosystem stability |
|------|-----------|------------------------------|-------------------|--------------------------------------|-------------------|---------------|------------------------|--------------------------------|
| npm | JS/TS | `~/.npm` | Copy | No fallback | yes (`package-lock.json`) | Slow | No | High |
| pnpm | JS/TS | `~/.pnpm-store` | Hard link | Copy | yes (`pnpm-lock.yaml`) | Fast | No | High |
| Bun | JS/TS | `~/.bun/bin/cache` | Hard link | Copy | yes (`bun.lockb`) | Fastest | Yes | Medium |
| pip | Python | `~/.cache/pip` | Copy | No fallback | yes (`requirements.txt`, `pyproject.toml`) | Slow | No | High |
| uv | Python | `~/.uv/cache` | Hard link or reflink | Copy | yes (`uv.lock`) | Fast | No | Medium |

## Install flow diagrams

### npm install flow
```mermaid
flowchart TD
    A[registry] --> B[download]
    B --> C[node_modules]
    C -.-> D[(project copy)]
    D --> C
```

### pnpm install flow
```mermaid
flowchart TD
    A[global store] --> B[hard link]
    B --> C[.pnpm virtual store]
    C --> D[symlink]
    D --> E[node_modules]
    E --> F[(project link)]
```

### Bun install flow
```mermaid
flowchart TD
    A[global cache] --> B[hard link]
    B -.-> C[(copy fallback)]
    C --> D[node_modules]
```

### pip install flow
```mermaid
flowchart TD
    A[PyPI] --> B[download]
    B --> C[venv site-packages]
    C -.-> D[(project copy)]
```

### uv install flow
```mermaid
flowchart TD
    A[global cache] --> B[hard link or reflink]
    B -.-> C[(copy fallback)]
    C --> D[venv site-packages]
```

## Which one avoids duplicate files on disk?

npm and pip copy packages per project, so installing the same library across multiple projects stores it multiple times on disk. pnpm, Bun, and uv all link from a shared global store/cache, giving you automatic deduplication.

## The bottom line

When you install the same package version across 10 projects, pnpm/Bun/uv only store it once on disk, while npm/pip store it 10 times. That means you save disk space and reduce CI build times—simple as that.
