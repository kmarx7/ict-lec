from pathlib import Path

from PySide6.QtCore import Qt, QUrl, Signal
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QAbstractItemView,
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
    cancel_requested = Signal()

    def __init__(self, repository=None) -> None:
        super().__init__()
        self.repository = repository
        self.archive_root = AppConfig().download_dir
        self.recording_rows = []
        self.completed_directory: Path | None = None
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 28)
        layout.setSpacing(18)
        top = QHBoxLayout()
        top.addWidget(
            PageHeader(
                "강의 아카이브",
                "Zoom 녹화 다운로드",
                "공식적으로 허용된 경로로 녹화를 내려받고 안전하게 보관합니다.",
            ),
            1,
        )
        privacy = QLabel("내 컴퓨터에만 저장")
        privacy.setObjectName("statusBadge")
        privacy.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top.addWidget(privacy, alignment=Qt.AlignmentFlag.AlignTop)
        layout.addLayout(top)

        acquire = Panel()
        input_row = QHBoxLayout()
        input_row.setSpacing(10)
        self.url = QLineEdit()
        self.url.setPlaceholderText("Zoom 공유 또는 재생 링크를 붙여넣으세요")
        self.url.setClearButtonEnabled(True)
        self.url.returnPressed.connect(self._analyze)
        self.analyze = QPushButton("다운로드 시작")
        self.analyze.setObjectName("primaryButton")
        self.analyze.clicked.connect(self._analyze)
        self.cancel_button = QPushButton("취소")
        self.cancel_button.setObjectName("quietButton")
        self.cancel_button.setEnabled(False)
        self.cancel_button.clicked.connect(self.cancel_requested.emit)
        input_row.addWidget(self.url, 1)
        input_row.addWidget(self.analyze)
        input_row.addWidget(self.cancel_button)
        acquire.content.addLayout(input_row)
        self.feedback = QLabel("Zoom 녹화 링크를 입력한 뒤 다운로드를 시작하세요.")
        self.feedback.setObjectName("secondaryText")
        self.feedback.setWordWrap(True)
        acquire.content.addWidget(self.feedback)
        layout.addWidget(acquire)

        download = Panel("다운로드 현황", "분석, 다운로드, 파일 검증 과정을 여기에서 확인할 수 있습니다.")
        status_row = QHBoxLayout()
        self.download_status = QLabel("대기 중")
        self.download_status.setObjectName("downloadStatus")
        self.download_percent = QLabel("—")
        self.download_percent.setObjectName("downloadPercent")
        status_row.addWidget(self.download_status)
        status_row.addStretch()
        status_row.addWidget(self.download_percent)
        download.content.addLayout(status_row)
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        download.content.addWidget(self.progress)
        metrics = QHBoxLayout()
        metrics.setSpacing(24)
        self.download_file = QLabel("파일  —")
        self.download_size = QLabel("받은 용량  —")
        self.download_speed = QLabel("속도  —")
        self.download_eta = QLabel("남은 시간  —")
        for label in (self.download_file, self.download_size, self.download_speed, self.download_eta):
            label.setObjectName("downloadMetric")
            metrics.addWidget(label)
        metrics.addStretch()
        download.content.addLayout(metrics)
        download_actions = QHBoxLayout()
        download_actions.addStretch()
        self.open_download_button = QPushButton("받은 파일 폴더 열기")
        self.open_download_button.setEnabled(False)
        self.open_download_button.clicked.connect(self.open_download_folder)
        download_actions.addWidget(self.open_download_button)
        download.content.addLayout(download_actions)
        layout.addWidget(download)

        split = QSplitter(Qt.Orientation.Horizontal)
        activity = Panel("진행 기록", "다운로드 과정의 판단과 결과를 순서대로 표시합니다.")
        self.badge = QLabel("준비")
        self.badge.setObjectName("statusBadge")
        activity.content.addWidget(self.badge, alignment=Qt.AlignmentFlag.AlignLeft)
        self.timeline = QListWidget()
        self.timeline.setObjectName("timeline")
        self.timeline.addItem("•  Zoom 녹화 링크를 기다리는 중")
        activity.content.addWidget(self.timeline, 1)
        library = Panel("최근 다운로드", "검증을 마치고 이 Mac에 저장된 파일입니다.")
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["제목", "상태", "저장일"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.itemSelectionChanged.connect(self._update_open_button)
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.empty_library = QLabel("아직 완료된 다운로드가 없습니다.")
        self.empty_library.setObjectName("secondaryText")
        self.empty_library.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        library.content.addWidget(self.empty_library)
        library.content.addWidget(self.table, 1)
        folder_actions = QHBoxLayout()
        self.open_selected_button = QPushButton("선택한 폴더 열기")
        self.open_selected_button.setEnabled(False)
        self.open_selected_button.clicked.connect(self.open_selected_in_finder)
        self.open_archive_button = QPushButton("전체 저장 폴더 열기")
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
            self.show_error("먼저 Zoom 녹화 링크를 입력해 주세요.")
            self.url.setFocus()
            return
        self.analyze_requested.emit(value)

    def begin(self, message: str = "녹화 페이지를 분석하는 중…") -> None:
        self.timeline.clear()
        self.completed_directory = None
        self.feedback.setText(message)
        self.download_status.setText("다운로드 준비 중")
        self.download_percent.setText("진행 중")
        self.download_file.setText("파일  확인 중")
        self.download_size.setText("받은 용량  —")
        self.download_speed.setText("속도  —")
        self.download_eta.setText("남은 시간  계산 중")
        self._set_badge("진행 중", "running")
        self.progress.setRange(0, 0)
        self.analyze.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.open_download_button.setEnabled(False)

    def finish(self, message: str, directory: Path | None = None, files: list[Path] | None = None) -> None:
        self.completed_directory = directory
        self.feedback.setText(message)
        self.download_status.setText("다운로드 완료")
        self.download_percent.setText("100%")
        self.progress.setRange(0, 100)
        self.progress.setValue(100)
        completed_files = files or []
        if completed_files:
            self.download_file.setText(f"파일  {', '.join(path.name for path in completed_files)}")
            total_bytes = sum(path.stat().st_size for path in completed_files if path.is_file())
            self.download_size.setText(f"받은 용량  {self._format_bytes(total_bytes)}")
        self.download_speed.setText("속도  완료")
        self.download_eta.setText("남은 시간  0초")
        self.open_download_button.setEnabled(bool(directory and directory.is_dir()))
        self._set_badge("완료", "success")
        self._set_idle_controls()

    def show_error(self, message: str) -> None:
        self.feedback.setText(message)
        self.download_status.setText("다운로드하지 못했습니다")
        self.download_percent.setText("—")
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self._set_badge("확인 필요", "error")
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
            self.download_percent.setText("진행 중")
        else:
            self.progress.setRange(0, 100)
            self.progress.setValue(round(progress.percentage))
            self.download_percent.setText(f"{progress.percentage:.0f}%")
        speed = progress.speed_bytes_per_second / (1024 * 1024)
        self.download_status.setText("파일 다운로드 중")
        self.download_file.setText(f"파일  {progress.filename}")
        self.download_size.setText(f"받은 용량  {self._format_bytes(progress.downloaded_bytes)}")
        self.download_speed.setText(f"속도  {speed:.1f} MB/s")
        eta = f"{progress.eta_seconds:.0f}초" if progress.eta_seconds is not None else "계산 중"
        self.download_eta.setText(f"남은 시간  {eta}")
        self.feedback.setText(f"{progress.filename} 파일을 다운로드하고 있습니다.")

    def refresh_library(self) -> None:
        self.recording_rows = list(self.repository.list_recordings()[:8]) if self.repository else []
        self.table.setRowCount(len(self.recording_rows))
        self.empty_library.setVisible(not self.recording_rows)
        self.table.setVisible(bool(self.recording_rows))
        self.open_selected_button.setEnabled(False)
        for row_index, row in enumerate(self.recording_rows):
            for column, key in enumerate(("title", "status", "created_at")):
                value = row[key] or ""
                if key == "status":
                    value = {"archived": "완료"}.get(str(value), value)
                self.table.setItem(row_index, column, QTableWidgetItem(str(value)))

    def open_selected_in_finder(self) -> None:
        row_index = self.table.currentRow()
        if row_index < 0 or row_index >= len(self.recording_rows):
            self.show_error("먼저 다운로드 항목을 선택해 주세요.")
            return
        directory = Path(self.recording_rows[row_index]["local_directory"] or "")
        if not directory.is_dir():
            self.show_error("선택한 폴더가 이 Mac에 없습니다.")
            return
        self._open_path(directory)

    def open_archive_folder(self) -> None:
        self.archive_root.mkdir(parents=True, exist_ok=True)
        self._open_path(self.archive_root)

    def open_download_folder(self) -> None:
        if not self.completed_directory or not self.completed_directory.is_dir():
            self.show_error("완료된 다운로드 폴더를 찾을 수 없습니다.")
            return
        self._open_path(self.completed_directory)

    def _open_path(self, path: Path) -> None:
        if not QDesktopServices.openUrl(QUrl.fromLocalFile(str(path.resolve()))):
            self.show_error("Finder에서 폴더를 열 수 없습니다.")

    def _update_open_button(self) -> None:
        self.open_selected_button.setEnabled(self.table.currentRow() >= 0)

    def _set_idle_controls(self) -> None:
        self.analyze.setEnabled(True)
        self.cancel_button.setEnabled(False)

    @staticmethod
    def _format_bytes(value: int) -> str:
        size = float(value)
        for unit in ("B", "KB", "MB", "GB"):
            if size < 1024 or unit == "GB":
                return f"{size:.1f} {unit}" if unit != "B" else f"{int(size)} B"
            size /= 1024
        return f"{size:.1f} GB"

    def _set_badge(self, text: str, state: str) -> None:
        self.badge.setText(text)
        self.badge.setProperty("state", state)
        self.badge.style().unpolish(self.badge)
        self.badge.style().polish(self.badge)
