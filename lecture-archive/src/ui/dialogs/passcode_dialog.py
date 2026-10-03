from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLineEdit


class PasscodeDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Recording Passcode")
        self.input = QLineEdit()
        self.input.setEchoMode(QLineEdit.EchoMode.Password)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout = QFormLayout(self)
        layout.addRow("Passcode", self.input)
        layout.addRow(buttons)

    def value(self) -> str:
        return self.input.text()

