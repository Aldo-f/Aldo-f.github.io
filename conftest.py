import subprocess, sys, os, time, urllib.request, shutil
import pytest


@pytest.fixture(scope="session", autouse=True)
def start_http_server():
    """Start a simple HTTP server on port 8000 serving the built site."""
    site_dir = os.path.join(os.path.dirname(__file__), "site")
    # Start server
    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "http.server",
            "8000",
            "--directory",
            site_dir,
            "--bind",
            "127.0.0.1",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    # Wait for server ready
    for _ in range(20):
        try:
            with urllib.request.urlopen(
                "http://127.0.0.1:8000/404.html", timeout=1
            ) as resp:
                if resp.status == 200:
                    break
        except Exception:
            time.sleep(0.5)
    else:
        pytest.fail("HTTP server failed to start")
    yield
    proc.terminate()
    proc.wait()
