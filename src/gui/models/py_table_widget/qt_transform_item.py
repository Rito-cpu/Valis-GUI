import os

from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.core.keyword_store import *
from src.gui.models.py_toggle import PyToggle


class TableTransformItem(QWidget):
    def __init__(
            self,
            sample_obj: object,
            parent = None
    ):
        super().__init__()

        if parent is not None:
            self.parent = parent

        self._sample_obj = sample_obj

        themes = Themes()
        self.themes = themes.items

        # Setup widget UI
        self._setup_widget()

        # Setup Slots/Signals
        self._rigid_toggle.toggled.connect(self.handle_rigid_toggle)
        self._non_rigid_toggle.toggled.connect(self.handle_non_rigid_toggle)

    def _setup_widget(self):
        button_frame = QFrame(self)
        button_frame.setObjectName('button_frame')
        button_frame.setFrameShape(QFrame.Shape.NoFrame)
        button_frame.setFrameShadow(QFrame.Shadow.Raised)

        rigid_frame = QFrame(button_frame)
        rigid_frame.setObjectName('rigid_frame')
        rigid_frame.setFrameShape(QFrame.Shape.NoFrame)
        rigid_frame.setFrameShadow(QFrame.Shadow.Raised)

        rigid_label = QLabel(rigid_frame)
        rigid_label.setObjectName('rigid_label')
        rigid_label.setText(RIGID_KEY)
        rigid_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rigid_label.setStyleSheet('font-size: 11px;')

        self._rigid_toggle = PyToggle(
            width=28,
            height=16,
            ellipse_y=2,
            bg_color = self.themes['app_color']['text_color'],
            circle_color = self.themes['app_color']['yellow_bg'],
            active_color = self.themes['app_color']['blue_bg'],
            parent=rigid_frame
        )
        self._rigid_toggle.setObjectName('_rigid_toggle')
        self._rigid_toggle.setChecked(True)

        rigid_layout = QHBoxLayout(rigid_frame)
        rigid_layout.setObjectName('rigid_layout')
        rigid_layout.setContentsMargins(5, 5, 5, 5)
        rigid_layout.setSpacing(7)
        rigid_layout.addWidget(rigid_label, alignment=Qt.AlignmentFlag.AlignCenter)
        rigid_layout.addWidget(self._rigid_toggle)

        non_rigid_frame = QFrame(button_frame)
        non_rigid_frame.setObjectName('non_rigid_frame')
        non_rigid_frame.setFrameShape(QFrame.Shape.NoFrame)
        non_rigid_frame.setFrameShadow(QFrame.Shadow.Raised)

        non_rigid_label = QLabel(non_rigid_frame)
        non_rigid_label.setObjectName('non_rigid_label')
        non_rigid_label.setText(NON_RIGID_KEY)
        non_rigid_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        non_rigid_label.setStyleSheet('font-size: 11px;')

        self._non_rigid_toggle = PyToggle(
            width=28,
            height=16,
            ellipse_y=2,
            bg_color = self.themes['app_color']['text_color'],
            circle_color = self.themes['app_color']['yellow_bg'],
            active_color = self.themes['app_color']['blue_bg'],
            parent=non_rigid_frame
        )
        self._non_rigid_toggle.setObjectName('_non_rigid_toggle')
        if os.path.exists(self._sample_obj.path_to_non_rigid_reg):
            self._non_rigid_toggle.setChecked(False)
        else:
            self._rigid_toggle.setChecked(True)

        non_rigid_layout = QHBoxLayout(non_rigid_frame)
        non_rigid_layout.setObjectName('non_rigid_layout')
        non_rigid_layout.setContentsMargins(5, 5, 5, 5)
        non_rigid_layout.setSpacing(7)
        non_rigid_layout.addWidget(non_rigid_label, alignment=Qt.AlignmentFlag.AlignCenter)
        non_rigid_layout.addWidget(self._non_rigid_toggle)

        button_layout = QHBoxLayout(button_frame)
        button_layout.setObjectName('button_layout')
        button_layout.setContentsMargins(5, 5, 5, 5)
        button_layout.setSpacing(25)
        button_layout.addWidget(rigid_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(non_rigid_frame, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(button_frame, alignment=Qt.AlignmentFlag.AlignCenter)

    def handle_rigid_toggle(self):
        if self._rigid_toggle.isChecked():
            self._non_rigid_toggle.setChecked(False)
        else:
            self._non_rigid_toggle.setChecked(True)

    def handle_non_rigid_toggle(self):
        if self._non_rigid_toggle.isChecked():
            self._rigid_toggle.setChecked(False)
        else:
            self._rigid_toggle.setChecked(True)

    def transform_type(self):
        if self._rigid_toggle.isChecked():
            return RIGID_KEY
        else:
            return NON_RIGID_KEY

    def is_non_rigid(self):
        return self._non_rigid_toggle.isChecked()

    def is_rigid(self):
        return self._rigid_toggle.isChecked()

    def set_rigid(self):
        self._rigid_toggle.setChecked(True)

    def set_non_rigid(self):
        self._non_rigid_toggle.setChecked(True)
