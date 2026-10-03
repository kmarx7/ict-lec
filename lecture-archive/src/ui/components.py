from PySide6.QtWidgets import QFrame, QLabel, QSizePolicy, QVBoxLayout, QWidget


class PageHeader(QWidget):
    def __init__(self, eyebrow: str, title: str, description: str) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        eyebrow_label = QLabel(eyebrow.upper())
        eyebrow_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        eyebrow_label.setObjectName("eyebrow")
        title_label = QLabel(title)
        title_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        title_label.setObjectName("pageTitle")
        description_label = QLabel(description)
        description_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        description_label.setObjectName("pageDescription")
        description_label.setWordWrap(True)
        layout.addWidget(eyebrow_label)
        layout.addWidget(title_label)
        layout.addWidget(description_label)


class Panel(QFrame):
    def __init__(self, title: str | None = None, description: str | None = None) -> None:
        super().__init__()
        self.setObjectName("panel")
        self.content = QVBoxLayout(self)
        self.content.setContentsMargins(20, 18, 20, 20)
        self.content.setSpacing(12)
        if title:
            label = QLabel(title)
            label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
            label.setObjectName("panelTitle")
            self.content.addWidget(label)
        if description:
            label = QLabel(description)
            label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
            label.setObjectName("panelDescription")
            label.setWordWrap(True)
            self.content.addWidget(label)
