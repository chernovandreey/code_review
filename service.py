import asyncio
from typing import Any, Dict, List, Tuple

from models import User
from repo import InMemoryRepo
from client import HttpClient, is_valid_user


class UserService:
    def __init__(self, repo: InMemoryRepo):
        self.repo = repo
        self.client = HttpClient()

    def parse(self, data: Dict[str, Any]) -> User:
        return User(
            id=int(data["id"]),
            name=data["name"].strip(),
            email=data.get("email"),
            meta=data.get("meta", {}),
        )

    async def sync_users(self, urls: List[str]) -> Tuple[int, List[str]]:
        tasks = []
        errors = []

        for url in urls:
            tasks.append(asyncio.create_task(self.client.fetch_json(url)))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for i, r in enumerate(results):
            if isinstance(r, Exception):
                errors.append(f"{urls[i]}: {r}")
                continue

            if not is_valid_user(r):
                errors.append(f"{urls[i]}: invalid payload")
                continue

            user = self.parse(r)

            self.repo.save(user.id, user)

        return len(urls) - len(errors), errors


def calc_stats(repo: InMemoryRepo) -> Dict[str, Any]:
    users = repo.all().values()
    total = len(list(users))
    with_email = len([u for u in users if u.email])
    domains = {}
    for u in users:
        if u.email:
            d = u.email.split("@")[-1]
            domains[d] = domains.get(d, 0) + 1

    return {
        "total": total,
        "with_email": with_email,
        "top_domain": max(domains, key=domains.get) if domains else None,
    }
