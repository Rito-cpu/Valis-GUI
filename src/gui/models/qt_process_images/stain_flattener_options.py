from src.core.pyqt_core import *
from src.core.app_config import *
from src.core.keyword_store import STAIN_FLATTENER_KEY
from src.core.json.json_themes import Themes
from src.gui.models.qt_spinbox import QtNumEntry
from src.gui.models import PyToggle


class StainFlattener(QWidget):
    has_empty_dict: bool = True

    def __init__(
        self,
        font_size: int = 12,
        parent = None
    ):
        super().__init__()

        if parent is not None:
            self.parent = parent

        themes = Themes()
        self.themes = themes.items

        self._font_size = font_size

        self.label_style = f'font-size: {self._font_size}px; color: {self.themes["app_color"]["text_color"]};'

        self._setup_widget()

        if not self.has_empty_dict:
            self.num_colors_entry.valueChanged.connect(self.check_num_colors)
            self.max_colors_entry.valueChanged.connect(self.check_max_colors)
    
    def _setup_widget(self):
        options_frame = QFrame(self)
        options_frame.setObjectName('options_frame')
        options_frame.setFrameShape(QFrame.Shape.NoFrame)
        options_frame.setFrameShadow(QFrame.Shadow.Raised)

        main_layout = QVBoxLayout(self)
        main_layout.setObjectName('main_layout')
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.addWidget(options_frame, alignment=Qt.AlignmentFlag.AlignVCenter)

        data_dict = BF_PROCESSOR_OPTIONS[STAIN_FLATTENER_KEY]
        if data_dict:
            self.has_empty_dict = False

            left_frame = QFrame(options_frame)
            left_frame.setObjectName('left_frame')
            left_frame.setFrameShape(QFrame.Shape.NoFrame)
            left_frame.setFrameShadow(QFrame.Shadow.Raised)

            num_colors_label = QLabel(left_frame)
            num_colors_label.setObjectName('num_colors_label')
            num_colors_label.setText('N-Colors:')
            num_colors_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            num_colors_label.setStyleSheet(self.label_style)

            self.num_colors_entry = QtNumEntry(
                font_size=12,
                bg_color=self.themes["app_color"]["text_color"],
                parent=left_frame
            )
            self.num_colors_entry.setObjectName('num_colors_entry')
            self.num_colors_entry.setDecimals(0)
            self.num_colors_entry.setRange(0, 255)
            self.num_colors_entry.setSingleStep(1)
            self.num_colors_entry.setValue(data_dict['n_colors'])

            max_colors_label = QLabel(left_frame)
            max_colors_label.setObjectName('max_colors_label')
            max_colors_label.setText('Max Colors:')
            max_colors_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            max_colors_label.setStyleSheet(self.label_style)

            self.max_colors_entry = QtNumEntry(
                font_size=12,
                bg_color=self.themes["app_color"]["text_color"],
                parent=left_frame
            )
            self.max_colors_entry.setObjectName('max_colors_entry')
            self.max_colors_entry.setDecimals(0)
            self.max_colors_entry.setRange(0, 255)
            self.max_colors_entry.setSingleStep(1)
            self.max_colors_entry.setValue(data_dict['max_colors'])

            q_value_label = QLabel(left_frame)
            q_value_label.setObjectName('q_value_label')
            q_value_label.setText('q-Value:')
            q_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            q_value_label.setStyleSheet(self.label_style)

            self.q_entry = QtNumEntry(
                font_size=12,
                bg_color=self.themes["app_color"]["text_color"],
                parent=left_frame
            )
            self.q_entry.setObjectName('q_entry')
            self.q_entry.setDecimals(0)
            self.q_entry.setRange(0, 100)
            self.q_entry.setSingleStep(1)
            self.q_entry.setValue(data_dict['q'])

            left_layout = QFormLayout(left_frame)
            left_layout.setObjectName('left_layout')
            left_layout.setContentsMargins(0, 0, 0, 0)
            left_layout.setSpacing(15)
            left_layout.addRow(num_colors_label, self.num_colors_entry)
            left_layout.addRow(max_colors_label, self.max_colors_entry)
            left_layout.addRow(q_value_label, self.q_entry)

            right_frame = QFrame(options_frame)
            right_frame.setObjectName('right_frame')
            right_frame.setFrameShape(QFrame.Shape.NoFrame)
            right_frame.setFrameShadow(QFrame.Shadow.Raised)

            mask_label = QLabel(right_frame)
            mask_label.setObjectName('mask_label')
            mask_label.setText('With Mask:')
            mask_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            mask_label.setStyleSheet(self.label_style)

            self.mask_toggle = PyToggle(
                width=28,
                height=16,
                ellipse_y=2,
                bg_color = self.themes['app_color']['text_color'],
                circle_color = self.themes['app_color']['yellow_bg'],
                active_color = self.themes['app_color']['blue_bg'],
                parent=right_frame
            )
            self.mask_toggle.setObjectName('mask_toggle')
            self.mask_toggle.setChecked(data_dict['with_mask'])

            eq_label = QLabel(right_frame)
            eq_label.setObjectName('eq_label')
            eq_label.setText('Adaptive EQ:')
            eq_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            eq_label.setStyleSheet(self.label_style)

            self.eq_toggle = PyToggle(
                width=28,
                height=16,
                ellipse_y=2,
                bg_color = self.themes['app_color']['text_color'],
                circle_color = self.themes['app_color']['yellow_bg'],
                active_color = self.themes['app_color']['blue_bg'],
                parent=right_frame
            )
            self.eq_toggle.setObjectName('eq_toggle')
            self.eq_toggle.setChecked(data_dict['adaptive_eq'])

            right_layout = QFormLayout(right_frame)
            right_layout.setObjectName('right_layout')
            right_layout.setContentsMargins(0, 0, 0, 0)
            right_layout.setSpacing(15)
            right_layout.addRow(mask_label, self.mask_toggle)
            right_layout.addRow(eq_label, self.eq_toggle)

            options_layout = QHBoxLayout(options_frame)
            options_layout.setObjectName('options_layout')
            options_layout.setContentsMargins(0, 0, 0, 0)
            options_layout.setSpacing(15)
            options_layout.addWidget(left_frame, alignment=Qt.AlignmentFlag.AlignVCenter)
            options_layout.addWidget(right_frame, alignment=Qt.AlignmentFlag.AlignVCenter)
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

    def check_num_colors(self):
        num_colors = self.get_num_colors()
        max_colors = self.get_max_colors()

        if num_colors > max_colors:
            self.num_colors_entry.setValue(max_colors)

    def check_max_colors(self):
        num_colors = self.get_num_colors()
        max_colors = self.get_max_colors()

        if max_colors < num_colors:
            self.max_colors_entry.setValue(num_colors)

    def get_num_colors(self):
        if not self.has_empty_dict:
            return self.num_colors_entry.value()
        else:
            return None
        
    def get_max_colors(self):
        if not self.has_empty_dict:
            return self.max_colors_entry.value()
        else:
            return None
        
    def get_q_value(self):
        if not self.has_empty_dict:
            return self.q_entry.value()
        else:
            return None
        
    def get_mask(self):
        if not self.has_empty_dict:
            return self.mask_toggle.isChecked()
        else:
            return None
        
    def get_adaptive(self):
        if not self.has_empty_dict:
            return self.eq_toggle.isChecked()
        else:
            return None
        
    def get_data(self):
        num_colors = self.get_num_colors()
        max_colors = self.get_max_colors()
        q_value = self.get_q_value()
        use_mask = self.get_mask()
        use_adaptive = self.get_adaptive()

        value_dict = {
            'n_colors': num_colors,
            'max_colors': max_colors,
            'q': q_value,
            'with_mask': use_mask,
            'adaptive_eq': use_adaptive
        }

        return value_dict
