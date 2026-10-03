from PySide6.QtWidgets import QLabel, QListWidget, QProgressBar, QVBoxLayout, QWidget


class ActivityPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("Activity")
        title.setObjectName("pageTitle")
        self.status = QLabel("Ready")
        self.timeline = QListWidget()
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.hide()
        layout.addWidget(title)
        layout.addWidget(self.status)
        layout.addWidget(self.progress)
        layout.addWidget(self.timeline, 1)

    def add_event(self, event) -> None:
        symbol = "✓" if event.event_type.value in {"ACTION_COMPLETED", "GOAL_REACHED"} else "•"
        if event.event_type.value in {"ACTION_FAILED", "TERMINATED"}:
            symbol = "✕"
        self.timeline.addItem(f"{symbol} {event.message}")
        self.status.setText(event.message)
        if event.event_type.value == "ACTION_STARTED":
            self.progress.setRange(0, 0)
            self.progress.show()
        elif event.event_type.value in {"ACTION_FAILED", "GOAL_REACHED", "TERMINATED"}:
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
        self.status.setText(
            f"{progress.filename} · {progress.downloaded_bytes / (1024 * 1024):.1f} MB"
            f" · {speed:.1f} MB/s{eta}"
        )
