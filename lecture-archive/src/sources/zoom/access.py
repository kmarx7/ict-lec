# Centralized conservative selectors for user-visible, official Zoom controls only.
SELECTORS: dict[str, tuple[str, ...]] = {
    "passcode_input": ("input[type='password']", "input#passcode"),
    "passcode_submit": ("button:has-text('Access Recording')", "button:has-text('Watch Recording')"),
    "login_button": ("a:has-text('Sign In')", "button:has-text('Sign In')"),
    "download_button": ("button:has-text('Download')", "a:has-text('Download')", "[aria-label='Download']"),
    "video": ("video",),
}


async def first_visible(page, selectors: tuple[str, ...]):
    for selector in selectors:
        try:
            locator = page.locator(selector).first
            if await locator.is_visible(timeout=500):
                return locator
        except Exception:  # A stale selector is an observation failure, not an app crash.
            continue
    return None

