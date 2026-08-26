---
type: Directory
title: Nextcloud File Sync & Share
description: Documentation for the Nextcloud file synchronization and sharing service in the home-lab
resource: ./05-media-nextcloud/
tags: [media, nextcloud, file-sync, docker]
sources:
  - id: nextcloud-deployment-source
    resource: ./05-media-nextcloud/
    title: Nextcloud Deployment Directory
    author: aldo
    usage_count: 1
    last_modified: 2026-08-25T09:15:00Z
generated:
  by: human:aldo
  at: 2026-08-25T09:15:00Z
verified:
  - by: human:aldo
    at: 2026-08-25T09:15:00Z
status: stable
stale_after: 2027-02-25T09:15:00Z
---

# 05-Media-Nextcloud

This directory contains documentation for the Nextcloud file synchronization and sharing service deployment.

Nextcloud is deployed as a Docker stack with MariaDB, Redis, and Apache containers, providing file storage accessible from the shared HDD1 mount.