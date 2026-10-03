from pathlib import Path

from src.agent.context import AgentContext
from src.agent.models import ExecutionResult
from src.sources.zoom.access import SELECTORS, first_visible
from src.strategies.base import DownloadStrategy


class ZoomBrowserDownloadStrategy(DownloadStrategy):
    name = "zoom_browser"

    def __init__(self, page_provider, destination_dir: Path) -> None:
        self.page_provider, self.destination_dir = page_provider, destination_dir

    async def can_handle(self, context: AgentContext) -> bool:
        return context.download_allowed is not False and context.browser_session_available

    async def execute(self, context: AgentContext) -> ExecutionResult:
        page = await self.page_provider(context.canonical_url or context.original_url)
        button = await first_visible(page, SELECTORS["download_button"])
        if button is None or await button.is_disabled():
            return ExecutionResult(success=False, strategy=self.name, error_code="DOWNLOAD_NOT_ALLOWED", message="Official Download control is unavailable")
        self.destination_dir.mkdir(parents=True, exist_ok=True)
        async with page.expect_download() as info:
            await button.click()
        download = await info.value
        target = self.destination_dir / download.suggested_filename
        await download.save_as(target)
        return ExecutionResult(success=True, strategy=self.name, downloaded_files=[target])

