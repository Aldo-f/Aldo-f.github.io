---
type: Ansible Role
title: Standard Ansible Role Template
description: Template for creating standardized Ansible roles in the home-lab infrastructure
resource: ./ansible-role-template.md
tags: [ansible, role, template, infrastructure]
sources:
  - id: ansible-role-convention
    resource: human:aldo
    title: Aldo's Ansible Role Convention
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

# Standard Ansible Role Template

## Overview
This document describes the standard structure and conventions for Ansible roles used in Aldo's home-lab infrastructure.

## Role Structure
```
role_name/
├── defaults/
│   └── main.yml          # Default variables
├── files/                # Static files to copy
├── handlers/
│   └── main.yml          # Handlers
├── meta/
│   └── main.yml          # Role metadata
├── README.md             # Role documentation
├── tasks/
│   └── main.yml          # Main tasks
├── templates/            # Jinja2 templates
├── tests/
│   ├── inventory         # Test inventory
│   └── test.yml          # Test playbook
└── vars/
    └── main.yml          # Other variables
```

## Conventions
1. **Naming**: Use lowercase with underscores (e.g., `docker_service`, `firewall_config`)
2. **Documentation**: Every role must have a README.md with usage instructions
3. **Variables**: 
   - Define sensible defaults in `defaults/main.yml`
   - Allow overrides via host/group vars or extra vars
   - Use descriptive variable names with clear prefixes
4. **Templates**: Store Jinja2 templates in the `templates/` directory
5. **Handlers**: Use handlers for service restarts and reloads
6. **Meta**: Include appropriate galaxy info and dependencies

## Best Practices
- Keep roles focused on a single concern
- Use blocks for error handling when appropriate
- Tag tasks for selective execution
- Validate inputs when possible
- Use become: true only when necessary