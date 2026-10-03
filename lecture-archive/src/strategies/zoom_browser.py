import time
from pathlib import Path

from src.agent.context import AgentContext
from src.agent.models import ExecutionResult
from src.download.progress import DownloadProgress
from src.sources.zoom.access import SELECTORS, first_visible
from src.strategies.base import DownloadStrategy


class ZoomBrowserDownloadStrategy(DownloadStrategy):
    name = "zoom_browser"

    def __init__(self, page_provider, destination_dir: Path, progress=None) -> None:
        self.page_provider = page_provider
        self.destination_dir = destination_dir
        self.progress = progress

    async def can_handle(self, context: AgentContext) -> bool:
        return context.download_allowed is not False and context.browser_session_available

    async def execute(self, context: AgentContext) -> ExecutionResult:
        page = await self.page_provider(context.canonical_url or context.original_url)
        button = await first_visible(page, SELECTORS["download_button"])
        if button is None or await button.is_disabled():
            return ExecutionResult(success=False, strategy=self.name, error_code="DOWNLOAD_NOT_ALLOWED", message="Zoom의 공식 다운로드 버튼을 사용할 수 없습니다.")
        self.destination_dir.mkdir(parents=True, exist_ok=True)
        async with page.expect_download() as info:
            await button.click()
        download = await info.value
        target = self.destination_dir / download.suggested_filename
        started_at = time.monotonic()
        if self.progress:
            self.progress(DownloadProgress(target.name, 0, None, 0, None, self.name))
        await download.save_as(target)
        if self.progress:
            size = target.stat().st_size
            elapsed = max(time.monotonic() - started_at, 0.001)
            self.progress(DownloadProgress(target.name, size, size, size / elapsed, 0, self.name))
        return ExecutionResult(success=True, strategy=self.name, downloaded_files=[target])
