from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from typing import Any

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.collectors.api_collector import ApiCollector, ApiVideo
from app.config import settings


QUERY_VIDEOS_PATH = "/v2/research/video/query/"
DEFAULT_FIELDS = [
    "id",
    "video_description",
    "create_time",
    "username",
    "region_code",
    "view_count",
    "like_count",
    "comment_count",
    "share_count",
    "hashtag_names",
]


class TikTokResearchApiError(RuntimeError):
    def __init__(self, message: str, status_code: int | None = None, retry_after_seconds: int | None = None) -> None:
        self.status_code = status_code
        self.retry_after_seconds = retry_after_seconds
        super().__init__(message)


class TikTokResearchRateLimitError(TikTokResearchApiError):
    def __init__(self, retry_after_seconds: int | None = None) -> None:
        self.retry_after_seconds = retry_after_seconds
        super().__init__("TikTok Research API rate limit exceeded", status_code=429, retry_after_seconds=retry_after_seconds)


@dataclass(frozen=True)
class TikTokQueryWindow:
    start_date: date
    end_date: date

    @classmethod
    def recent(cls, days: int) -> "TikTokQueryWindow":
        end_date = datetime.now(UTC).date()
        start_date = end_date - timedelta(days=days - 1)
        return cls(start_date=start_date, end_date=end_date)

    def as_body_dates(self) -> dict[str, str]:
        return {
            "start_date": self.start_date.strftime("%Y%m%d"),
            "end_date": self.end_date.strftime("%Y%m%d"),
        }


class TikTokResearchCollector(ApiCollector):
    def __init__(
        self,
        token: str = settings.tiktok_research_api_token,
        base_url: str = settings.tiktok_research_api_base_url,
        region_code: str = settings.tiktok_region_code,
        max_count: int = settings.tiktok_max_count,
        query_days: int = settings.tiktok_query_days,
    ) -> None:
        self.token = token
        self.base_url = base_url.rstrip("/")
        self.region_code = region_code
        self.max_count = max_count
        self.query_days = query_days

    async def collect_keyword(self, keyword: str) -> list[ApiVideo]:
        return await self._collect(field_name="keyword", field_value=keyword)

    async def collect_hashtag(self, hashtag: str) -> list[ApiVideo]:
        normalized = hashtag.lstrip("#")
        return await self._collect(field_name="hashtag_name", field_value=normalized)

    async def collect_account(self, username: str) -> list[ApiVideo]:
        normalized = username.lstrip("@")
        return await self._collect(field_name="username", field_value=normalized)

    async def _collect(self, field_name: str, field_value: str) -> list[ApiVideo]:
        if not self.token:
            raise TikTokResearchApiError("TIKTOK_RESEARCH_API_TOKEN is not configured")

        window = TikTokQueryWindow.recent(self.query_days)
        cursor = 0
        search_id = None
        videos: list[ApiVideo] = []

        async with httpx.AsyncClient(base_url=self.base_url, timeout=30) as client:
            while True:
                body = self.build_query_body(
                    field_name=field_name,
                    field_value=field_value,
                    window=window,
                    cursor=cursor,
                    search_id=search_id,
                )
                payload = await self._post_query_videos(client, body)
                data = payload.get("data", {})
                videos.extend(self._parse_videos(payload))
                if not data.get("has_more"):
                    break
                cursor = int(data.get("cursor", cursor))
                search_id = data.get("search_id", search_id)

        return videos

    def build_query_body(
        self,
        field_name: str,
        field_value: str,
        window: TikTokQueryWindow,
        cursor: int | None = None,
        search_id: str | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "query": {
                "and": [
                    {
                        "operation": "IN",
                        "field_name": "region_code",
                        "field_values": [self.region_code],
                    },
                    {
                        "operation": "EQ",
                        "field_name": field_name,
                        "field_values": [field_value],
                    },
                ]
            },
            **window.as_body_dates(),
            "max_count": self.max_count,
            "is_random": False,
        }
        if cursor:
            body["cursor"] = cursor
        if search_id:
            body["search_id"] = search_id
        return body

    @retry(
        wait=wait_exponential(multiplier=1, min=2, max=60),
        stop=stop_after_attempt(5),
        retry=retry_if_exception_type((TikTokResearchRateLimitError, httpx.TimeoutException, httpx.TransportError)),
        reraise=True,
    )
    async def _post_query_videos(self, client: httpx.AsyncClient, body: dict[str, Any]) -> dict[str, Any]:
        response = await client.post(
            QUERY_VIDEOS_PATH,
            params={"fields": ",".join(DEFAULT_FIELDS)},
            headers={"Authorization": f"Bearer {self.token}"},
            json=body,
        )
        if response.status_code == 429:
            retry_after = response.headers.get("retry-after")
            raise TikTokResearchRateLimitError(int(retry_after) if retry_after and retry_after.isdigit() else None)
        if response.status_code >= 500:
            raise TikTokResearchApiError(f"TikTok Research API server error: {response.status_code}", status_code=response.status_code)
        if response.status_code >= 400:
            raise TikTokResearchApiError(f"TikTok Research API request failed: {response.status_code} {response.text}", status_code=response.status_code)
        return response.json()

    def _parse_videos(self, payload: dict[str, Any]) -> list[ApiVideo]:
        raw_videos = payload.get("data", {}).get("videos", [])
        videos = []
        for raw in raw_videos:
            videos.append(
                ApiVideo(
                    platform="tiktok",
                    url=f"https://www.tiktok.com/@{raw.get('username')}/video/{raw.get('id')}",
                    author=raw.get("username"),
                    caption=raw.get("video_description"),
                    raw=raw,
                )
            )
        return videos


tiktok_research_collector = TikTokResearchCollector()
