from dataclasses import dataclass
from itertools import cycle
from threading import Lock

from app.config import settings


@dataclass(frozen=True)
class ProxyConfig:
    server: str

    def as_playwright_proxy(self) -> dict[str, str]:
        return {"server": self.server}


class ProxyRotator:
    def __init__(self, proxy_urls: list[str]) -> None:
        self._lock = Lock()
        self._proxies = [ProxyConfig(server=url) for url in proxy_urls]
        self._cycle = cycle(self._proxies) if self._proxies else None

    def next(self) -> ProxyConfig | None:
        if self._cycle is None:
            return None
        with self._lock:
            return next(self._cycle)


proxy_rotator = ProxyRotator(settings.proxy_url_list)

