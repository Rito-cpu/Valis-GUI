from src.core.pyqt_core import *
from src.core.app_config import *
from src.core.keyword_store import HEDECONVOLUTION_KEY
from src.core.json.json_themes import Themes
from src.gui.models import QtComboBox
from src.gui.models.qt_spinbox import QtNumEntry


class HEDOptions(QWidget):
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

        self.label_style = f'font-size: {self._font_size}px; color: {self.themes["app_color"]["text_color"]};'

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

        data_dict = BF_PROCESSOR_OPTIONS[HEDECONVOLUTION_KEY]
        if data_dict:
            self.has_empty_dict = False

            left_frame = QFrame(options_frame)
            left_frame.setObjectName('left_frame')
            left_frame.setFrameShape(QFrame.Shape.NoFrame)
            left_frame.setFrameShadow(QFrame.Shadow.Raised)

            stain_label = QLabel(left_frame)
            stain_label.setObjectName('stain_label')
            stain_label.setText('Stain:')
            stain_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            stain_label.setStyleSheet(self.label_style)

            self.stain_combo = QtComboBox(
                bg_color=self.themes["app_color"]["dark_one"],
                text_color=self.themes["app_color"]["text_color"],
                parent=left_frame
            )
            self.stain_combo.setObjectName('stain_combo')
            self.stain_combo.addItems([data_dict['stain']])
            self.stain_combo.setFixedHeight(30)
            self.stain_combo.setMinimumWidth(125)

            io_label = QLabel(left_frame)
            io_label.setObjectName('io_label')
            io_label.setText('IO:')
            io_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            io_label.setStyleSheet(self.label_style)

            self.io_entry = QtNumEntry(
                font_size=12,
                bg_color=self.themes["app_color"]["text_color"],
                parent=left_frame
            )
            self.io_entry.setObjectName('io_entry')
            self.io_entry.setDecimals(0)
            self.io_entry.setRange(0, 500)
            self.io_entry.setValue(data_dict['Io'])

            left_layout = QFormLayout(left_frame)
            left_layout.setObjectName('left_layout')
            left_layout.setContentsMargins(0, 0, 0, 0)
            left_layout.setSpacing(15)
            left_layout.addRow(stain_label, self.stain_combo)
            left_layout.addRow(io_label, self.io_entry)

            right_frame = QFrame(options_frame)
            right_frame.setObjectName('right_frame')
            right_frame.setFrameShape(QFrame.Shape.NoFrame)
            right_frame.setFrameShadow(QFrame.Shadow.Raised)

            alpha_label = QLabel(right_frame)
            alpha_label.setObjectName('alpha_label')
            alpha_label.setText('Alpha:')
            alpha_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            alpha_label.setStyleSheet(self.label_style)

            self.alpha_entry = QtNumEntry(
                font_size=12,
                bg_color=self.themes["app_color"]["text_color"],
                parent=right_frame
            )
            self.alpha_entry.setObjectName('alpha_entry')
            self.alpha_entry.setDecimals(2)
            self.alpha_entry.setRange(0, 1)
            self.alpha_entry.setSingleStep(0.01)
            self.alpha_entry.setValue(data_dict['alpha'])

            beta_label = QLabel(right_frame)
            beta_label.setObjectName('beta_label')
            beta_label.setText('Beta:')
            beta_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            beta_label.setStyleSheet(self.label_style)

            self.beta_entry = QtNumEntry(
                font_size=12,
                bg_color=self.themes["app_color"]["text_color"],
                parent=right_frame
            )
            self.beta_entry.setObjectName('beta_entry')
            self.beta_entry.setDecimals(2)
            self.beta_entry.setRange(0, 1)
            self.beta_entry.setSingleStep(0.01)
            self.beta_entry.setValue(data_dict['beta'])

            right_layout = QFormLayout(right_frame)
            right_layout.setObjectName('right_layout')
            right_layout.setContentsMargins(0, 0, 0, 0)
            right_layout.setSpacing(15)
            right_layout.addRow(alpha_label, self.alpha_entry)
            right_layout.addRow(beta_label, self.beta_entry)

            options_layout = QGridLayout(options_frame)
            options_layout.setObjectName('options_layout')
            options_layout.setContentsMargins(0, 0, 0, 0)
            options_layout.setSpacing(15)
            options_layout.addWidget(left_frame, 0, 0, 1, 1)
            options_layout.addWidget(right_frame, 0, 1, 1, 1)
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

    def get_stain(self):
        if not self.has_empty_dict:
            return self.stain_combo.currentText()
        else:
            return None
        
    def get_io(self):
        if not self.has_empty_dict:
            return self.io_entry.value()
        else:
            return None
        
    def get_alpha(self):
        if not self.has_empty_dict:
            return self.alpha_entry.value()
        else:
            return None
        
    def get_beta(self):
        if not self.has_empty_dict:
            return self.beta_entry.value()
        else:
            return None
        
    def get_data(self):
        stain_type = self.get_stain()
        io_value = self.get_io()
        alpha_value = self.get_alpha()
        beta_value = self.get_beta()

        value_dict = {
            'stain': stain_type,
            'Io': io_value,
            'alpha': alpha_value,
            'beta': beta_value
        }

        return value_dict
