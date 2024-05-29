from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.gui.models.py_toggle import PyToggle


class ExportTableItem(QWidget):
    def __init__(
            self,
            text,
            sample_obj,
            parent=None
    ):
        super().__init__()

        if parent is not None:
            self.parent = parent

        self._text = text
        self._sample_obj = sample_obj

        themes = Themes()
        self.themes = themes.items

        self._setup_widget()

    def _setup_widget(self):
        sample_frame = QFrame(self)
        sample_frame.setObjectName('sample_frame')
        sample_frame.setFrameShape(QFrame.Shape.NoFrame)
        sample_frame.setFrameShadow(QFrame.Shadow.Raised)

        sample_label = QLabel(sample_frame)
        sample_label.setObjectName('sample_label')
        sample_label.setText(self._text)
        sample_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sample_label.setStyleSheet('font-size: 12px;')

        self._sample_toggle = PyToggle(
            width=28,
            height=16,
            ellipse_y=2,
            bg_color = self.themes['app_color']['text_color'],
            circle_color = self.themes['app_color']['yellow_bg'],
            active_color = self.themes['app_color']['blue_bg'],
            parent=sample_frame
        )
        self._sample_toggle.setObjectName('_sample_toggle')
        self._sample_toggle.setChecked(self._sample_obj.to_export)

        sample_layout = QHBoxLayout(sample_frame)
        sample_layout.setObjectName('sample_layout')
        sample_layout.setContentsMargins(5, 5, 5, 5)
        sample_layout.setSpacing(25)
        sample_layout.addWidget(self._sample_toggle, alignment=Qt.AlignmentFlag.AlignLeft)
        sample_layout.addWidget(sample_label)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(sample_frame, alignment=Qt.AlignmentFlag.AlignCenter)

    def text(self):
        return self._text

    def isChecked(self):
        return self._sample_toggle.isChecked()
