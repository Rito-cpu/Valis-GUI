from PyQt6.QtGui import QMouseEvent
from src.core.pyqt_core import *
from src.core.app_config import *
from src.core.json.json_themes import Themes
from src.gui.models.qt_spinbox import QtNumEntry
from src.gui.models.qt_combo_widget import QtComboBox
from .channel_options import ChannelGetter
from .color_distance_options import BgColorDistance
from .color_standardizer import ColorfulStandardizer
from .greyscale_options import GrayOptions
from .hed_options import HEDOptions
from .luminosity_options import LuminosityOptions
from .stain_flattener_options import StainFlattener
from .styles import *
from .bf_process import BFProcessWidget
from .if_process import IFProcessWidget


class GradientButton(QPushButton):
    button_hover_style = """
        QPushButton {
            border-radius: 17px;
            border: 1px outset lightgray;
            color: black;
            font-size: 14px;
        }
    """

    def __init__(
        self,
        parent=None
    ):
        super().__init__()
        if parent is not None:
            self.setParent(parent)

        self.setFixedSize(70, 70)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._gradient_pos = 0
        self.set_gradient(self._gradient_pos)
        self.set_normal_style()

    def set_gradient(self, pos):
        if pos == 0:
            gradient = "qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 blue, stop: 1 red)"
        else:
            gradient = "qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 red, stop: 1 blue)"
        self._current_gradient = gradient

    def toggle_gradient(self):
        if self._gradient_pos == 0:
            self._gradient_pos = 1
        else:
            self._gradient_pos = 0
        self.set_gradient(self._gradient_pos)

    def set_normal_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                border-radius: 17px;
                border: 1px inset lightgray;
                background: {self._current_gradient};
                color: black;
                font-size: 14px;
            }}
            QPushButton:hover {{
                
            }}
        """)

    def set_pressed_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                border-radius: 17px;
                border: 2px outset lightgray;
                background: {self._current_gradient};
                color: black;
                font-size: 14px;
            }}
        """)

    def toggle_gradient(self):
        if self._gradient_pos == 0:
            self._gradient_pos = 1
        else:
            self._gradient_pos = 0
        self.set_gradient(self._gradient_pos)
        self.set_normal_style()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.set_pressed_style()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.toggle_gradient()


class QtProcessImages(QGroupBox):
    def __init__(
            self,
            title: str = 'Process Images',
            color: str = 'black',
            bg_color: str = 'lightgray',
            title_size: int = 16,
            border_radius: int = 8,
            margin_top: int = 21,
            font_size: int=12,
            parent=None
        ):
        super().__init__()

        if parent != None:
            self.setParent(parent)

        self.setTitle(title)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        #if not option_items:
        #    option_items = ['EQ', 'Greyscale', 'EQ Brightness', 'Already Processed']
        global COMBINED_PROCESSOR_OPTIONS

        self._option_items = COMBINED_PROCESSOR_OPTIONS
        self._font_size = font_size

        themes = Themes()
        self.themes = themes.items

        groupbox_style = groupbox_template.format(
            color=self.themes['app_color']['main_bg'],
            color_two=self.themes['app_color']['text_color'],
            bg_color=self.themes['app_color']['blue_bg'],
            title_size=title_size,
            border_radius=border_radius,
            margin_top=margin_top,
            font_size=font_size
        )
        self.setStyleSheet(groupbox_style)

        # setup UI
        #self._setup_widget()
        self._setup_two()

        # *** Slots/Signals ***
        #self.process_option_dropdown.currentIndexChanged.connect(self.dropdown_changed)

    def _setup_widget(self):
        content_widget = QWidget(self)
        content_widget.setObjectName('content_widget')

        maximum_size_label = QLabel(content_widget)
        maximum_size_label.setObjectName('maximum_size_label')
        maximum_size_label.setText('Maximum Size (pixels):')
        maximum_size_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self._maximum_size_entry = QtNumEntry(
            font_size=self._font_size,
            font_color=self.themes['app_color']['text_color'],
            bg_color=self.themes['app_color']['dark_one'],
            parent=content_widget
        )
        self._maximum_size_entry.setObjectName('maximum_size_entry')
        self._maximum_size_entry.setRange(1, 1000)
        self._maximum_size_entry.setSingleStep(1)
        self._maximum_size_entry.setValue(500)
        self._maximum_size_entry.setFixedSize(75, 25)

        process_method_label = QLabel(content_widget)
        process_method_label.setObjectName('process_method_label')
        process_method_label.setText('Processing Method:')
        process_method_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.process_option_dropdown = QtComboBox(
            bg_color=self.themes["app_color"]["dark_one"],
            text_color=self.themes["app_color"]["text_color"],
            parent=content_widget
        )
        self.process_option_dropdown.setObjectName('process_option_dropdown')
        self.process_option_dropdown.addItems(self._option_items)
        self.process_option_dropdown.setCurrentIndex(0)
        self.process_option_dropdown.setFixedHeight(30)
        self.process_option_dropdown.setMinimumWidth(120)
        self.process_option_dropdown.setCursor(Qt.CursorShape.PointingHandCursor)

        # *** Create option Widgets ***
        self._stack_widget = QWidget(content_widget)
        self._stack_widget.setObjectName('stack_widget')
        self._stack_widget.setStyleSheet('QWidget#stack_widget {border: none; background: white; border-radius: 8px;}')

        self.channel_getter_widget = ChannelGetter(parent=self._stack_widget)
        self.bg_color_distance_widget = BgColorDistance(parent=self._stack_widget)
        self.colorful_standardizer_widget = ColorfulStandardizer(parent=self._stack_widget)
        self.gray_widget = GrayOptions(parent=self._stack_widget)
        self.hed_widget = HEDOptions(parent=self._stack_widget)
        self.luminosity_widget = LuminosityOptions(parent=self._stack_widget)
        self.stain_flattener_widget = StainFlattener(parent=self._stack_widget)

        self._stack_layout = QStackedLayout(self._stack_widget)
        self._stack_layout.setContentsMargins(15, 15, 15, 15)
        self._stack_layout.addWidget(self.channel_getter_widget)
        self._stack_layout.addWidget(self.bg_color_distance_widget)
        self._stack_layout.addWidget(self.colorful_standardizer_widget)
        self._stack_layout.addWidget(self.gray_widget)
        self._stack_layout.addWidget(self.hed_widget)
        self._stack_layout.addWidget(self.luminosity_widget)
        self._stack_layout.addWidget(self.stain_flattener_widget)

        content_layout = QGridLayout(content_widget)
        content_layout.setContentsMargins(25, 18, 25, 18)
        content_layout.setSpacing(25)
        content_layout.addWidget(maximum_size_label, 0, 0, 1, 1)
        content_layout.addWidget(self._maximum_size_entry, 0, 1, 1, 1)
        content_layout.addWidget(process_method_label, 1, 0, 1, 1)
        content_layout.addWidget(self.process_option_dropdown, 1, 1, 1, 2)
        content_layout.addWidget(self._stack_widget, 2, 0, 1, 4)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(25)
        main_layout.addWidget(content_widget)

    def dropdown_changed(self, dropdown_index):
        self._stack_layout.setCurrentIndex(dropdown_index)

    def get_current_option_data(self):
        option_widget = self._stack_layout.currentWidget()
        options = option_widget.get_data()

        return options

    def get_data(self):
        maximum_size = self._maximum_size_entry.value()
        process_type = self.process_option_dropdown.currentText()
        option_data = self.get_current_option_data()

        data_dict = {
            'maximum_size': maximum_size,
            'process_type': process_type,
            'options': option_data
        }

        return data_dict

    def _setup_two(self):
        content = QWidget(self)
        self.t1 = BFProcessWidget(parent=content)
        #self.t2 = IFProcessWidget(parent=content)
        #self.t2.hide()
        self.butt = GradientButton(parent=content)
        self.butt.setObjectName('butt')
        self.butt.setFixedSize(35, 35)
        self.butt.setText('BF')
        self.butt.clicked.connect(self.testing)
        c_lay = QVBoxLayout(content)
        c_lay.setContentsMargins(5, 5, 5, 5)
        c_lay.addWidget(self.butt)
        c_lay.addWidget(self.t1)
        #c_lay.addWidget(self.t2)
        main_lay = QVBoxLayout(self)
        main_lay.setContentsMargins(0, 0, 0, 0)
        main_lay.addWidget(content)

    def testing(self):
        if self.butt.text() == 'BF':
            self.butt.setText('IF')
        else:
            self.butt.setText('BF')
