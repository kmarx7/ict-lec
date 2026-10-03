from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from src.app.config import AppConfig
from src.ui.components import PageHeader, Panel


class SettingsPage(QWidget):
    def __init__(self, config: AppConfig | None = None) -> None:
        super().__init__()
        config = config or AppConfig()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(34, 30, 34, 30)
        layout.setSpacing(24)
        layout.addWidget(
            PageHeader(
                "Preferences",
                "Settings",
                "Review storage and acquisition safeguards.",
            )
        )
        storage = Panel("Archive location", "Verified files and metadata are stored here.")
        path = QLabel(str(config.download_dir))
        path.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        path.setObjectName("securityNote")
        storage.content.addWidget(path)
        safeguards = Panel("Privacy safeguards")
        note = QLabel(
            "Passcodes remain in session memory only. Cookies, OAuth tokens, authorization "
            "headers, and signed URLs are never written to metadata or activity logs."
        )
        note.setWordWrap(True)
        note.setObjectName("secondaryText")
        safeguards.content.addWidget(note)
        layout.addWidget(storage)
        layout.addWidget(safeguards)
        layout.addStretch()

