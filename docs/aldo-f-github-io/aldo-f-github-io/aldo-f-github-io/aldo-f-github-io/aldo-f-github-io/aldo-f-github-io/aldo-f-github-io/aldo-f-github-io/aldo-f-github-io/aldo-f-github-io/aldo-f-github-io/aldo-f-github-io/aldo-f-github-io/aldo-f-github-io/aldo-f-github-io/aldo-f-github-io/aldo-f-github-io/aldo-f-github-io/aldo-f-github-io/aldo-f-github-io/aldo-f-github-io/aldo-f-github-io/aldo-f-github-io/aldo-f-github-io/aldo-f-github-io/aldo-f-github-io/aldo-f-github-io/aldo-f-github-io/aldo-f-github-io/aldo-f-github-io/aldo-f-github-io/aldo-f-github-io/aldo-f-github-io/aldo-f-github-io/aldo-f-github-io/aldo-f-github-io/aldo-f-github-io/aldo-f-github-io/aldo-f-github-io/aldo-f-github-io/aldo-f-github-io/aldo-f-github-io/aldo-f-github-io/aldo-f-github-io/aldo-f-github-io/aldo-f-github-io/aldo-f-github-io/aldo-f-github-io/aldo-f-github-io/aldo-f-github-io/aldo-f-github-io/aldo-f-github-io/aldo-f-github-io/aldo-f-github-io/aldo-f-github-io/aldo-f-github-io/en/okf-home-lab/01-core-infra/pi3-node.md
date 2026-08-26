---
type: Node
title: Raspberry Pi 3 (pi3)
description: Raspberry Pi 3 Model B+ node in the home-lab infrastructure
resource: ./pi3-node.md
tags: [node, raspberry-pi, pi3, hardware, debian]
sources:
  - id: pi3-hardware-specs
    resource: human:aldo
    title: Aldo's Pi3 Hardware Specification
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

# Raspberry Pi 3 (pi3)

## Overview
The Raspberry Pi 3 (pi3) is a single-board computer serving as one of the two nodes in Aldo's home-lab infrastructure.

## Specifications
- Model: Raspberry Pi 3 Model B+
- Architecture: ARM64
- Operating System: Debian
- IP Address: 192.168.0.3
- Role: Secondary node in home-lab cluster
- Connected to: Shared HDD1 storage mount

## Services Hosted
- [To be determined based on actual deployment]

## Relationships
- Paired with: pi5 (192.168.0.5)
- Storage: Shares HDD1 mount with pi5
- Management: Controlled via Ansible from 01-core-infra/