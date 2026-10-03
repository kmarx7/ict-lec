import shutil
from pathlib import Path

from src.agent.context import AgentContext
from src.agent.models import ExecutionResult
from src.strategies.base import DownloadStrategy


class LocalImportStrategy(DownloadStrategy):
    name = "local_import"

    def __init__(self, destination_dir: Path) -> None:
        self.destination_dir = destination_dir

    async def can_handle(self, context: AgentContext) -> bool:
        return bool(context.local_import_path and context.local_import_path.is_file())

    async def execute(self, context: AgentContext) -> ExecutionResult:
        source = context.local_import_path
        if not source or not source.is_file():
            return ExecutionResult(success=False, strategy=self.name, error_code="HTTP_NOT_FOUND", message="Local file not found")
        self.destination_dir.mkdir(parents=True, exist_ok=True)
        target = self.destination_dir / source.name
        if source.resolve() != target.resolve():
            await __import__("asyncio").to_thread(shutil.copy2, source, target)
        return ExecutionResult(success=True, strategy=self.name, downloaded_files=[target])

