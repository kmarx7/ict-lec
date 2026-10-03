import shutil

from src.agent.context import AgentContext
from src.agent.models import Observation
from src.sources.zoom.url_parser import ZoomURLParser


class BasicObserver:
    """Combines safe local facts with optional page/API observations supplied by adapters."""

    def __init__(self, page_probe=None, api_available=None) -> None:
        self.page_probe = page_probe
        self.api_available = api_available or (lambda: False)

    async def inspect(self, context: AgentContext) -> Observation:
        local = context.local_import_path
        result = Observation(
            local_file_available=bool(local and local.is_file()),
            disk_free_bytes=shutil.disk_usage(local.parent if local else ".").free,
            api_available=bool(self.api_available()),
        )
        try:
            parsed = ZoomURLParser().parse(context.original_url)
            result.url_valid = True
            result.canonical_url = parsed.canonical_url
        except ValueError as exc:
            if not result.local_file_available:
                result.errors.append(str(exc))
            return result
        if self.page_probe:
            state = await self.page_probe(result.canonical_url)
            result.browser_session_available = True
            result.recording_found = state.recording_found
            result.playback_available = state.playback_available
            result.download_allowed = state.download_allowed
            result.passcode_required = state.passcode_required
            result.login_required = state.login_required
            result.browser_download_available = state.download_button_visible
        return result
