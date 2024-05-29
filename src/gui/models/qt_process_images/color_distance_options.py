from src.core.pyqt_core import *
from src.core.app_config import *
from src.core.keyword_store import BG_COLOR_DISTANCE_KEY
from src.core.json.json_themes import Themes
from src.gui.models.qt_spinbox import QtNumEntry


class BgColorDistance(QWidget):
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
        options_frame.setObjectName('options_frame')
        options_frame.setFrameShape(QFrame.Shape.NoFrame)
        options_frame.setFrameShadow(QFrame.Shadow.Raised)

        main_layout = QVBoxLayout(self)
        main_layout.setObjectName('main_layout')
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.addWidget(options_frame, alignment=Qt.AlignmentFlag.AlignVCenter)

        data_dict = BF_PROCESSOR_OPTIONS[BG_COLOR_DISTANCE_KEY]
        if data_dict:
            self.has_empty_dict = False

            brightness_label = QLabel(options_frame)
            brightness_label.setObjectName('brightness_label')
            brightness_label.setText('Brightness:')
            brightness_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            brightness_label.setStyleSheet(self.label_style)

            self.brightness_box = QtNumEntry(
                font_size=12,
                bg_color=self.themes["app_color"]["text_color"],
                parent=options_frame
            )
            self.brightness_box.setObjectName('brightness_box')
            self.brightness_box.setMinimumSize(30, 30)
            self.brightness_box.setDecimals(2)
            self.brightness_box.setRange(0, 10)
            self.brightness_box.setSingleStep(0.01)
            self.brightness_box.setValue(data_dict['brightness_q'])

            options_layout = QFormLayout(options_frame)
            options_layout.setContentsMargins(0, 0, 0, 0)
            options_layout.setSpacing(15)
            options_layout.addRow(brightness_label, self.brightness_box)
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

    def get_brightness_value(self):
        if not self.has_empty_dict:
            return self.brightness_box.value()
        else:
            return None
        
    def get_data(self):
        brightness_value = self.get_brightness_value()

        value_dict = {
            'brightness_q': brightness_value
        }

        return value_dict
