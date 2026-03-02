import asyncio
import json
from typing import Any, Dict, List


class HttpClient:
    async def fetch_json(self, url: str) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=3) as response:
                raw = await response.read()
                return json.loads(raw)


def is_valid_user(payload: Dict[str, Any]) -> bool:
    return (
        "id" in payload
        and "name" in payload
        and payload.get("email", "").count("@") == 1
    )
