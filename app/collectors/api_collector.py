from dataclasses import dataclass

from tenacity import retry, stop_after_attempt, wait_exponential


@dataclass(frozen=True)
class ApiVideo:
    platform: str
    url: str
    author: str | None
    caption: str | None
    raw: dict


class OfficialApiCollector:
    @retry(wait=wait_exponential(multiplier=1, min=2, max=60), stop=stop_after_attempt(5))
    async def collect_keyword(self, platform: str, keyword: str) -> list[ApiVideo]:
        if platform == "tiktok":
            return await self._collect_tiktok_keyword(keyword)
        if platform == "instagram":
            return await self._collect_instagram_keyword(keyword)
        raise ValueError(f"Unsupported platform: {platform}")

    async def _collect_tiktok_keyword(self, keyword: str) -> list[ApiVideo]:
        return []

    async def _collect_instagram_keyword(self, keyword: str) -> list[ApiVideo]:
        return []


official_api_collector = OfficialApiCollector()

