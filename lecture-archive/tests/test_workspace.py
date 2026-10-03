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


class RepositoryStub:
    def __init__(self, rows):
        self.rows = rows

    def list_recordings(self):
        return self.rows


def test_selecting_archive_enables_finder_button(app, tmp_path):
    row = {
        "title": "Lecture",
        "status": "archived",
        "created_at": "2026-10-03",
        "local_directory": str(tmp_path),
    }
    page = WorkspacePage(RepositoryStub([row]))
    assert not page.open_selected_button.isEnabled()
    page.table.selectRow(0)
    assert page.open_selected_button.isEnabled()


def test_open_archive_folder_creates_and_opens_directory(app, tmp_path, monkeypatch):
    opened = []
    page = WorkspacePage()
    page.archive_root = tmp_path / "LectureArchive"
    monkeypatch.setattr(
        "src.ui.workspace_page.QDesktopServices.openUrl",
        lambda url: opened.append(url.toLocalFile()) or True,
    )
    page.open_archive_folder()
    assert page.archive_root.is_dir()
    assert opened == [str(page.archive_root.resolve())]
