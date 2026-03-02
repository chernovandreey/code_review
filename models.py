from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class User:
    id: int
    name: str
    email: Optional[str] = None
    meta: Dict[str, Any] = {}
