"""vLLM healthcheck script."""

import sys
import httpx


def check(url: str = "http://localhost:8000/health") -> int:
    try:
        r = httpx.get(url, timeout=5.0)
        return 0 if r.status_code == 200 else 1
    except Exception:
        return 1


if __name__ == "__main__":
    sys.exit(check())
