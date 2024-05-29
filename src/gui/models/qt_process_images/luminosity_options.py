from src.core.pyqt_core import *
from src.core.app_config import *
from src.core.keyword_store import LUMINOSITY_KEY
from src.core.json.json_themes import Themes


class LuminosityOptions(QWidget):
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

        data_dict = BF_PROCESSOR_OPTIONS[LUMINOSITY_KEY]
        if data_dict:
            self.has_empty_dict = False
            pass
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

    def get_data(self):
        value_dict = {}

        return value_dict
