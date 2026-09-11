import subprocess
import sys
import time
from pathlib import Path

import requests

BUNDLE = Path(__file__).resolve().parents[2] / ".." / "02-ai-okf-home-lab"
BUNDLE = BUNDLE.resolve()
# Maintain backward compatibility: if .env / rag folder missing, fall back to repo root
if not (BUNDLE / ".env").exists():
    BUNDLE = Path(__file__).resolve().parents[2]
URL = "http://127.0.0.1:8000/search"


def _load_api_key():
    """Load RAG_API_KEY from the OKF RAG .env file."""
    env_path = BUNDLE / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if line.startswith("RAG_API_KEY="):
                return line.split("=", 1)[1]
    return None


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
            [
                sys.executable,
                "-m",
                "uvicorn",
                "rag_api:app",
                "--host",
                "127.0.0.1",
                "--port",
                "8000",
            ],
            cwd=str(BUNDLE / "rag"),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        for _ in range(60):
            if _server_running():
                break
            time.sleep(1)
        else:
            proc.terminate()
            raise RuntimeError("RAG API did not start within 60s")

    response = requests.post(
        URL,
        json={"question": "How to enable Jellyfin hardware transcoding?"},
        headers={"X-API-Key": _load_api_key() or ""},
        timeout=120,
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data and "sources" in data
