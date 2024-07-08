from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.core.app_config import IF_PROCESSOR_OPTIONS, DEFAULT_PROCESSOR_IF, default_if_processor_args
from src.gui.models.qt_combo_widget import QtComboBox
from .styles import *
from .process_args import ClassArgs


class IFProcessWidget(QGroupBox):
    def __init__(
        self,
        title: str = 'Immunofluorescence Process',
        color: str = 'black',
        bg_color: str = 'lightgray',
        title_size: int = 16,
        border_radius: int = 8,
        margin_top: int = 21,
        font_size: int=13,
        parent=None
    ):
        super().__init__()

        if parent is not None:
            self.setParent(parent)

        self.setTitle(title)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)


        #print(f'Brightfield Methods: \n{IF_PROCESSOR_OPTIONS}')
        #print(f'\nDefault Proc: {DEFAULT_PROCESSOR_IF}')
        #print(f'Default Brightfield Args: \n{default_if_processor_args}')

        self._method_names = IF_PROCESSOR_OPTIONS.keys()

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

        self._setup_widget()

        self.process_combo_box.currentIndexChanged.connect(self.change_setting)


    def _setup_widget(self):
        content_frame = QFrame(self)
        content_frame.setObjectName('content_frame')
        content_frame.setFrameShape(QFrame.Shape.NoFrame)
        content_frame.setFrameShadow(QFrame.Shadow.Raised)

        method_frame = QFrame(content_frame)
        method_frame.setObjectName('method_frame')
        method_frame.setFrameShape(QFrame.Shape.NoFrame)
        method_frame.setFrameShadow(QFrame.Shadow.Raised)

        method_label = QLabel(method_frame)
        method_label.setObjectName('method_label')
        method_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        method_label.setText('Method:')

        self.process_combo_box = QtComboBox(
            bg_color=self.themes["app_color"]["dark_one"],
            text_color=self.themes["app_color"]["text_color"],
            parent=method_frame
        )
        self.process_combo_box.setObjectName('process_combo_box')
        self.process_combo_box.addItems(self._method_names)
        self.process_combo_box.setCurrentText(DEFAULT_PROCESSOR_IF)
        self.process_combo_box.setFixedHeight(30)
        self.process_combo_box.setMinimumWidth(150)
        self.process_combo_box.setMaximumWidth(200)
        self.process_combo_box.setCursor(Qt.CursorShape.PointingHandCursor)

        method_layout = QFormLayout(method_frame)
        method_layout.setObjectName('method_layout')
        method_layout.addRow(method_label, self.process_combo_box)

        self.stacked_settings_area = QStackedWidget(content_frame)
        self.stacked_settings_area.setObjectName('stacked_settings_area')
        self.create_dynamic_settings()

        content_layout = QVBoxLayout(content_frame)
        content_layout.setObjectName('content_layout')
        content_layout.setContentsMargins(25, 10, 25, 10)
        content_layout.addWidget(self.stacked_settings_area)
        content_layout.addWidget(method_frame, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout = QVBoxLayout(self)
        main_layout.setObjectName('main_layout')
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(content_frame)

    def get_processing_class(self):
        return self.process_combo_box.currentText()
    
    def change_setting(self):
        self.stacked_settings_area.setCurrentIndex(self.process_combo_box.currentIndex())

    def create_dynamic_settings(self):
        for process_type in self._method_names:
            args_frame = QFrame(self.stacked_settings_area)
            args_frame.setObjectName('args_frame')
            args_frame.setFrameShape(QFrame.Shape.NoFrame)
            args_frame.setFrameShadow(QFrame.Shadow.Raised)

            method_args_label = QLabel(args_frame)
            method_args_label.setObjectName('method_args_label')
            method_args_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            method_args_label.setText(process_type + ' Settings')

            dynamic_process_settings = ClassArgs(
                args=IF_PROCESSOR_OPTIONS[process_type],
                parent=args_frame
            )
            dynamic_process_settings.setObjectName('dynamic_process_settings')

            args_layout = QVBoxLayout(args_frame)
            args_layout.setObjectName('args_layout')
            args_layout.addWidget(method_args_label, alignment=Qt.AlignmentFlag.AlignCenter)
            args_layout.addWidget(dynamic_process_settings, alignment=Qt.AlignmentFlag.AlignCenter)

            self.stacked_settings_area.addWidget(args_frame)
        self.stacked_settings_area.setCurrentIndex(self.process_combo_box.currentIndex())

    def get_widget_settings(self):
        frame = self.stacked_settings_area.currentWidget()
        setting_widget = frame.findChild(ClassArgs)
        return setting_widget.get_data()