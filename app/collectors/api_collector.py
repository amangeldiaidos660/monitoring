from dataclasses import dataclass


@dataclass(frozen=True)
class ApiVideo:
    platform: str
    url: str
    author: str | None
    caption: str | None
    raw: dict


class ApiCollector:
    async def collect_keyword(self, keyword: str) -> list[ApiVideo]:
        raise NotImplementedError

    async def collect_hashtag(self, hashtag: str) -> list[ApiVideo]:
        raise NotImplementedError

    async def collect_account(self, username: str) -> list[ApiVideo]:
        raise NotImplementedError
