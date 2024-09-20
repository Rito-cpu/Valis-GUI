import os

from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.core.app_config import IMG_RSC_PATH
from .styles import tool_bttn_template


class QtZoomFrame(QWidget):
    zoom_out = pyqtSignal(bool)
    zoom_in = pyqtSignal(bool)

    def __init__(
        self,
        plus_path: list = ['downloads', 'white_plus.png'],
        minus_path: list = ['downloads', 'white_minus.png'],
        min_range: int = 0,
        max_range: int = 0,
        parent = None
    ):
        super().__init__()

        if parent is not None:
            self.setParent(parent)

        themes = Themes()
        self.themes = themes.items
        self._plus_path = os.path.join(IMG_RSC_PATH, *plus_path)
        self._minus_path = os.path.join(IMG_RSC_PATH, *minus_path)
        self._min_range = min_range
        self._max_range = max_range

        self._setup_widget()

        self.zoom_out_bttn.clicked.connect(self.zoom_out_clicked)
        self.zoom_in_bttn.clicked.connect(self.zoom_in_clicked)
        #self.zoom_out_bttn.clicked.connect(self.left_side_clicked)
        #self.zoom_out_bttn.released.connect(self.left_side_released)
        #self.zoom_in_bttn.clicked.connect(self.right_side_clicked)
        #self.zoom_in_bttn.released.connect(self.right_side_released)

    def _setup_widget(self):
        tool_bttn_format = tool_bttn_template.format(
            _color = self.themes['app_color']['blue_bg']
        )

        #container_frame = QFrame(self)
        #container_frame.setObjectName('container_frame')
        #container_frame.setFrameShape(QFrame.Shape.NoFrame)
        #container_frame.setFrameShadow(QFrame.Shadow.Plain)
        #container_frame.setStyleSheet(f"""
        #    QFrame#container_frame {{
        #        background: {self.themes['app_color']['blue_bg']};
        #        border: 2px solid lightgray;
        #        border-radius: 8px;
        #    }}
        #""")

        self.frame_style = """
            QFrame#{obj_name} {{
                background: {bg_color};
                border: {border_width}px solid {border_color};
                border-top-{side}-radius: {radius}px;
                border-bottom-{side}-radius: {radius}px;
                border-{none_side}: none;
            }}
        """

        self.left_side_frame = QFrame(self)
        self.left_side_frame.setObjectName('left_side_frame')
        self.left_side_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.left_side_frame.setFrameShadow(QFrame.Shadow.Plain)
        self.left_side_frame.setStyleSheet(
            self.frame_style.format(
                obj_name=self.left_side_frame.objectName(),
                bg_color=self.themes['app_color']['blue_bg'],
                border_width=2,
                border_color=self.themes['app_color']['text_color'],
                side='left',
                radius=8,
                none_side='right'
            )
        )

        self.zoom_out_bttn = QToolButton(self.left_side_frame)
        self.zoom_out_bttn.setObjectName('zoom_out_bttn')
        self.zoom_out_bttn.setIcon(QIcon(self._minus_path))
        self.zoom_out_bttn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.zoom_out_bttn.setIconSize(QSize(18, 18))
        self.zoom_out_bttn.setStyleSheet(tool_bttn_format)

        left_side_layout = QVBoxLayout(self.left_side_frame)
        left_side_layout.setObjectName('left_side_layout')
        left_side_layout.setContentsMargins(0, 0, 0, 0)
        left_side_layout.addWidget(self.zoom_out_bttn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.right_side_frame = QFrame(self)
        self.right_side_frame.setObjectName('right_side_frame')
        self.right_side_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.right_side_frame.setFrameShadow(QFrame.Shadow.Plain)
        self.right_side_frame.setStyleSheet(
            self.frame_style.format(
                obj_name=self.right_side_frame.objectName(),
                bg_color=self.themes['app_color']['blue_bg'],
                border_width=2,
                border_color=self.themes['app_color']['text_color'],
                side='right',
                radius=8,
                none_side='left'
            )
        )

        self.zoom_in_bttn = QToolButton(self.right_side_frame)
        self.zoom_in_bttn.setObjectName('zoom_in_bttn')
        self.zoom_in_bttn.setIcon(QIcon(self._plus_path))
        self.zoom_in_bttn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.zoom_in_bttn.setIconSize(QSize(18, 18))
        self.zoom_in_bttn.setStyleSheet(tool_bttn_format)

        right_side_layout = QVBoxLayout(self.right_side_frame)
        right_side_layout.setObjectName('right_side_layout')
        right_side_layout.setContentsMargins(0, 0, 0, 0)
        right_side_layout.addWidget(self.zoom_in_bttn, alignment=Qt.AlignmentFlag.AlignCenter)

        middle_line = QFrame(self)
        middle_line.setObjectName('middle_line')
        middle_line.setFrameShape(QFrame.Shape.VLine)
        middle_line.setFrameShadow(QFrame.Shadow.Plain)
        middle_line.setFixedWidth(2)
        middle_line.setStyleSheet(f'background-color: {self.themes["app_color"]["main_bg"]}; border: none;')

        #container_layout = QHBoxLayout(container_frame)
        #container_layout.setObjectName('container_layout')
        #container_layout.setContentsMargins(0, 0, 0, 0)
        #container_layout.setSpacing(0)
        #container_layout.addWidget(self.zoom_out_bttn, alignment=Qt.AlignmentFlag.AlignCenter)
        #container_layout.addWidget(self.zoom_tracker, alignment=Qt.AlignmentFlag.AlignCenter)
        #container_layout.addWidget(middle_line)
        #container_layout.addWidget(self.zoom_in_bttn, alignment=Qt.AlignmentFlag.AlignCenter)

        #container_frame.setFixedWidth(container_layout.sizeHint().width() + 20)

        main_layout = QHBoxLayout(self)
        main_layout.setObjectName('main_layout')
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.left_side_frame)
        main_layout.addWidget(middle_line)
        main_layout.addWidget(self.right_side_frame)

        self.setFixedSize(main_layout.sizeHint().width() + 18, 25)

    def left_side_clicked(self):
        self.left_side_frame.setStyleSheet(
            self.frame_style.format(
                obj_name=self.left_side_frame.objectName(),
                bg_color=self.themes['app_color']['blue_bg'],
                border_width=1,
                border_color=self.themes['app_color']['main_bg'],
                side='left',
                radius=8,
                none_side='right'
            )
        )

    def left_side_released(self):
        self.left_side_frame.setStyleSheet(
            self.frame_style.format(
                obj_name=self.left_side_frame.objectName(),
                bg_color=self.themes['app_color']['blue_bg'],
                border_width=2,
                border_color=self.themes['app_color']['main_bg'],
                side='left',
                radius=8,
                none_side='right'
            )
        )

    def right_side_clicked(self):
        self.right_side_frame.setStyleSheet(
            self.frame_style.format(
                obj_name=self.right_side_frame.objectName(),
                bg_color=self.themes['app_color']['blue_bg'],
                border_width=1,
                border_color=self.themes['app_color']['main_bg'],
                side='right',
                radius=8,
                none_side='left'
            )
        )

    def right_side_released(self):
        self.right_side_frame.setStyleSheet(
            self.frame_style.format(
                obj_name=self.right_side_frame.objectName(),
                bg_color=self.themes['app_color']['blue_bg'],
                border_width=2,
                border_color=self.themes['app_color']['main_bg'],
                side='right',
                radius=8,
                none_side='left'
            )
        )

    def zoom_out_clicked(self):
        self.zoom_out.emit(True)

    def zoom_in_clicked(self):
        self.zoom_in.emit(True)

