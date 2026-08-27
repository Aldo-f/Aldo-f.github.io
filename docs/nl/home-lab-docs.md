# Home-lab Documentatie

Deze hub documenteert Aldo's home-lab: infrastructuur, mediaservices en
zelf-gehoste applicaties.

## Wat je hier vindt

| Sectie | Inhoud |
|--------|--------|
| Thuis (v3/v4/v5/main) | VRT MAX video-downloader — installatie, gebruik, probleemoplossing |
| Clocky | React klokstudio — features en ontwikkeling |
| Blanky | Projectdocumentatie, main en v1 |
| Radio Community | Democratische internetradio — architectuur, API, streaming |
| Passive Income (PINO) | Orchestrator voor passive-income providers |
| Neo-Brutalist Home | Dashboard design-exploratie |

De documentatie van elk project staat in een eigen sectie (zie de navigatie)
en wordt bij het bouwen van de site rechtstreeks uit de repository van dat
project gehaald — zo klopt hij altijd met de code.

## Voor AI-agents

Machineleesbare gestructureerde kennis (OKF-formaat) en een lokale
retrieval-pipeline (RAG) worden apart bijgehouden en lokaal op de host
gequery'd.

### Hoe het werkt

Het OKF (Open Knowledge Format) bundle op `~/dev/okf-home-lab/` bevat
gestructureerde markdown-documentatie over de home-lab infrastructuur. Een RAG
(Retrieval-Augmented Generation) pipeline indexeert deze kennis en stelt
natuurlijke-taal queries mogelijk.

**Pipeline flow:**
1. Alle markdown bestanden in concept-mappen (`01-*`, `05-*`, `06-*`) plus
   `index.md` en `log.md` worden geladen
2. Tekst wordt geëmbedd met `sentence-transformers/all-MiniLM-L6-v2`
3. Vectoren worden opgeslagen in FAISS (lokaal) of Mem0 Platform (cloud)
4. Queries worden geëmbed en doorzocht voor top-k relevante documenten
5. De best-matching snippet wordt teruggegeven als antwoord met relevantiescore

### Bestandslocaties

| Pad | Doel |
|-----|------|
| `~/dev/okf-home-lab/rag/rag_query.py` | Core RAG pipeline (`OKFRAGPipeline` klasse) |
| `~/dev/okf-home-lab/rag/rag_api.py` | FastAPI wrapper (poort 8000) |
| `~/dev/okf-home-lab/rag/mem0_store.py` | Mem0 Platform vector store client |
| `~/dev/okf-home-lab/rag/memory_helper.py` | Leest `hermes config get memory.provider` |
| `~/dev/okf-home-lab/rag/README.md` | Volledige RAG documentatie |
| `~/dev/okf-home-lab/rag/requirements.txt` | Python afhankelijkheden |

### Commando's voor agents

**Query via Python (direct):**
```python
from rag_query import OKFRAGPipeline
pipeline = OKFRAGPipeline('~/dev/okf-home-lab')
result = pipeline.query_with_answer('Wat is het Jellyfin health-check commando?')
print(result['answer'])        # Snippet van meest relevante doc
print(result['confidence'])    # 0.0-1.0 relevantiescore
print(result['sources'])       # Lijst van {title, path, relevance}
```

**Query via CLI:**
```bash
cd ~/dev/okf-home-lab
python3 rag/rag_query.py "Wat is het Jellyfin health-check commando?"
python3 rag/rag_query.py "Hoe deploy je Traefik?" --k 5
```

**Query via HTTP API:**
```bash
# Start de API server
./scripts/run_rag_api.sh

# Query de API
curl -s -X POST http://127.0.0.1:8000/search \
  -H 'Content-Type: application/json' \
  -d '{"question": "Wat is het Jellyfin health-check commando?", "k": 3}'
```

**Vector store provider wisselen:**
```bash
hermes config set memory.provider mem0    # Gebruik Mem0 Platform (vereist MEM0_API_KEY)
hermes config set memory.provider faiss   # Gebruik lokale FAISS (standaard)
```

### Wat agents moeten doen

Wanneer je informatie nodig hebt over de home-lab infrastructuur:

1. **Query de RAG pipeline** in plaats van handmatig bestanden te doorzoeken —
   het retourneert relevante snippets met confidence scores
2. **Citeer bronnen** — het `sources` veld bevat het oorspronkelijke doc pad,
   zodat je kunt verwijzen naar waar het antwoord vandaan komt
3. **Gebruik de API wanneer mogelijk** — het FastAPI endpoint is sneller voor
   meerdere queries dan de pipeline elke keer opnieuw te initialiseren
4. **Controleer confidence** — als `confidence < 0.5` kan het antwoord onbetrouwbaar
   zijn; val terug op het direct lezen van de brondocumenten

### Indexering gedrag

- Nieuwe markdown bestanden in concept-mappen worden automatisch meegenomen
  bij de volgende run
- Re-indexering is gecached via content hash (`.mem0_index_hash`) om onnodig
  werk te vermijden wanneer het bundle niet is veranderd
- De watcher op `~/dev/okf-home-lab/documentation_watcher/watcher.py` monitort
  source repos en synchroniseert wijzigingen naar het bundle

### Probleemoplossing

| Probleem | Oplossing |
|----------|-----------|
| `MEM0_API_KEY not found` | Voeg `MEM0_API_KEY=...` toe aan `~/.hermes/.env` of export het |
| "Index not built" | Zorg dat je vanuit de OKF bundle root draait |
| Langzame eerste query | Eerste run bouwt de index; daaropvolgende queries zijn snel |
