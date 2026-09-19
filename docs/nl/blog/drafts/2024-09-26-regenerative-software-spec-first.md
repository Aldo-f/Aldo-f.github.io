---
title: Spec‑First, Test‑First, Regenerate‑Always
date: 2026-09-20
author: Aldo
tags: [regen, spec, tdd]
---

# Spec‑First, Test‑First, Regenerate‑Always

Dit artikel legt de **5‑stappen workflow** uit die de Phoenix‑Architectuur gebruikt:

1. **Spec** – schrijf een OpenAPI/JSON‑Schema contract.
2. **Regeneratie** – genereer een stub‑implementatie (`make spec`).
3. **Test** – schrijf een falende test die het gewenste gedrag beschrijft.
4. **Iteratie** – pas de spec of de test aan totdat de gegenereerde code slaagt.
5. **CI / Deploy** – laat een GitHub‑Action de pipeline uitvoeren en de site publiceren.

Het hele proces wordt geautomatiseerd; je bewerkt **nooit** handmatig de gegenereerde broncode. Alleen het contract en de tests staan in versiebeheer.

## Voorbeeld‑workflow (commands)

```bash
# 1. Spec schrijven
uv run python -m scripts.write_spec specs/hello.yaml

# 2. Stub genereren
echo "make spec"

# 3. Test schrijven (fails eerst)
uv run pytest -q tests/test_hello.py

# 4. Itereer tot tests slagen
make spec && make test

# 5. CI draait automatisch bij elke push
```

Volgende post behandelt de concrete tooling (OpenAPI‑generator, pytest, ruff, enz.).
