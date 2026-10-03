import asyncio
import json
import sys
from datetime import date
from pathlib import Path

from PySide6.QtWidgets import QApplication, QDialog
from qasync import QEventLoop, asyncSlot

from src.agent.context import AgentContext
from src.agent.controller import LoopController
from src.agent.evaluator import GoalEvaluator
from src.agent.events import AgentEvent, EventType
from src.agent.executor import Executor
from src.agent.observer import BasicObserver
from src.agent.planner import RuleBasedPlanner
from src.app.config import AppConfig
from src.library.database import Database
from src.library.filesystem import archive_directory
from src.library.repository import RecordingRepository
from src.sources.zoom.access import SELECTORS, first_visible
from src.sources.zoom.browser import ZoomBrowserSession
from src.sources.zoom.parser import ZoomPageParser
from src.strategies.local_import import LocalImportStrategy
from src.strategies.zoom_browser import ZoomBrowserDownloadStrategy
from src.ui.dialogs.login_dialog import LoginDialog
from src.ui.dialogs.passcode_dialog import PasscodeDialog
from src.ui.main_window import MainWindow


class ApplicationCoordinator:
    def __init__(self, window: MainWindow, config: AppConfig, repository: RecordingRepository) -> None:
        self.window, self.config, self.repository = window, config, repository
        self.controller: LoopController | None = None
        self.active_context: AgentContext | None = None
        self.browser = ZoomBrowserSession()
        self.page_parser = ZoomPageParser()
        window.workspace.analyze_requested.connect(self.analyze)
        window.workspace.import_requested.connect(self.import_file)
        window.workspace.cancel_requested.connect(self.cancel)

    @asyncSlot(str)
    async def analyze(self, url: str) -> None:
        context = AgentContext(original_url=url)
        await self._run(context)

    @asyncSlot(str)
    async def import_file(self, path: str) -> None:
        context = AgentContext(original_url="local://import", source_type="local", local_import_path=Path(path))
        await self._run(context)

    def cancel(self) -> None:
        if self.active_context:
            self.active_context.cancelled = True
            self.window.workspace.show_error("Cancellation requested. Stopping safely…")

    async def _run(self, context: AgentContext) -> None:
        self.active_context = context
        self.window.workspace.begin(
            "Importing and verifying local file…"
            if context.source_type == "local"
            else "Opening the authorized Zoom recording page…"
        )
        title = context.local_import_path.stem if context.local_import_path else "Zoom_Recording"
        destination = archive_directory(self.config.download_dir, title, date.today())
        observer = BasicObserver(page_probe=None if context.source_type == "local" else self._probe_page)
        strategies = {
            "local_import": LocalImportStrategy(destination),
            "zoom_browser": ZoomBrowserDownloadStrategy(self._open_page, destination),
        }
        self.controller = LoopController(
            observer,
            RuleBasedPlanner(),
            Executor(strategies),
            GoalEvaluator(),
            max_loops=self.config.max_loops,
            event_sink=self.window.workspace.add_event,
            human_handler=self._handle_human_action,
        )
        try:
            result = await self.controller.run(context)
            if result.goal_reached:
                self._archive(result, destination, title)
                self.window.workspace.refresh_library()
                self.window.workspace.finish("Verified and archived successfully.")
            else:
                reason = (
                    result.terminal_reason
                    or result.last_error_message
                    or "No authorized download path is available."
                )
                self.window.workspace.show_error(reason)
        except Exception as exc:
            error_name = type(exc).__name__
            self.window.workspace.add_event(
                AgentEvent(
                    event_type=EventType.ACTION_FAILED,
                    message=f"The acquisition could not start ({error_name}).",
                    error_code="UNKNOWN_ERROR",
                )
            )
            self.window.workspace.show_error(
                f"Could not continue because {error_name} occurred. Check Playwright/browser setup."
            )
        finally:
            self.active_context = None

    async def _open_page(self, url: str):
        return await self.browser.open(url, headed=True)

    async def _probe_page(self, url: str):
        return await self.page_parser.inspect(await self._open_page(url))

    async def _handle_human_action(self, context, plan) -> None:
        if plan.action.value == "request_passcode":
            dialog = PasscodeDialog(self.window)
            if dialog.exec() != QDialog.DialogCode.Accepted:
                context.cancelled = True
                return
            context.passcode = dialog.value()
            page = await self._open_page(context.canonical_url or context.original_url)
            input_box = await first_visible(page, SELECTORS["passcode_input"])
            submit = await first_visible(page, SELECTORS["passcode_submit"])
            if input_box and submit:
                await input_box.fill(context.passcode)
                await submit.click()
                await page.wait_for_timeout(1_000)
            context.passcode = None
            context.passcode_required = False
        else:
            await self._open_page(context.canonical_url or context.original_url)
            dialog = LoginDialog(self.window)
            if dialog.exec() != QDialog.DialogCode.Accepted:
                context.cancelled = True
            context.login_required = False

    def _archive(self, context: AgentContext, destination: Path, title: str) -> None:
        metadata = {
            "source": context.source_type,
            "title": title,
            "recording_date": date.today().isoformat(),
            "acquisition_strategy": context.current_strategy,
            "verified": True,
            "files": [
                {"type": path.suffix.removeprefix(".").upper(), "filename": path.name, "verified": True}
                for path in context.completed_files
            ],
        }
        destination.mkdir(parents=True, exist_ok=True)
        (destination / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
        self.repository.add(
            source_url=context.canonical_url or context.original_url,
            title=title,
            strategy=context.current_strategy or "unknown",
            directory=destination,
            files=context.completed_files,
        )


def main() -> int:
    app = QApplication.instance() or QApplication(sys.argv)
    config = AppConfig()
    database = Database(config.database_path)
    database.initialize()
    repository = RecordingRepository(database)
    window = MainWindow(repository)
    coordinator = ApplicationCoordinator(window, config, repository)
    window._coordinator = coordinator
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window.show()
    with loop:
        loop.run_forever()
    return 0
