# Mem0 integration for OKF RAG pipeline

The OKF RAG pipeline can optionally use **Mem0** as the vector store instead of the default SQLite/FAISS approach. Mem0 provides:

- Server‑side LLM‑driven semantic extraction and deduplication.
- Cross‑session persistence and reranking.
- Platform mode that avoids Qdrant locking issues on the Raspberry Pi 5.

## When to use Mem0
- When you need higher‑quality semantic search across large documentation bundles.
- When you want automatic deduplication of similar concept embeddings.
- When you prefer a managed cloud service over local storage.

## Setup steps
1. **Configure the provider** (once per machine):
   ```bash
   hermes config set memory.provider mem0
   hermes config set mem0.api_key <YOUR_MEM0_KEY>
   ```
2. **Install the Python client** (if not already):
   ```bash
   pip install mem0
   ```
3. **Adjust the RAG pipeline** (`rag/pipeline.py`):
   - Replace the `SQLiteVectorStore` import with `from mem0 import Mem0VectorStore`.
   - Initialise with:
     ```python
     vector_store = Mem0VectorStore(collection="okf_rag")
     ```
   - Remove any `faiss` initialisation; Mem0 handles indexing internally.

4. **Re‑generate embeddings** (will now be stored in Mem0):
   ```bash
   python scripts/generate_embeddings.py
   ```
   The script will detect the `memory.provider` setting and push vectors to Mem0.

5. **Run validation & queries** as usual – the search command will now query Mem0 and return results with confidence scores.

## Pitfalls & gotchas
- **Network latency** – Mem0 queries add a small round‑trip; ensure the Pi 5 has reliable internet.
- **Rate limits** – respect the plan limits; batch embeddings to stay under the request quota.
- **Cost** – Mem0 usage is billed per request; monitor usage via the Mem0 dashboard.

## Verification checklist
- [ ] `hermes config get memory.provider` returns `mem0`.
- [ ] `python scripts/generate_embeddings.py` finishes without errors.
- [ ] `make search QUERY="..."` returns a result with a non‑zero confidence score.
- [ ] `mem0 usage` (or the web dashboard) shows the new vectors.

---

*This reference file is part of the OKF bundle management skill and should be kept up‑to‑date with any changes to the Mem0 API or authentication flow.*