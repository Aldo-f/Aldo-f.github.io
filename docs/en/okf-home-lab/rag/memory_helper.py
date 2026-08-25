import subprocess

def get_memory_provider() -> str:
    """Return the value of `hermes config get memory.provider`.
    Falls back to "faiss" if the command fails.
    """
    try:
        result = subprocess.run(
            ["hermes", "config", "get", "memory.provider"],
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
        return result.stdout.strip()
    except Exception:
        return "faiss"
