---
title: How this documentation hub is built
date: 2026-08-20
categories:
  - Meta
---

The hub you are reading aggregates documentation from several repositories at
build time. A MkDocs configuration lists each project repository and branch,
and during every build the docs folders of those repositories are pulled in
and merged into one navigable site under a single explicit table of contents.

This approach keeps each project's documentation next to its code while still
offering one entry point for readers. The build pipeline itself is plain
continuous integration: install the pinned requirements, run a strict build,
publish the static output. No database, no server-side rendering, no
quokka-buildkit style magic — just deterministic tooling that anyone can rerun
locally with two commands.
