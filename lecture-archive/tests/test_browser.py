from pathlib import Path

from src.sources.zoom import browser


def test_packaged_app_uses_standard_playwright_cache(monkeypatch):
    monkeypatch.setattr(browser.sys, "frozen", True, raising=False)
    monkeypatch.delenv("PLAYWRIGHT_BROWSERS_PATH", raising=False)
    browser.configure_packaged_browser_path()
    assert Path(browser.os.environ["PLAYWRIGHT_BROWSERS_PATH"]).name == "ms-playwright"


def test_development_keeps_playwright_default(monkeypatch):
    monkeypatch.delattr(browser.sys, "frozen", raising=False)
    monkeypatch.delenv("PLAYWRIGHT_BROWSERS_PATH", raising=False)
    browser.configure_packaged_browser_path()
    assert "PLAYWRIGHT_BROWSERS_PATH" not in browser.os.environ
