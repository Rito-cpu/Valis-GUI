import os

from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.core.app_config import IMG_RSC_PATH
from .qt_arrow_button import QtArrowButton


class QtImageNav(QWidget):
    last_clicked = pyqtSignal()
    next_clicked = pyqtSignal()

    def __init__(
        self,
        left_arrow_path = ['svg_icons', 'icon_arrow_left.svg'],
        right_arrow_path = ['svg_icons', 'icon_arrow_right.svg'],
        font_size: int = 18,
        parent=None
    ):
        super().__init__()

        if parent is not None:
            self.setParent(parent)

        themes = Themes()
        self.themes = themes.items

        self.left_arrow = os.path.join(IMG_RSC_PATH, *left_arrow_path)
        self.right_arrow = os.path.join(IMG_RSC_PATH, *right_arrow_path)
        self._font_size = font_size
        self._current_pos = 0

        self._setup_widget()

        self._last_bttn.clicked.connect(self.on_last)
        self._next_bttn.clicked.connect(self.on_next)

    def _setup_widget(self):
        self.container_widget = QWidget(self)
        self.container_widget.setObjectName('container_widget')
        self.container_widget.setFixedSize(179, 80)  # adjust the size to fit your needs

        self.circle_frame = QFrame(self.container_widget)
        self.circle_frame.setObjectName('circle_frame')
        self.circle_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.circle_frame.setFrameShadow(QFrame.Shadow.Plain)
        self.circle_frame.setFixedSize(80, 80)
        self.circle_frame.setStyleSheet(f"""
            QFrame#circle_frame {{
                background: {self.themes['app_color']['blue_bg']};
                border-radius: 40px;
            }}
        """)
        self.circle_frame.move(49, 0)  # center the circle frame within the container widget

        inner_circle = QFrame(self.circle_frame)
        inner_circle.setObjectName('inner_circle')
        inner_circle.setFrameShape(QFrame.Shape.NoFrame)
        inner_circle.setFrameShadow(QFrame.Shadow.Plain)
        inner_circle.setFixedSize(60, 60)
        inner_circle.setStyleSheet(f"""
            QFrame#inner_circle {{
                background: {self.themes['app_color']['yellow_bg']};
                border-radius: 30px;
            }}
        """)

        self.position_label = QLabel(inner_circle)
        self.position_label.setObjectName('position_label')
        self.position_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.position_label.setText('0')
        self.position_label.setStyleSheet(f'color: {self.themes["app_color"]["text_color"]}; font-size: {self._font_size}px;')

        inner_circle_layout = QVBoxLayout(inner_circle)
        inner_circle_layout.setObjectName('inner_circle_layout')
        inner_circle_layout.setContentsMargins(0, 0, 0, 0)
        inner_circle_layout.addWidget(self.position_label, alignment=Qt.AlignmentFlag.AlignCenter)

        circle_frame_layout = QVBoxLayout(self.circle_frame)
        circle_frame_layout.setObjectName('circle_frame_layout')
        circle_frame_layout.setContentsMargins(0, 0, 0, 0)
        circle_frame_layout.addWidget(inner_circle, alignment=Qt.AlignmentFlag.AlignCenter)

        self._last_bttn = QtArrowButton(
            direction='left', 
            image_path=self.left_arrow, 
            parent=self.container_widget
        )
        self._last_bttn.setObjectName('last_bttn')
        self._last_bttn.setGeometry(0, 29, self._last_bttn.sizeHint().width(), self._last_bttn.sizeHint().height())
        
        self._next_bttn = QtArrowButton(
            direction='right', 
            image_path=self.right_arrow, 
            parent=self.container_widget
        )
        self._next_bttn.setObjectName('next_bttn')
        self._next_bttn.setGeometry(120, 29, self._next_bttn.sizeHint().width(), self._next_bttn.sizeHint().height())

        circle_layout = QHBoxLayout()
        circle_layout.addStretch()
        circle_layout.addWidget(self.container_widget)
        circle_layout.addStretch()

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addLayout(circle_layout)

    def on_last(self):
        self.last_clicked.emit()
    
    def on_next(self):
        self.next_clicked.emit()

    def change_text(self, placement: str):
        self.position_label.setText(placement)

    def reset(self):
        self.position_label.setText('0')
