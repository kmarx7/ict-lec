from PySide6.QtWidgets import QLabel, QListWidget, QProgressBar, QVBoxLayout, QWidget

from src.ui.components import PageHeader, Panel


class ActivityPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(34, 30, 34, 30)
        layout.setSpacing(20)
        layout.addWidget(PageHeader("Acquisition loop", "Activity", "Observe, plan, execute, and verify — every decision remains visible."))
        summary = Panel()
        self.badge = QLabel("READY")
        self.badge.setObjectName("statusBadge")
        self.status = QLabel("Waiting for a recording")
        self.status.setObjectName("panelTitle")
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.hide()
        summary.content.addWidget(self.badge)
        summary.content.addWidget(self.status)
        summary.content.addWidget(self.progress)
        self.timeline = QListWidget()
        self.timeline.setObjectName("timeline")
        section = QLabel("TIMELINE")
        section.setObjectName("fieldLabel")
        layout.addWidget(summary)
        layout.addWidget(section)
        layout.addWidget(self.timeline, 1)

    def add_event(self, event) -> None:
        symbol = "✓" if event.event_type.value in {"ACTION_COMPLETED", "GOAL_REACHED"} else "•"
        if event.event_type.value in {"ACTION_FAILED", "TERMINATED"}:
            symbol = "✕"
        self.timeline.addItem(f"{symbol}  {event.message}")
        self.timeline.scrollToBottom()
        self.status.setText(event.message)
        if event.event_type.value == "ACTION_STARTED":
            self.badge.setText("RUNNING")
            self.progress.setRange(0, 0)
            self.progress.show()
        elif event.event_type.value in {"ACTION_FAILED", "GOAL_REACHED", "TERMINATED"}:
            self.badge.setText("COMPLETE" if event.event_type.value == "GOAL_REACHED" else "STOPPED")
            self.progress.hide()

    def update_progress(self, progress) -> None:
        self.progress.show()
        if progress.percentage is None:
            self.progress.setRange(0, 0)
        else:
            self.progress.setRange(0, 100)
            self.progress.setValue(round(progress.percentage))
        speed = progress.speed_bytes_per_second / (1024 * 1024)
        eta = f" · ETA {progress.eta_seconds:.0f}s" if progress.eta_seconds is not None else ""
        self.status.setText(f"{progress.filename} · {progress.downloaded_bytes / (1024 * 1024):.1f} MB · {speed:.1f} MB/s{eta}")

