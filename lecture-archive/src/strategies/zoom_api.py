from src.strategies.zoom_direct import ZoomDirectDownloadStrategy


class ZoomApiStrategy(ZoomDirectDownloadStrategy):
    name = "zoom_api"

    async def can_handle(self, context):
        return context.api_available and await super().can_handle(context)

