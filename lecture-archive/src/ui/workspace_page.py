from pathlib import Path

from PySide6.QtCore import Qt, QUrl, Signal
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QListWidget,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.app.config import AppConfig
from src.ui.components import PageHeader, Panel


class WorkspacePage(QWidget):
    analyze_requested = Signal(str)
    import_requested = Signal(str)
    cancel_requested = Signal()

    def __init__(self, repository=None) -> None:
        super().__init__()
        self.repository = repository
        self.archive_root = AppConfig().download_dir
        self.recording_rows = []
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 28)
        layout.setSpacing(18)
        top = QHBoxLayout()
        top.addWidget(PageHeader("Lecture Archive", "Acquire and archive", "One workspace from authorized Zoom link to verified local media."), 1)
        privacy = QLabel("PRIVATE · ON DEVICE")
        privacy.setObjectName("statusBadge")
        privacy.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top.addWidget(privacy, alignment=Qt.AlignmentFlag.AlignTop)
        layout.addLayout(top)

        acquire = Panel()
        input_row = QHBoxLayout()
        input_row.setSpacing(10)
        self.url = QLineEdit()
        self.url.setPlaceholderText("Paste a Zoom share or playback URL…")
        self.url.setClearButtonEnabled(True)
        self.url.returnPressed.connect(self._analyze)
        self.analyze = QPushButton("Analyze & download")
        self.analyze.setObjectName("primaryButton")
        self.analyze.clicked.connect(self._analyze)
        self.import_button = QPushButton("Import file…")
        self.import_button.clicked.connect(self._pick_file)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("quietButton")
        self.cancel_button.setEnabled(False)
        self.cancel_button.clicked.connect(self.cancel_requested.emit)
        input_row.addWidget(self.url, 1)
        input_row.addWidget(self.import_button)
        input_row.addWidget(self.analyze)
        input_row.addWidget(self.cancel_button)
        acquire.content.addLayout(input_row)
        self.feedback = QLabel("Ready — enter a recording URL or import an existing file.")
        self.feedback.setObjectName("secondaryText")
        self.feedback.setWordWrap(True)
        acquire.content.addWidget(self.feedback)
        self.progress = QProgressBar()
        self.progress.hide()
        acquire.content.addWidget(self.progress)
        layout.addWidget(acquire)

        split = QSplitter(Qt.Orientation.Horizontal)
        activity = Panel("Activity", "The acquisition loop reports every decision and result.")
        self.badge = QLabel("READY")
        self.badge.setObjectName("statusBadge")
        activity.content.addWidget(self.badge, alignment=Qt.AlignmentFlag.AlignLeft)
        self.timeline = QListWidget()
        self.timeline.setObjectName("timeline")
        self.timeline.addItem("•  Waiting for a recording")
        activity.content.addWidget(self.timeline, 1)
        library = Panel("Recent archive", "Verified items stored on this Mac.")
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Title", "Status", "Created"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.itemSelectionChanged.connect(self._update_open_button)
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.empty_library = QLabel("No verified recordings yet.")
        self.empty_library.setObjectName("secondaryText")
        self.empty_library.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        library.content.addWidget(self.empty_library)
        library.content.addWidget(self.table, 1)
        folder_actions = QHBoxLayout()
        self.open_selected_button = QPushButton("Open selected in Finder")
        self.open_selected_button.setEnabled(False)
        self.open_selected_button.clicked.connect(self.open_selected_in_finder)
        self.open_archive_button = QPushButton("Open archive folder")
        self.open_archive_button.setObjectName("quietButton")
        self.open_archive_button.clicked.connect(self.open_archive_folder)
        folder_actions.addWidget(self.open_selected_button)
        folder_actions.addWidget(self.open_archive_button)
        folder_actions.addStretch()
        library.content.addLayout(folder_actions)
        library.content.addStretch()
        split.addWidget(activity)
        split.addWidget(library)
        split.setSizes([620, 390])
        split.setChildrenCollapsible(False)
        layout.addWidget(split, 1)
        self.refresh_library()

    def _analyze(self) -> None:
        value = self.url.text().strip()
        if not value:
            self.show_error("Enter a Zoom recording URL first.")
            self.url.setFocus()
            return
        self.analyze_requested.emit(value)

    def _pick_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Import Recording", "", "Media (*.mp4 *.m4a *.mov *.vtt);;All Files (*)")
        if path:
            self.import_requested.emit(path)

    def begin(self, message: str = "Analyzing recording…") -> None:
        self.timeline.clear()
        self.feedback.setText(message)
        self._set_badge("RUNNING", "running")
        self.progress.setRange(0, 0)
        self.progress.show()
        self.analyze.setEnabled(False)
        self.import_button.setEnabled(False)
        self.cancel_button.setEnabled(True)

    def finish(self, message: str) -> None:
        self.feedback.setText(message)
        self._set_badge("COMPLETE", "success")
        self.progress.hide()
        self._set_idle_controls()

    def show_error(self, message: str) -> None:
        self.feedback.setText(message)
        self._set_badge("NEEDS ATTENTION", "error")
        self.progress.hide()
        self._set_idle_controls()

    def add_event(self, event) -> None:
        symbol = "✓" if event.event_type.value in {"ACTION_COMPLETED", "GOAL_REACHED"} else "•"
        if event.event_type.value in {"ACTION_FAILED", "TERMINATED"}:
            symbol = "✕"
        self.timeline.addItem(f"{symbol}  {event.message}")
        self.timeline.scrollToBottom()
        self.feedback.setText(event.message)

    def update_progress(self, progress) -> None:
        self.progress.show()
        if progress.percentage is None:
            self.progress.setRange(0, 0)
        else:
            self.progress.setRange(0, 100)
            self.progress.setValue(round(progress.percentage))
        speed = progress.speed_bytes_per_second / (1024 * 1024)
        self.feedback.setText(f"{progress.filename} · {progress.downloaded_bytes / (1024 * 1024):.1f} MB · {speed:.1f} MB/s")

    def refresh_library(self) -> None:
        self.recording_rows = list(self.repository.list_recordings()[:8]) if self.repository else []
        self.table.setRowCount(len(self.recording_rows))
        self.empty_library.setVisible(not self.recording_rows)
        self.table.setVisible(bool(self.recording_rows))
        self.open_selected_button.setEnabled(False)
        for row_index, row in enumerate(self.recording_rows):
            for column, key in enumerate(("title", "status", "created_at")):
                self.table.setItem(row_index, column, QTableWidgetItem(str(row[key] or "")))

    def open_selected_in_finder(self) -> None:
        row_index = self.table.currentRow()
        if row_index < 0 or row_index >= len(self.recording_rows):
            self.show_error("Select an archived recording first.")
            return
        directory = Path(self.recording_rows[row_index]["local_directory"] or "")
        if not directory.is_dir():
            self.show_error("The selected archive folder no longer exists on this Mac.")
            return
        self._open_path(directory)

    def open_archive_folder(self) -> None:
        self.archive_root.mkdir(parents=True, exist_ok=True)
        self._open_path(self.archive_root)

    def _open_path(self, path: Path) -> None:
        if not QDesktopServices.openUrl(QUrl.fromLocalFile(str(path.resolve()))):
            self.show_error("Finder could not open this folder.")

    def _update_open_button(self) -> None:
        self.open_selected_button.setEnabled(self.table.currentRow() >= 0)

    def _set_idle_controls(self) -> None:
        self.analyze.setEnabled(True)
        self.import_button.setEnabled(True)
        self.cancel_button.setEnabled(False)

    def _set_badge(self, text: str, state: str) -> None:
        self.badge.setText(text)
        self.badge.setProperty("state", state)
        self.badge.style().unpolish(self.badge)
        self.badge.style().polish(self.badge)
