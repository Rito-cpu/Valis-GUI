import os

from src.core.pyqt_core import *
from src.core.app_config import IMG_RSC_PATH
from src.core.json.json_themes import Themes
from .styles import setting_label_template
from .helper_window import HelperWindow


class SettingHeader(QWidget):
    def __init__(
        self,
        label_text: str,
        tool_msg: str,
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
        # TODO: Continue work here
        if self._message_window is not None:
            self._message_window.close()
            self._message_window = None

        curr_setting_name = self._label_text

        self._message_window = HelperWindow(
            setting_name=curr_setting_name,
            setting_msg=self._tool_msg
        )
        self._message_window.closed.connect(self.on_msg_close)
        self._message_window.show()

    def on_msg_close(self):
        print('Resetting the message window to None.')
        self._message_window = None
