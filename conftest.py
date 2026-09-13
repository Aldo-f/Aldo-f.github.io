import subprocess, sys, os, time, urllib.request, tempfile, shutil
import pytest


@pytest.fixture(scope="session", autouse=True)
def start_http_server():
    """Start a simple HTTP server on port 8000 serving minimal static pages.
    Creates temporary 404.html files with the required DOM element.
    """
    # Create temporary directory with minimal pages
    temp_dir = tempfile.mkdtemp()
    # root 404.html
    with open(os.path.join(temp_dir, "404.html"), "w") as f:
        f.write('<div id="dungeon-scene"></div>')
    # nl/404.html
    os.makedirs(os.path.join(temp_dir, "nl"), exist_ok=True)
    with open(os.path.join(temp_dir, "nl", "404.html"), "w") as f:
        f.write('<div id="dungeon-scene"></div>')
    # Start server
    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "http.server",
            "8000",
            "--directory",
            temp_dir,
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
    shutil.rmtree(temp_dir)
