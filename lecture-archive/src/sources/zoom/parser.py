from src.sources.zoom.access import SELECTORS, first_visible
from src.sources.zoom.models import ZoomPageState


class ZoomPageParser:
    async def inspect(self, page) -> ZoomPageState:
        title = await page.title()
        body = (await page.locator("body").inner_text(timeout=3_000)).lower()
        download = await first_visible(page, SELECTORS["download_button"])
        video = await first_visible(page, SELECTORS["video"])
        passcode = await first_visible(page, SELECTORS["passcode_input"])
        login = await first_visible(page, SELECTORS["login_button"])
        not_found = "recording does not exist" in body or "recording has expired" in body
        disabled = any(text in body for text in ("download has been disabled", "download disabled"))
        return ZoomPageState(
            recording_found=False if not_found else True,
            playback_available=video is not None,
            download_allowed=False if disabled else (True if download is not None else None),
            passcode_required=passcode is not None,
            login_required=login is not None and video is None,
            download_button_visible=download is not None,
            title=title,
        )

