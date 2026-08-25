import subprocess
import sys
import time
from pathlib import Path

import requests

BUNDLE = Path(__file__).resolve().parents[2]
URL = "http://127.0.0.1:8000/search"


def _server_running() -> bool:
    try:
        import urllib.request
        urllib.request.urlopen("http://127.0.0.1:8000/openapi.json", timeout=2)
        return True
    except Exception:
        return False


def test_search_endpoint():
    if not _server_running():
        proc = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "rag_api:app",
             "--host", "127.0.0.1", "--port", "8000"],
            cwd=str(BUNDLE / "rag"),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        for _ in range(60):
            if _server_running():
                break
            time.sleep(1)
        else:
            proc.terminate()
            raise RuntimeError("RAG API did not start within 60s")

    response = requests.post(
        URL, json={"question": "How to enable Jellyfin hardware transcoding?"}, timeout=120
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data and "sources" in data
