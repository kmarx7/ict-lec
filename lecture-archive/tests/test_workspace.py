import os

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

from src.ui.workspace_page import WorkspacePage


@pytest.fixture(scope="module")
def app():
    return QApplication.instance() or QApplication([])


def test_empty_url_shows_inline_error(app):
    page = WorkspacePage()
    page._analyze()
    assert "Enter a Zoom recording URL" in page.feedback.text()
    assert page.badge.text() == "NEEDS ATTENTION"


def test_valid_url_emits_request(app):
    page = WorkspacePage()
    received = []
    page.analyze_requested.connect(received.append)
    page.url.setText("https://zoom.us/rec/share/example")
    page._analyze()
    assert received == ["https://zoom.us/rec/share/example"]


def test_busy_and_complete_states(app):
    page = WorkspacePage()
    page.begin()
    assert not page.analyze.isEnabled() and page.cancel_button.isEnabled()
    page.finish("Done")
    assert page.analyze.isEnabled() and not page.cancel_button.isEnabled()
