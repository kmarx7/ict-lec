from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.ui.components import PageHeader, Panel


class SourcePage(QWidget):
    analyze_requested = Signal(str)
    import_requested = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(34, 30, 34, 30)
        layout.setSpacing(24)
        layout.addWidget(PageHeader("New acquisition", "Download a recording", "Archive a Zoom Cloud Recording through an authorized download path."))
        panel = Panel("Zoom recording link", "Paste a share or playback URL. Lecture Archive will inspect access before acting.")
        self.url = QLineEdit()
        self.url.setPlaceholderText("https://us06web.zoom.us/rec/share/…")
        self.url.setClearButtonEnabled(True)
        self.url.returnPressed.connect(self._analyze)
        self.analyze = QPushButton("Analyze recording")
        self.analyze.setObjectName("primaryButton")
        self.analyze.setDefault(True)
        self.analyze.clicked.connect(self._analyze)
        self.import_button = QPushButton("Import local file…")
        self.import_button.setObjectName("quietButton")
        self.import_button.clicked.connect(self._pick_file)
        row = QHBoxLayout()
        row.setSpacing(10)
        row.addWidget(self.url, 1)
        row.addWidget(self.analyze)
        field_label = QLabel("RECORDING URL")
        field_label.setObjectName("fieldLabel")
        panel.content.addWidget(field_label)
        panel.content.addLayout(row)
        panel.content.addWidget(self.import_button, alignment=Qt.AlignmentFlag.AlignLeft)
        security = QLabel("⌁  Permission-aware by design  ·  No stream extraction  ·  No stored credentials")
        security.setObjectName("securityNote")
        security.setWordWrap(True)
        layout.addWidget(panel)
        layout.addWidget(security)
        layout.addStretch()

    def _analyze(self) -> None:
        value = self.url.text().strip()
        if value:
            self.analyze_requested.emit(value)

    def _pick_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Import Recording", "", "Media (*.mp4 *.m4a *.mov *.vtt);;All Files (*)")
        if path:
            self.import_requested.emit(path)

