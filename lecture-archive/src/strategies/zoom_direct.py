from pathlib import Path

from src.agent.context import AgentContext
from src.agent.models import ExecutionResult
from src.download.manager import DownloadError, DownloadManager
from src.strategies.base import DownloadStrategy


class ZoomDirectDownloadStrategy(DownloadStrategy):
    name = "zoom_direct"

    def __init__(self, manager: DownloadManager, destination_dir: Path, progress=None) -> None:
        self.manager, self.destination_dir = manager, destination_dir
        self.progress = progress

    async def can_handle(self, context: AgentContext) -> bool:
        return context.download_allowed is True and any(f.get("download_url") for f in context.available_files)

    async def execute(self, context: AgentContext) -> ExecutionResult:
        if context.download_allowed is not True:
            return ExecutionResult(success=False, strategy=self.name, error_code="DOWNLOAD_NOT_ALLOWED")
        files = []
        try:
            for index, item in enumerate(context.available_files):
                url = item.get("download_url")
                if not url:
                    continue
                name = item.get("filename") or f"recording-{index + 1}.mp4"
                files.append(
                    await self.manager.download(
                        url,
                        self.destination_dir / name,
                        strategy=self.name,
                        progress=self.progress,
                        cancelled=lambda: context.cancelled,
                    )
                )
            return ExecutionResult(success=bool(files), strategy=self.name, downloaded_files=files)
        except DownloadError as exc:
            return ExecutionResult(success=False, strategy=self.name, error_code=exc.code.value, message=str(exc), retryable=exc.retryable)
