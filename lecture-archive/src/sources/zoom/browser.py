from playwright.async_api import Browser, BrowserContext, Page, async_playwright


class ZoomBrowserSession:
    def __init__(self) -> None:
        self._playwright = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None

    async def open(self, url: str, *, headed: bool = True) -> Page:
        if self.page is None:
            self._playwright = await async_playwright().start()
            self.browser = await self._playwright.chromium.launch(headless=not headed)
            self.context = await self.browser.new_context(accept_downloads=True)
            self.page = await self.context.new_page()
        await self.page.goto(url, wait_until="domcontentloaded")
        return self.page

    async def close(self) -> None:
        if self.browser:
            await self.browser.close()
        if self._playwright:
            await self._playwright.stop()
        self.page = self.context = self.browser = self._playwright = None

