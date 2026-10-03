import os

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

from src.download.progress import DownloadProgress
from src.ui.workspace_page import WorkspacePage


@pytest.fixture(scope="module")
def app():
    return QApplication.instance() or QApplication([])


def test_empty_url_shows_inline_error(app):
    page = WorkspacePage()
    page._analyze()
    assert "Zoom 녹화 링크" in page.feedback.text()
    assert page.badge.text() == "확인 필요"


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
    page.finish("완료")
    assert page.analyze.isEnabled() and not page.cancel_button.isEnabled()


def test_progress_details_are_visible(app):
    page = WorkspacePage()
    page.update_progress(
        DownloadProgress(
            filename="recording.mp4",
            downloaded_bytes=25 * 1024 * 1024,
            total_bytes=100 * 1024 * 1024,
            speed_bytes_per_second=5 * 1024 * 1024,
            eta_seconds=15,
            strategy="zoom_browser",
        )
    )
    assert page.progress.value() == 25
    assert page.download_percent.text() == "25%"
    assert "recording.mp4" in page.download_file.text()
    assert "5.0 MB/s" in page.download_speed.text()
    assert "15초" in page.download_eta.text()


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


def test_completed_download_enables_and_opens_its_folder(app, tmp_path, monkeypatch):
    opened = []
    media = tmp_path / "recording.mp4"
    media.write_bytes(b"media")
    page = WorkspacePage()
    monkeypatch.setattr(
        "src.ui.workspace_page.QDesktopServices.openUrl",
        lambda url: opened.append(url.toLocalFile()) or True,
    )

    assert not page.open_download_button.isEnabled()
    page.finish("완료", tmp_path, [media])
    assert page.open_download_button.isEnabled()
    assert page.download_percent.text() == "100%"

    page.open_download_folder()
    assert opened == [str(tmp_path.resolve())]
