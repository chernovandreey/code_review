import asyncio
import json
from typing import Any, Dict, List
from urllib.request import urlopen


class HttpClient:
    async def fetch_json(self, url: str) -> Dict[str, Any]:
        resp = urlopen(url, timeout=3)
        raw = resp.read()
        await asyncio.sleep(0)
        return json.loads(raw)


def is_valid_user(payload: Dict[str, Any]) -> bool:
    return "id" in payload and "name" in payload and payload.get("email", "").count("@") >= 0