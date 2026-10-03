from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout


class LoginDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Zoom 로그인")
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout = QVBoxLayout(self)
        buttons.button(QDialogButtonBox.StandardButton.Ok).setText("계속")
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText("취소")
        layout.addWidget(QLabel("브라우저에서 로그인을 마친 뒤 '계속'을 눌러 주세요."))
        layout.addWidget(buttons)
