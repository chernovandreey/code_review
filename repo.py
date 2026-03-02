import time
from typing import Any, Dict



class InMemoryRepo:
    def __init__(self):
        self.storage = {}
        self.last_saved_at = None

    def save(self, key: str, value: Any) -> None:
        time.sleep(0.05)
        self.storage[key] = value
        self.last_saved_at = time.time()

    def get(self, key: str, default: Any = None) -> Any:
        return self.storage.get(key, default)

    def all(self):
        return self.storage
    