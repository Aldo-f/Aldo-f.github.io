import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "rag"))

import memory_helper
from memory_helper import get_memory_provider


def test_helper_reads_hermes_config(monkeypatch):
    # Real call: hermes config get memory.provider is configured as "mem0"
    provider = get_memory_provider()
    assert provider in {"mem0", "faiss"}


def test_helper_falls_back_on_failure(monkeypatch):
    def boom(*a, **kw):
        raise FileNotFoundError("hermes missing")

    monkeypatch.setattr(memory_helper.subprocess, "run", boom)
    assert get_memory_provider() == "faiss"


@pytest.mark.skipif(
    get_memory_provider() != "mem0", reason="memory.provider is not mem0"
)
def test_mem0_used():
    from rag_query import OKFRAGPipeline
    from mem0_store import Mem0VectorStore

    pipeline = OKFRAGPipeline(bundle_path=str(Path(__file__).resolve().parents[2]))
    assert isinstance(pipeline.vector_store, Mem0VectorStore)

    results = pipeline.query("What is the Jellyfin health-check command?", k=2)
    assert results and "error" not in results[0]
