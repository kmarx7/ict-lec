from PySide6.QtWidgets import QHBoxLayout, QListWidget, QMainWindow, QStackedWidget, QWidget

from src.ui.activity_page import ActivityPage
from src.ui.library_page import LibraryPage
from src.ui.source_page import SourcePage


class MainWindow(QMainWindow):
    def __init__(self, repository=None) -> None:
        super().__init__()
        self.setWindowTitle("Lecture Archive")
        self.resize(900, 600)
        root = QWidget()
        layout = QHBoxLayout(root)
        self.navigation = QListWidget()
        self.navigation.setFixedWidth(150)
        self.navigation.addItems(["Download", "Activity", "Library", "Settings"])
        self.pages = QStackedWidget()
        self.source_page = SourcePage()
        self.activity_page = ActivityPage()
        self.library_page = LibraryPage(repository)
        self.pages.addWidget(self.source_page)
        self.pages.addWidget(self.activity_page)
        self.pages.addWidget(self.library_page)
        self.pages.addWidget(QWidget())
        self.navigation.currentRowChanged.connect(self.pages.setCurrentIndex)
        self.navigation.setCurrentRow(0)
        layout.addWidget(self.navigation)
        layout.addWidget(self.pages, 1)
        self.setCentralWidget(root)
        self.setStyleSheet("""
            QMainWindow { background: #f4f4f4; }
            QListWidget { border: 0; background: #e9e9e9; padding: 8px; }
            QListWidget::item { padding: 8px; border-radius: 5px; }
            QListWidget::item:selected { background: #d2d2d2; color: #111; }
            #pageTitle { font-size: 22px; font-weight: 600; margin-bottom: 4px; }
            QLineEdit { padding: 7px; border: 1px solid #aaa; border-radius: 5px; background: white; }
            QPushButton { padding: 7px 14px; }
        """)

