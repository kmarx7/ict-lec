from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class RecordingPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Recording details"))
        layout.addStretch()

