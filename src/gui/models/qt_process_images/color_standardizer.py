from src.core.pyqt_core import *
from src.core.app_config import *
from src.core.keyword_store import COLORFUL_STANDARDIZER_KEY
from src.core.json.json_themes import Themes
from src.gui.models.qt_spinbox import QtNumEntry
from src.gui.models import PyToggle


class ColorfulStandardizer(QWidget):
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

        data_dict = BF_PROCESSOR_OPTIONS[COLORFUL_STANDARDIZER_KEY]
        if data_dict:
            self.has_empty_dict = False

            left_container = QFrame(options_frame)
            left_container.setObjectName('left_container')
            left_container.setFrameShape(QFrame.Shape.NoFrame)
            left_container.setFrameShadow(QFrame.Shadow.Raised)

            invert_label = QLabel(left_container)
            invert_label.setObjectName('invert_label')
            invert_label.setText('Invert:')
            invert_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            invert_label.setStyleSheet(self.label_style)

            self.invert_toggle = PyToggle(
                width=28,
                height=16,
                ellipse_y=2,
                bg_color = self.themes['app_color']['text_color'],
                circle_color = self.themes['app_color']['yellow_bg'],
                active_color = self.themes['app_color']['blue_bg'],
                parent=left_container
            )
            self.invert_toggle.setObjectName('invert_toggle')
            self.invert_toggle.setChecked(data_dict['invert'])

            adaptive_label = QLabel(left_container)
            adaptive_label.setObjectName('adaptive_label')
            adaptive_label.setText('Adaptive EQ:')
            adaptive_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            adaptive_label.setStyleSheet(self.label_style)

            self.adaptive_eq_toggle = PyToggle(
                width=28,
                height=16,
                ellipse_y=2,
                bg_color = self.themes['app_color']['text_color'],
                circle_color = self.themes['app_color']['yellow_bg'],
                active_color = self.themes['app_color']['blue_bg'],
                parent=left_container
            )
            self.adaptive_eq_toggle.setObjectName('adaptive_eq_toggle')
            self.adaptive_eq_toggle.setChecked(data_dict['adaptive_eq'])

            left_form = QFormLayout(left_container)
            left_form.setObjectName('left_form')
            left_form.setContentsMargins(0, 0, 0, 0)
            left_form.setSpacing(15)
            left_form.addRow(invert_label, self.invert_toggle)
            left_form.addRow(adaptive_label, self.adaptive_eq_toggle)

            right_container = QFrame(options_frame)
            right_container.setObjectName('right_container')
            right_container.setFrameShape(QFrame.Shape.NoFrame)
            right_container.setFrameShadow(QFrame.Shadow.Raised)

            c_label = QLabel(right_container)
            c_label.setObjectName('c_label')
            c_label.setText('C Value:')
            c_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            c_label.setStyleSheet(self.label_style)

            self.c_value_box = QtNumEntry(
                font_size=12,
                bg_color=self.themes["app_color"]["text_color"],
                parent=right_container
            )
            self.c_value_box.setObjectName('c_value_box')
            self.c_value_box.setMinimumSize(30, 30)
            self.c_value_box.setDecimals(2)
            self.c_value_box.setRange(0, 100)
            self.c_value_box.setSingleStep(0.01)
            self.c_value_box.setValue(data_dict['c'])

            right_form = QFormLayout(right_container)
            right_form.setObjectName('right_form')
            right_form.setContentsMargins(0, 0, 0, 0)
            right_form.setSpacing(15)
            right_form.addRow(c_label, self.c_value_box)

            options_gridlay = QGridLayout(options_frame)
            options_gridlay.setObjectName('options_gridlay')
            options_gridlay.setContentsMargins(0, 0, 0, 0)
            options_gridlay.addWidget(left_container, 0, 0, 1, 1)
            options_gridlay.addWidget(right_container, 0, 1, 1, 1)
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

    def get_c_value(self):
        if not self.has_empty_dict:
            return self.c_value_box.value()
        else:
            return None

    def get_invert(self):
        if not self.has_empty_dict:
            return self.invert_toggle.isChecked()
        else:
            return None
        
    def get_adaptive(self):
        if not self.has_empty_dict:
            return self.adaptive_eq_toggle.isChecked()
        else:
            return None

    def get_data(self):
        c_value = self.get_c_value()
        is_inverted = self.get_invert()
        adaptive_eq = self.get_adaptive()

        value_dict = {
            'c': c_value,
            'invert': is_inverted,
            'adaptive_eq': adaptive_eq
        }

        return value_dict
