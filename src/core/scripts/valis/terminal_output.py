from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QPlainTextEdit, QVBoxLayout
from PyQt6.QtCore import QProcess
import sys


class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.register_button = QPushButton("Register")
        self.register_button.pressed.connect(self.register)
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)
        self.resize(500, 500)
        self.p = None

        layout = QVBoxLayout()
        layout.addWidget(self.register_button)
        layout.addWidget(self.text)
        self.setLayout(layout)

    def register(self):
        self.text.appendPlainText("Starting Valis")
        self.p = QProcess()
        self.p.readyReadStandardError.connect(self.read_stderr)
        self.p.finished.connect(lambda: self.text.appendPlainText("Finished, you may now close this window"))
        self.p.start("python3", ['on_register_press.py'])

    def read_stderr(self):
        error = self.p.readAllStandardError()
        readout = bytes(error).decode("utf8")
        self.text.appendPlainText(readout)

    def read_stdout(self):
        out = self.p.readAllStandardError()
        readout = bytes(out).decode("utf8")
        self.text.appendPlainText(readout)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec())
