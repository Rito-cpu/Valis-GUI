from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from .styles import right_arrow_template, left_arrow_template


class QtArrowButton(QWidget):
    clicked = pyqtSignal()
    released = pyqtSignal()

    def __init__(
        self,
        direction: str,
        image_path: str,
        font_size: int = 13,
        parent=None
    ):
        super().__init__()

        if parent is not None:
            self.setParent(parent)

        self.setMouseTracking(True)
        self.setFixedSize(59, 25)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        themes = Themes()
        self.themes = themes.items
        self._direction = direction
        self._arrow_path = image_path
        self._font_size = font_size

        self._setup_widget()

    def _setup_widget(self):
        if self._direction == 'left':
            self._default_format = left_arrow_template.format(
                _color = self.themes['app_color']['blue_bg'],
                text_color = self.themes['app_color']['main_bg']
            )
            self._clicked_format = left_arrow_template.format(
                _color=self.themes['app_color']['blue_pressed'],
                text_color=self.themes['app_color']['main_bg']
            )
        else:
            self._default_format = right_arrow_template.format(
                _color = self.themes['app_color']['blue_bg'],
                text_color = self.themes['app_color']['main_bg']
            )
            self._clicked_format = right_arrow_template.format(
                _color=self.themes['app_color']['blue_pressed'],
                text_color=self.themes['app_color']['main_bg']
            )

        self._main_frame = QFrame(self)
        self._main_frame.setObjectName('main_frame')
        self._main_frame.setFrameShape(QFrame.Shape.NoFrame)
        self._main_frame.setFrameShadow(QFrame.Shadow.Plain)
        self._main_frame.setStyleSheet(self._default_format)

        image_pixmap = QPixmap(self._arrow_path)
        image_pixmap.scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio)

        image_label = QLabel(self._main_frame)
        image_label.setObjectName('image_label')
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setPixmap(image_pixmap)

        frame_layout = QHBoxLayout(self._main_frame)
        frame_layout.setObjectName('frame_layout')
        frame_layout.setSpacing(3)

        direction_label = QLabel(self._main_frame)
        direction_label.setObjectName('direction_label')
        direction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        direction_label.setStyleSheet(f'font-size: {self._font_size}px; color: {self.themes["app_color"]["main_bg"]};')

        if self._direction == "left":
            direction_label.setText("Last")
            
            frame_layout.setContentsMargins(4, 3, 0, 3)
            frame_layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignCenter)
            frame_layout.addWidget(direction_label, alignment=Qt.AlignmentFlag.AlignCenter)
            frame_layout.addStretch(1)
        else:
            direction_label.setText('Next')
            
            frame_layout.setContentsMargins(0, 3, 4, 3)
            frame_layout.addStretch(1)
            frame_layout.addWidget(direction_label, alignment=Qt.AlignmentFlag.AlignCenter)
            frame_layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout = QVBoxLayout(self)
        main_layout.setObjectName('main_layout')
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self._main_frame)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._main_frame.setStyleSheet(self._clicked_format)
            self.clicked.emit()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._main_frame.setStyleSheet(self._default_format)
            self.released.emit()
        super().mouseReleaseEvent(event)

    def enterEvent(self, event):
        super().enterEvent(event)

    def leaveEvent(self, event):
        super().leaveEvent(event)
