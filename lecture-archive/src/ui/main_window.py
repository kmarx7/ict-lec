from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from src.ui.activity_page import ActivityPage
from src.ui.library_page import LibraryPage
from src.ui.settings_page import SettingsPage
from src.ui.source_page import SourcePage
from src.ui.theme import APP_STYLESHEET


class MainWindow(QMainWindow):
    def __init__(self, repository=None) -> None:
        super().__init__()
        self.setWindowTitle("Lecture Archive")
        self.resize(1080, 720)
        self.setMinimumSize(840, 560)
        root = QWidget()
        root.setObjectName("appRoot")
        layout = QHBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(188)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(14, 18, 14, 16)
        sidebar_layout.setSpacing(8)
        brand_row = QHBoxLayout()
        mark = QLabel("LA")
        mark.setObjectName("brandMark")
        mark.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mark.setFixedSize(34, 34)
        brand_text = QVBoxLayout()
        brand_text.setSpacing(0)
        name = QLabel("Lecture Archive")
        name.setObjectName("brandName")
        caption = QLabel("LOCAL LIBRARY")
        caption.setObjectName("brandCaption")
        brand_text.addWidget(name)
        brand_text.addWidget(caption)
        brand_row.addWidget(mark)
        brand_row.addLayout(brand_text)
        sidebar_layout.addLayout(brand_row)
        sidebar_layout.addSpacing(16)
        self.navigation = QListWidget()
        self.navigation.setObjectName("navigation")
        self.navigation.setIconSize(QSize(16, 16))
        for text in ("＋  Download", "◷  Activity", "▤  Library", "⚙  Settings"):
            item = QListWidgetItem(text)
            item.setSizeHint(QSize(150, 40))
            self.navigation.addItem(item)
        sidebar_layout.addWidget(self.navigation)
        sidebar_layout.addStretch()
        privacy = QLabel("PRIVATE · ON DEVICE")
        privacy.setObjectName("brandCaption")
        sidebar_layout.addWidget(privacy)
        self.pages = QStackedWidget()
        self.source_page = SourcePage()
        self.activity_page = ActivityPage()
        self.library_page = LibraryPage(repository)
        self.settings_page = SettingsPage()
        for page in (self.source_page, self.activity_page, self.library_page, self.settings_page):
            self.pages.addWidget(page)
        self.navigation.currentRowChanged.connect(self.pages.setCurrentIndex)
        self.navigation.setCurrentRow(0)
        layout.addWidget(sidebar)
        layout.addWidget(self.pages, 1)
        self.setCentralWidget(root)
        self.setFont(QFont("SF Pro Text", 13))
        self.setStyleSheet(APP_STYLESHEET)

