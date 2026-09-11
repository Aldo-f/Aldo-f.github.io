# Spec 005 — Chat RAG integration

Status: IN PROGRESS (endpoint public, chat widget needs build-time key injection + search box)
Endpoint: https://rag.aldof.duckdns.org/search (CORS open for aldo-f.github.io)
Key: RAG_API_KEY (aido_rag_...) stored in okf-home-lab/.env, must NOT appear in client JS
Next: Add GitHub Actions secret, modify hooks/chat.py for build-time injection, build both languages
