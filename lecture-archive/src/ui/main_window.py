from PySide6.QtGui import QFont
from PySide6.QtWidgets import QMainWindow

from src.ui.theme import APP_STYLESHEET
from src.ui.workspace_page import WorkspacePage


class MainWindow(QMainWindow):
    def __init__(self, repository=None) -> None:
        super().__init__()
        self.setWindowTitle("Lecture Archive")
        self.resize(1120, 760)
        self.setMinimumSize(860, 600)
        self.workspace = WorkspacePage(repository)
        self.setCentralWidget(self.workspace)
        self.setFont(QFont("SF Pro Text", 13))
        self.setStyleSheet(APP_STYLESHEET)

