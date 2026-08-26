---
type: Node
title: Raspberry Pi 5 (pi5)
description: Raspberry Pi 5 node in the home-lab infrastructure
resource: ./pi5-node.md
tags: [node, raspberry-pi, pi5, hardware, debian]
sources:
  - id: pi5-hardware-specs
    resource: human:aldo
    title: Aldo's Pi5 Hardware Specification
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

# Raspberry Pi 5 (pi5)

## Overview
The Raspberry Pi 5 (pi5) is a single-board computer serving as the primary node in Aldo's home-lab infrastructure.

## Specifications
- Model: Raspberry Pi 5
- Architecture: ARM64
- Operating System: Debian
- IP Address: 192.168.0.5
- Role: Primary node in home-lab cluster
- Connected to: Shared HDD1 storage mount

## Services Hosted
- [To be determined based on actual deployment]

## Relationships
- Paired with: pi3 (192.168.0.3)
- Storage: Shares HDD1 mount with pi3
- Management: Controlled via Ansible from 01-core-infra/