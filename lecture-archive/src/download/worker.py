from src.download.manager import DownloadManager


class DownloadWorker:
    """Thin async worker boundary kept separate for future Qt signal integration."""

    def __init__(self, manager: DownloadManager | None = None) -> None:
        self.manager = manager or DownloadManager()

    async def run(self, *args, **kwargs):
        return await self.manager.download(*args, **kwargs)

