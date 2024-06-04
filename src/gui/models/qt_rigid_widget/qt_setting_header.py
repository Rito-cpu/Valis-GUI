import os

from src.core.pyqt_core import *
from src.core.app_config import IMG_RSC_PATH
from src.core.json.json_themes import Themes
from .styles import setting_label_template


class SettingHeader(QWidget):
    def __init__(
        self,
        label_text: str,
        tool_msg: str='',
        font_size: int=12,
        parent=None
    ):
        super().__init__()
        
        if parent is not None:
            self.setParent(parent)

        self._label_text = label_text
        self._tool_msg = tool_msg
        self._font_size = font_size
        self._message_window = None

        themes = Themes()
        self.themes = themes.items

        self._setup_widget()

        self.help_bttn.clicked.connect(self.show_window)

    def _setup_widget(self):
        icon_path = os.path.join(IMG_RSC_PATH, 'downloads/bqm.png')

        self.help_bttn = QToolButton(self)
        self.help_bttn.setObjectName('setting_help')
        self.help_bttn.setIcon(QIcon(icon_path))
        self.help_bttn.setIconSize(QSize(30, 30))
        self.help_bttn.setStyleSheet('background: none; border: none;')
        self.help_bttn.setCursor(Qt.CursorShape.PointingHandCursor)

        label_style = setting_label_template.format(
            font_color=self.themes['app_color']['main_bg'],
            size=self._font_size
        )

        setting_label = QLabel(self)
        setting_label.setObjectName('setting_label')
        setting_label.setText(self._label_text)
        setting_label.setStyleSheet(label_style)

        main_layout = QHBoxLayout(self)
        main_layout.setObjectName('main_layout')
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(20)
        main_layout.addWidget(self.help_bttn)
        main_layout.addWidget(setting_label)

    def show_window(self):        
        self._message_window = QMainWindow()
        self._message_window.setObjectName('message_window')
        self._message_window.setStyleSheet(f'background: {self.themes["app_color"]["main_bg"]};')

        central_widget = QWidget(self._message_window)
        central_widget.setObjectName('central_widget')

        label_style = setting_label_template.format(
            font_color=self.themes['app_color']['text_color'],
            size=self._font_size
        )

        title_text = QLabel(central_widget)
        title_text.setObjectName('title_text')
        title_text.setText(f'{self._label_text} Information:')
        title_text.setStyleSheet(f'color: {self.themes["app_color"]["main_bg"]}; font-size: 12px; background: {self.themes["app_color"]["blue_bg"]}; border-radius: 8px; padding: 8px;')
        title_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        message_label = QLabel(central_widget)
        message_label.setObjectName('message_label')
        message_label.setText(self._tool_msg)
        message_label.setStyleSheet(f'color: {self.themes["app_color"]["text_color"]}; font-size: 12px; border-radius: 8px; padding: 8px; border: 1px solid black;')
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        central_layout = QVBoxLayout(central_widget)
        central_layout.setObjectName('central_layout')
        central_layout.setContentsMargins(5, 5, 5, 5)
        central_layout.setSpacing(15)
        central_layout.addStretch(1)
        central_layout.addWidget(title_text, alignment=Qt.AlignmentFlag.AlignCenter)
        central_layout.addWidget(message_label, alignment=Qt.AlignmentFlag.AlignCenter)
        central_layout.addStretch(1)
        
        self._message_window.setCentralWidget(central_widget)
        self._message_window.setMinimumSize(400, 250)
        self._message_window.show()
