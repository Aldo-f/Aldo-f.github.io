# Home-lab Documentation

This hub documents Aldo's home-lab: infrastructure, media services and
self-hosted applications.

## What you'll find here

| Section | Content |
|---------|---------|
| Thuis (v3/v4/v5/main) | VRT MAX video downloader — install, usage, troubleshooting |
| Clocky | React clock studio — features and development |
| Blanky | Project docs, main and v1 |
| Radio Community | Democratic internet radio — architecture, API, streaming |
| Passive Income (PINO) | Orchestrator for passive-income providers |
| Neo-Brutalist Home | Dashboard design exploration |

Documentation for each project lives in its own section (see the navigation)
and is pulled straight from that project's repository at build time, so it
always matches the code.

## For AI agents

Agent-readable structured knowledge (OKF format) and a local retrieval
pipeline (RAG) are maintained separately and queried locally on the host.

### How it works

The OKF (Open Knowledge Format) bundle at `~/dev/okf-home-lab/` contains
structured markdown documentation about the home-lab infrastructure. A RAG
(Retrieval-Augmented Generation) pipeline indexes this knowledge and allows
natural-language queries.

**Pipeline flow:**
1. All markdown files in concept folders (`01-*`, `05-*`, `06-*`) plus
   `index.md` and `log.md` are loaded
2. Text is embedded using `sentence-transformers/all-MiniLM-L6-v2`
3. Vectors are stored in either FAISS (local) or Mem0 Platform (cloud)
4. Queries are embedded and searched for top-k relevant documents
5. The best-match snippet is returned as the answer with relevance score

### File locations

| Path | Purpose |
|------|---------|
| `~/dev/okf-home-lab/rag/rag_query.py` | Core RAG pipeline (`OKFRAGPipeline` class) |
| `~/dev/okf-home-lab/rag/rag_api.py` | FastAPI wrapper (port 8000) |
| `~/dev/okf-home-lab/rag/mem0_store.py` | Mem0 Platform vector store client |
| `~/dev/okf-home-lab/rag/memory_helper.py` | Reads `hermes config get memory.provider` |
| `~/dev/okf-home-lab/rag/README.md` | Full RAG documentation |
| `~/dev/okf-home-lab/rag/requirements.txt` | Python dependencies |

### Commands for agents

**Query via Python (direct):**
```python
from rag_query import OKFRAGPipeline
pipeline = OKFRAGPipeline('~/dev/okf-home-lab')
result = pipeline.query_with_answer('What is the Jellyfin health-check command?')
print(result['answer'])        # Snippet from most relevant doc
print(result['confidence'])    # 0.0-1.0 relevance score
print(result['sources'])       # List of {title, path, relevance}
```

**Query via CLI:**
```bash
cd ~/dev/okf-home-lab
python3 rag/rag_query.py "What is the Jellyfin health-check command?"
python3 rag/rag_query.py "How to deploy Traefik?" --k 5
```

**Query via HTTP API:**
```bash
# Start the API server
./scripts/run_rag_api.sh

# Query it
curl -s -X POST http://127.0.0.1:8000/search \
  -H 'Content-Type: application/json' \
  -d '{"question": "What is the Jellyfin health-check command?", "k": 3}'
```

**Switch vector store provider:**
```bash
hermes config set memory.provider mem0    # Use Mem0 Platform (requires MEM0_API_KEY)
hermes config set memory.provider faiss   # Use local FAISS (default)
```

### What agents should do

When you need information about the home-lab infrastructure:

1. **Query the RAG pipeline** instead of searching files manually — it returns
   relevant snippets with confidence scores
2. **Cite sources** — the `sources` field contains the original doc path, so
   you can reference where the answer came from
3. **Use the API when possible** — the FastAPI endpoint is faster for multiple
   queries than re-initializing the pipeline each time
4. **Check confidence** — if `confidence < 0.5`, the answer may be unreliable;
   fall back to reading the source docs directly

### Indexing behavior

- New markdown files in concept folders are picked up automatically on next run
- Re-indexing is cached via content hash (`.mem0_index_hash`) to avoid
  unnecessary work when the bundle hasn't changed
- The watcher at `~/dev/okf-home-lab/documentation_watcher/watcher.py` monitors
  source repos and syncs changes into the bundle

### Troubleshooting

| Issue | Solution |
|-------|----------|
| `MEM0_API_KEY not found` | Add `MEM0_API_KEY=...` to `~/.hermes/.env` or export it |
| "Index not built" | Ensure you're running from the OKF bundle root |
| Slow first query | First run builds the index; subsequent queries are fast |
