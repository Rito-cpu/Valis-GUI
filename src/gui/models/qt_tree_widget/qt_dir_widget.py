from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.gui.models import PyToggle


class DirectoryWidget(QWidget):
    def __init__(
        self,
        dir_name: str = None,
        font_size: int = 13,
        parent=None
    ):
        super().__init__()

        if parent is not None:
            self.setParent(parent)

        self._file_name = dir_name
        self._font_size = font_size

        themes = Themes()
        self.themes = themes.items

        self._setup_widget()

    def _setup_widget(self):
        content_frame = QFrame(self)
        content_frame.setObjectName('content_frame')
        content_frame.setFrameShape(QFrame.Shape.NoFrame)
        content_frame.setFrameShadow(QFrame.Shadow.Plain)

        self.file_label = QLabel(self)
        self.file_label.setObjectName('file_label')
        self.file_label.setText(self._file_name)
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_label.setStyleSheet(f'color: {self.themes["app_color"]["text_color"]}; font-size: {self._font_size}px; font-weight: bold;')

        sorted_frame = QFrame(self)
        sorted_frame.setFrameShape(QFrame.Shape.NoFrame)
        sorted_frame.setFrameShadow(QFrame.Shadow.Plain)

        sorted_label = QLabel(sorted_frame)
        sorted_label.setObjectName('sorted_label')
        sorted_label.setText('Sorted:')
        sorted_label.setStyleSheet(f'color: {self.themes["app_color"]["text_color"]}; font-size: 10px;')

        self.sorted_toggle = PyToggle(
            width=28,
            height=16,
            ellipse_y=2,
            bg_color = self.themes['app_color']['text_color'],
            circle_color = self.themes['app_color']['yellow_bg'],
            active_color = self.themes['app_color']['blue_bg'],
            parent=sorted_frame
        )
        self.sorted_toggle.setObjectName('sorted_toggle')
        self.sorted_toggle.setChecked(False)

        sorted_lay = QHBoxLayout(sorted_frame)
        sorted_lay.setContentsMargins(0, 0, 0, 0)
        sorted_lay.setSpacing(5)
        sorted_lay.addWidget(sorted_label, alignment=Qt.AlignmentFlag.AlignCenter)
        sorted_lay.addWidget(self.sorted_toggle)

        content_layout = QVBoxLayout(content_frame)
        content_layout.setObjectName('content_layout')
        content_layout.setContentsMargins(5, 8, 5, 8)
        content_layout.setSpacing(5)
        content_layout.addWidget(self.file_label, alignment=Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(sorted_frame, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout = QVBoxLayout(self)
        main_layout.setObjectName('main_layout')
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(content_frame)

    def set_text(self, text: str):
        self.file_label.setText(text)
    
    def get_text(self):
        return self.file_label.text()
    
    def is_sorted(self):
        return self.sorted_toggle.isChecked()
