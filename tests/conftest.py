import subprocess, sys, os, time, urllib.request, socket
import pytest


@pytest.fixture(scope="session", autouse=True)
def start_http_server():
    """Start a simple HTTP server on port 8000 serving the built site."""
    import subprocess, sys, os, time, urllib.request
    site_dir = os.path.join(os.path.dirname(__file__), "..", "site")
    site_dir = os.path.abspath(site_dir)
    
    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "http.server",
            "8000",
            "--bind",
            "127.0.0.1",
            "--directory",
            site_dir,
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
        proc.terminate()
        pytest.fail(f"HTTP server failed to start on port 8000")
    
    yield
    proc.terminate()
    proc.wait()