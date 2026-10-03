from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.ui.components import PageHeader


class LibraryPage(QWidget):
    def __init__(self, repository=None) -> None:
        super().__init__()
        self.repository = repository
        layout = QVBoxLayout(self)
        layout.setContentsMargins(34, 30, 34, 30)
        layout.setSpacing(20)
        layout.addWidget(PageHeader("Archive", "Library", "Verified recordings stored on this Mac."))
        section = QLabel("RECORDINGS")
        section.setObjectName("fieldLabel")
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Title", "Source", "Status", "Created"])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().hide()
        self.table.verticalHeader().setDefaultSectionSize(42)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for index in range(1, 4):
            header.setSectionResizeMode(index, QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(section)
        layout.addWidget(self.table)

    def refresh(self) -> None:
        rows = self.repository.list_recordings() if self.repository else []
        self.table.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            for column, key in enumerate(("title", "source", "status", "created_at")):
                self.table.setItem(row_index, column, QTableWidgetItem(str(row[key] or "")))

