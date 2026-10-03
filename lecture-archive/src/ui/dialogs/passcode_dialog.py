from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLineEdit


class PasscodeDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("녹화 암호 입력")
        self.input = QLineEdit()
        self.input.setEchoMode(QLineEdit.EchoMode.Password)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.button(QDialogButtonBox.StandardButton.Ok).setText("확인")
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText("취소")
        layout = QFormLayout(self)
        layout.addRow("암호", self.input)
        layout.addRow(buttons)

    def value(self) -> str:
        return self.input.text()
