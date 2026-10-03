import os
import sys
from pathlib import Path

from playwright.async_api import Browser, BrowserContext, Page, async_playwright


def configure_packaged_browser_path() -> None:
    if getattr(sys, "frozen", False):
        os.environ.setdefault(
            "PLAYWRIGHT_BROWSERS_PATH",
            str(Path.home() / "Library" / "Caches" / "ms-playwright"),
        )


class ZoomBrowserSession:
    def __init__(self) -> None:
        self._playwright = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None

    async def open(self, url: str, *, headed: bool = True) -> Page:
        if self.page is None:
            configure_packaged_browser_path()
            self._playwright = await async_playwright().start()
            self.browser = await self._playwright.chromium.launch(headless=not headed)
            self.context = await self.browser.new_context(accept_downloads=True)
            self.page = await self.context.new_page()
        if self.page.url != url:
            await self.page.goto(url, wait_until="domcontentloaded")
        return self.page

    async def close(self) -> None:
        if self.browser:
            await self.browser.close()
        if self._playwright:
            await self._playwright.stop()
        self.page = self.context = self.browser = self._playwright = None
