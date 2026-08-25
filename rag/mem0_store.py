#!/usr/bin/env python3
"""
Mem0 Platform vector store for the OKF RAG pipeline.

The plan's `Mem0VectorStore` symbol does not exist in the mem0ai SDK, so this
module provides the equivalent: a thin client over the Mem0 Platform REST API
(api.mem0.ai) that supports search and add. It reads MEM0_API_KEY from the
environment (or ~/.hermes/.env) and scopes all memories to user_id="okf_rag".
"""
import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional

API_BASE = "https://api.mem0.ai"


def _load_api_key() -> Optional[str]:
    key = os.environ.get("MEM0_API_KEY")
    if key:
        return key.strip()
    env_file = Path.home() / ".hermes" / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line.startswith("MEM0_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


class Mem0VectorStore:
    """Minimal Mem0 Platform client with FAISS-like search semantics."""

    def __init__(self, collection: str = "okf_rag", api_key: Optional[str] = None):
        self.collection = collection
        # Mem0 Platform scopes by user_id; use the collection name as the scope.
        self.user_id = collection
        self.api_key = api_key or _load_api_key()
        if not self.api_key:
            raise RuntimeError(
                "MEM0_API_KEY not found in environment or ~/.hermes/.env"
            )

    def _post(self, path: str, payload: dict, timeout: int = 30):
        req = urllib.request.Request(
            API_BASE + path,
            data=json.dumps(payload).encode(),
            headers={
                "Authorization": f"Token {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"Mem0 API error {e.code}: {e.read().decode()}") from e

    def add(self, texts: List[str], metadatas: Optional[List[Dict]] = None):
        """Index documents. Returns list of per-item results."""
        metadatas = metadatas or [{} for _ in texts]
        results = []
        for text, meta in zip(texts, metadatas):
            payload = {
                "messages": [{"role": "user", "content": text}],
                "user_id": self.user_id,
                "metadata": meta,
                "version": "v2",
            }
            results.append(self._post("/v1/memories/", payload))
        return results

    def search(self, query: str, limit: int = 3) -> List[Dict]:
        """Semantic search; returns hits with memory/score/metadata fields."""
        payload = {
            "query": query,
            "filters": {"AND": [{"user_id": self.user_id}]},
            "limit": limit,
        }
        return self._post("/v2/memories/search/", payload)
