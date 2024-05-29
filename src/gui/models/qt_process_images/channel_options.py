from src.core.pyqt_core import *
from src.core.app_config import IF_PROCESSOR_OPTIONS
from src.core.json.json_themes import Themes
from src.core.keyword_store import CHANNEL_GETTER_KEY
from src.gui.models import QtComboBox, PyToggle


class ChannelGetter(QWidget):
    has_empty_dict: bool = True

    def __init__(
        self,
        font_size: int = 12,
        parent=None
    ):
        super().__init__()

        if parent is not None:
            self.parent = parent

        themes = Themes()
        self.themes = themes.items

        self._font_size = font_size

        self.label_style = f'font-size: {self._font_size}; color: {self.themes["app_color"]["text_color"]};'

        self._setup_widget()

    def _setup_widget(self):
        options_frame = QFrame(self)
        options_frame.setObjectName('channel_frame')
        options_frame.setFrameShape(QFrame.Shape.NoFrame)
        options_frame.setFrameShadow(QFrame.Shadow.Raised)

        main_layout = QVBoxLayout(self)
        main_layout.setObjectName('main_layout')
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.addWidget(options_frame, alignment=Qt.AlignmentFlag.AlignVCenter)

        data_dict = IF_PROCESSOR_OPTIONS[CHANNEL_GETTER_KEY]
        if data_dict:
            self.has_empty_dict = False
            channel_label = QLabel(options_frame)
            channel_label.setObjectName('channel_label')
            channel_label.setText('Channel:')
            channel_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            channel_label.setStyleSheet(self.label_style)

            self.channel_combo = QtComboBox(
                bg_color=self.themes["app_color"]["dark_one"],
                text_color=self.themes["app_color"]["text_color"],
                parent=options_frame
            )
            self.channel_combo.setObjectName('channel_combo')
            self.channel_combo.addItems([data_dict['channel']])
            self.channel_combo.setFixedHeight(30)
            self.channel_combo.setMinimumWidth(125)

            adaptive_label = QLabel(options_frame)
            adaptive_label.setObjectName('adaptive_label')
            adaptive_label.setText('Adaptive EQ:')
            adaptive_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            adaptive_label.setStyleSheet(self.label_style)

            self.adaptive_toggle = PyToggle(
                width=28,
                height=16,
                ellipse_y=2,
                bg_color = self.themes['app_color']['text_color'],
                circle_color = self.themes['app_color']['yellow_bg'],
                active_color = self.themes['app_color']['blue_bg'],
                parent=options_frame
            )
            self.adaptive_toggle.setObjectName('adaptive_toggle')
            self.adaptive_toggle.setChecked(data_dict['adaptive_eq'])

            options_layout = QFormLayout(options_frame)
            options_layout.setObjectName('adaptive_layout')
            options_layout.setContentsMargins(0, 0, 0, 0)
            options_layout.setSpacing(15)
            options_layout.addRow(channel_label, self.channel_combo)
            options_layout.addRow(adaptive_label, self.adaptive_toggle)
        else:
            empty_label = QLabel(options_frame)
            empty_label.setObjectName('empty_label')
            empty_label.setText('No Settings Available')
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setStyleSheet(self.label_style)

            options_layout = QVBoxLayout(options_frame)
            options_layout.setObjectName('options_layout')
            options_layout.setContentsMargins(0, 0, 0, 0)
            options_layout.addWidget(empty_label, alignment=Qt.AlignmentFlag.AlignCenter)

    def get_channel(self):
        if not self.has_empty_dict:
            return self.channel_combo.currentText()
        else:
            return None
    
    def get_adaptive_eq(self):
        if not self.has_empty_dict:
            return self.adaptive_toggle.isChecked()
        else:
            return None

    def get_data(self):
        current_channel = self.get_channel()
        use_adaptive_eq = self.get_adaptive_eq()
        
        value_dict = {
            'channel': current_channel,
            'adaptive_eq': use_adaptive_eq
        }

        return value_dict
