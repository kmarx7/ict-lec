from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class SourcePage(QWidget):
    analyze_requested = Signal(str)
    import_requested = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("Download a recording")
        title.setObjectName("pageTitle")
        description = QLabel("Enter a Zoom Cloud Recording link you are authorized to access.")
        self.url = QLineEdit()
        self.url.setPlaceholderText("https://…zoom.us/rec/share/…")
        self.analyze = QPushButton("Analyze")
        self.analyze.setDefault(True)
        self.analyze.clicked.connect(lambda: self.analyze_requested.emit(self.url.text().strip()))
        self.import_button = QPushButton("Import Local File…")
        self.import_button.clicked.connect(self._pick_file)
        row = QHBoxLayout()
        row.addWidget(self.url, 1)
        row.addWidget(self.analyze)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addSpacing(16)
        layout.addWidget(QLabel("Zoom Recording URL"))
        layout.addLayout(row)
        layout.addSpacing(8)
        layout.addWidget(self.import_button, alignment=__import__("PySide6").QtCore.Qt.AlignmentFlag.AlignLeft)
        layout.addStretch()

    def _pick_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Import Recording", "", "Media (*.mp4 *.m4a *.mov *.vtt);;All Files (*)")
        if path:
            self.import_requested.emit(path)

