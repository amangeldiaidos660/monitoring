from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
import random

from playwright.async_api import Browser, BrowserContext, async_playwright

from app.config import settings
from app.collectors.proxies import proxy_rotator


@asynccontextmanager
async def browser_context() -> AsyncIterator[BrowserContext]:
    async with async_playwright() as playwright:
        browser_type = getattr(playwright, settings.playwright_browser)
        proxy = proxy_rotator.next()
        launch_options = {"headless": settings.playwright_headless}
        if proxy is not None:
            launch_options["proxy"] = proxy.as_playwright_proxy()
        browser: Browser = await browser_type.launch(**launch_options)
        context_options = {}
        if settings.user_agent_list:
            context_options["user_agent"] = random.choice(settings.user_agent_list)
        context = await browser.new_context(**context_options)
        context.set_default_timeout(settings.playwright_timeout_ms)
        try:
            yield context
        finally:
            await context.close()
            await browser.close()

