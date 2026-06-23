from dataclasses import dataclass

from app.collectors.browser import browser_context


@dataclass(frozen=True)
class ScrapedVideo:
    platform: str
    url: str
    author: str | None = None
    caption: str | None = None
    metrics: dict | None = None


class PlaywrightScraper:
    async def collect_keyword(self, platform: str, keyword: str) -> list[ScrapedVideo]:
        async with browser_context() as context:
            page = await context.new_page()
            await page.goto(self._search_url(platform, keyword), wait_until="domcontentloaded")
            return []

    async def monitor_account(self, platform: str, account: str) -> list[ScrapedVideo]:
        async with browser_context() as context:
            page = await context.new_page()
            await page.goto(self._profile_url(platform, account), wait_until="domcontentloaded")
            return []

    def _search_url(self, platform: str, keyword: str) -> str:
        if platform == "tiktok":
            return f"https://www.tiktok.com/search/video?q={keyword}"
        if platform == "instagram":
            return f"https://www.instagram.com/explore/search/keyword/?q={keyword}"
        raise ValueError(f"Unsupported platform: {platform}")

    def _profile_url(self, platform: str, account: str) -> str:
        username = account.lstrip("@")
        if platform == "tiktok":
            return f"https://www.tiktok.com/@{username}"
        if platform == "instagram":
            return f"https://www.instagram.com/{username}/"
        raise ValueError(f"Unsupported platform: {platform}")


playwright_scraper = PlaywrightScraper()

