# this file is to create a window to test the functionality of the progress bar and initialize it properly.
# It will likely need to be changed to fit into the GUI architecture.


import sys

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QPlainTextEdit, QVBoxLayout, QProgressBar
from PyQt6.QtCore import QProcess, QThread
import completion_checker


class Window(QWidget):
    def __init__(self, path: str, steps_dict: dict, sample_list: list, parent=None,):
        super().__init__(parent)
        self.t = None
        self.resize(500, 500)
        self.setWindowTitle("Valis")
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)
        self.value = 0
        self.path = path
        self.steps_dict = steps_dict
        self.sample_list = sample_list

        self.b = QProgressBar()
        self.b.setRange(0, len(steps_dict) + 2)
        self.b.setTextVisible(True)

        layout = QVBoxLayout()
        layout.addWidget(self.b)
        self.setLayout(layout)

    def create_thread(self):
        self.t = completion_checker.Thread(self.path, self.steps_dict, self.sample_list)
        self.t.dir_change.connect(self.advance)
        self.t.start()

    def advance(self, value):
        self.b.setValue(value)


def init_prog_bar(path: str, steps_dict: dict, sample_list: list):
    app = QApplication(sys.argv)
    window = Window(path, steps_dict, sample_list)
    window.create_thread()
    window.show()
    sys.exit(app.exec())
