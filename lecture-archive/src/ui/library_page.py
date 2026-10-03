from PySide6.QtWidgets import QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget


class LibraryPage(QWidget):
    def __init__(self, repository=None) -> None:
        super().__init__()
        self.repository = repository
        layout = QVBoxLayout(self)
        title = QLabel("Library")
        title.setObjectName("pageTitle")
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Title", "Source", "Status", "Created"])
        layout.addWidget(title)
        layout.addWidget(self.table)

    def refresh(self) -> None:
        rows = self.repository.list_recordings() if self.repository else []
        self.table.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            for column, key in enumerate(("title", "source", "status", "created_at")):
                self.table.setItem(row_index, column, QTableWidgetItem(str(row[key] or "")))

