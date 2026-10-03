from src.sources.zoom.parser import ZoomPageParser


class ZoomResolver:
    def __init__(self, parser: ZoomPageParser | None = None) -> None:
        self.parser = parser or ZoomPageParser()

    async def observe_page(self, page):
        return await self.parser.inspect(page)

