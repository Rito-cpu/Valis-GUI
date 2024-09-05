import os
import numpy as np

from .styles import *
from src.core.pyqt_core import *
from src.core.app_config import IMG_RSC_PATH
from src.core.json.json_themes import Themes
from src.core.keyword_store import THMB_DIM
from src.gui.models import PyPushButton
from .qt_graphics_view import QtGraphicsView


class QtImageView(QWidget):
    def __init__(
            self,
            dimensions=(THMB_DIM, THMB_DIM),
            padding: int = 100,
            title_size: int = 16,
            font_size: int = 14,
            plus_path: str = 'downloads/white_plus.png',
            minus_path: str = 'downloads/white_minus.png',
            parent=None
    ) -> None:
        super().__init__()

        if parent is not None:
            self.parent = parent

        if dimensions is None:
            dimensions = (THMB_DIM, THMB_DIM)

        self.dimensions = dimensions
        self.padding = padding
        self.pixmap_list = []
        self.names_list = []
        self._title_size = title_size
        self._font_size = font_size
        self.image_counter = 0
        self.num_images = 0

        self._plus_path = os.path.join(IMG_RSC_PATH, plus_path)
        self._minus_path = os.path.join(IMG_RSC_PATH, minus_path)

        themes = Themes()
        self.themes = themes.items

        self.setObjectName('QtImageView')
        self.setMinimumWidth(self.dimensions[0] + self.padding)
        self.setMinimumHeight(self.dimensions[1] + self.padding)

        viewer_frame = viewer_template.format(
            _obj_name=self.objectName(),
            _bg=self.themes['app_color']['text_color']
        )
        self.setStyleSheet(viewer_frame)

        # Setup widget
        self._setup_widget()

        # Set signals/slots
        self.display.image_added.connect(self.set_image_face)
        self.display.images_removed.connect(self.set_no_image_face)
        self.last_bttn.clicked.connect(self.last_image)
        self.next_bttn.clicked.connect(self.next_image)
        self.zoom_in_bttn.clicked.connect(self.zoom_in)
        self.zoom_out_bttn.clicked.connect(self.zoom_out)

    def _setup_widget(self):
        title_format = title_label_template.format(
            _title_size=self._title_size,
            _color = self.themes['app_color']['main_bg']
        )

        body_format = body_label_template.format(
            _font_size = self._font_size,
            _color = self.themes['app_color']['text_color']
        )

        tool_bttn_format = tool_bttn_template.format(
            _color = self.themes['app_color']['blue_bg']
        )

        self.sample_label = QLabel(self)
        self.sample_label.setObjectName('sample_label')
        self.sample_label.setText('Sample: None')
        self.sample_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sample_label.setStyleSheet(title_format)

        self.sample_name = QLabel(self)
        self.sample_name.setObjectName('sample_label')
        self.sample_name.setText('None')
        self.sample_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sample_name.setStyleSheet(title_format)

        display_face = QWidget(self)
        display_face.setObjectName('display_face')

        self.no_image_label = QLabel(display_face)
        self.no_image_label.setObjectName('no_image_label')
        self.no_image_label.setText('No Image')
        self.no_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_image_label.setStyleSheet(body_format)

        self.image_frame = QFrame(display_face)
        self.image_frame.setObjectName('image_frame')
        self.image_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.image_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.display = QtGraphicsView(parent=self.image_frame)

        navigation_frame = QWidget(self.image_frame)
        navigation_frame.setObjectName('navigation_frame')
        navigation_format = navigation_template.format(
            _obj_name = navigation_frame.objectName(),
            _color = self.themes['app_color']['main_bg']
        )
        navigation_frame.setStyleSheet(navigation_format)

        self.navigation_label = QLabel(navigation_frame)
        self.navigation_label.setObjectName('navigation_label')
        self.navigation_label.setText('Empty')
        self.navigation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.navigation_label.setStyleSheet(f'font-size: 14px; color: {self.themes["app_color"]["text_color"]}')

        self.next_bttn = PyPushButton(
            text="Next",
            radius=8,
            color=self.themes['app_color']['main_bg'],
            bg_color=self.themes['app_color']['blue_bg'],
            bg_color_hover=self.themes['app_color']['highlight_bg'],
            bg_color_pressed=self.themes['app_color']['highlight_bg'],
            parent=navigation_frame
        )
        self.next_bttn.setObjectName(u"next_bttn")
        self.next_bttn.setFixedSize(85, 31)

        self.last_bttn = PyPushButton(
            text="Last",
            radius=8,
            color=self.themes['app_color']['main_bg'],
            bg_color=self.themes['app_color']['blue_bg'],
            bg_color_hover=self.themes['app_color']['highlight_bg'],
            bg_color_pressed=self.themes['app_color']['highlight_bg'],
            parent=navigation_frame
        )
        self.last_bttn.setObjectName(u"last_bttn")
        self.last_bttn.setFixedSize(85, 31)

        zoom_frame = QWidget(navigation_frame)
        zoom_frame.setObjectName('zoom_frame')

        self.zoom_in_bttn = QToolButton(navigation_frame)
        self.zoom_in_bttn.setIcon(QIcon(self._plus_path))
        self.zoom_in_bttn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.zoom_in_bttn.setIconSize(QSize(18, 18))
        self.zoom_in_bttn.setStyleSheet(tool_bttn_format)

        self.zoom_out_bttn = QToolButton(navigation_frame)
        self.zoom_out_bttn.setIcon(QIcon(self._minus_path))
        self.zoom_out_bttn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.zoom_out_bttn.setIconSize(QSize(18, 18))
        self.zoom_out_bttn.setStyleSheet(tool_bttn_format)

        separator_label = QLabel(zoom_frame)
        separator_label.setObjectName('separator_label')
        separator_label.setText('/')
        separator_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        separator_label.setStyleSheet(f'font-size: 14px;')

        zoom_layout = QHBoxLayout(zoom_frame)
        zoom_layout.setObjectName('zoom_layout')
        zoom_layout.setContentsMargins(0, 0, 0, 0)
        zoom_layout.setSpacing(3)
        zoom_layout.addWidget(self.zoom_out_bttn)
        zoom_layout.addWidget(separator_label)
        zoom_layout.addWidget(self.zoom_in_bttn)
        zoom_frame.setFixedWidth(zoom_layout.sizeHint().width()+5)

        navigation_layout = QGridLayout(navigation_frame)
        navigation_layout.setObjectName('navigation_layout')
        navigation_layout.setContentsMargins(10, 10, 10, 10)
        navigation_layout.setSpacing(10)
        navigation_layout.addWidget(self.navigation_label, 0, 0, 1, 2)
        navigation_layout.addWidget(self.last_bttn, 1, 0, 1, 1)
        navigation_layout.addWidget(self.next_bttn, 1, 1, 1, 1)
        navigation_layout.addWidget(zoom_frame, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        navigation_frame.setFixedHeight(navigation_layout.sizeHint().height()+10)
        navigation_frame.setMinimumWidth(navigation_layout.sizeHint().width() + 10)

        frame_layout = QVBoxLayout(self.image_frame)
        frame_layout.setContentsMargins(5, 5, 5, 5)
        frame_layout.setSpacing(5)
        frame_layout.addWidget(self.display)
        frame_layout.addWidget(self.sample_name, Qt.AlignmentFlag.AlignCenter)
        frame_layout.addWidget(navigation_frame, alignment=Qt.AlignmentFlag.AlignCenter)

        self.display_face_layout = QStackedLayout(display_face)
        self.display_face_layout.addWidget(self.no_image_label)
        self.display_face_layout.addWidget(self.image_frame)
        self.display_face_layout.setCurrentWidget(self.no_image_label)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        main_layout.addWidget(self.sample_label)
        main_layout.addWidget(display_face)

    def zoom_in(self):
        self.display.zoom_in()

    def zoom_out(self):
        self.display.zoom_out()

    def img2pixmap(self, image):
        if image.ndim > 2:
            height, width, channel = image.shape
            bytes_per_line = 3 * width
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        else:
            height, width = image.shape
            bytes_per_line = width
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)

        pixmap = QPixmap.fromImage(q_image)

        return pixmap

    def last_image(self):
        if self.image_counter > 0:
            self.image_counter -= 1
            self.display.set_image(self.pixmap_list[self.image_counter])
            self.display.reset_zoom()

            if self.names_list is not None:
                self.sample_name.setText(self.names_list[self.image_counter])
                self.navigation_label.setText(f'{self.image_counter+1}/{self.num_images}')

    def next_image(self):
        if self.image_counter < self.num_images - 1:
            self.image_counter += 1
            self.display.set_image(self.pixmap_list[self.image_counter])
            self.display.reset_zoom()

            if self.names_list is not None:
                self.sample_name.setText(self.names_list[self.image_counter])
                self.navigation_label.setText(f'{self.image_counter+1}/{self.num_images}')

    def add_images(self, sample, image_list, image_names=None):
        if image_list:
            self.num_images = len(image_list)
            self.names_list = image_names
            self.pixmap_list = [None] * len(image_list)

            for index, image in enumerate(image_list):
                # print("adding image", index)
                self.pixmap_list[index] = image # self.img2pixmap(image)

            self.display.set_image(self.pixmap_list[self.image_counter])

            if sample:
                self.sample_label.setText(f'Sample: {sample}')

            if self.names_list is not None:
                self.sample_name.setText(self.names_list[self.image_counter])
                self.navigation_label.setText(f'{self.image_counter+1}/{self.num_images}')

    def clear(self):
        # if len(self.pixmap_list) > 0:
        self.display.clear_image()
        self.pixmap_list = []
        self.names_list = []
        self.image_counter = 0
        self.num_images = 0
        self.sample_label.setText('Sample: None')
        self.sample_name.setText('None')
        self.navigation_label.setText('Empty')

    def set_no_image_face(self):
        self.display_face_layout.setCurrentWidget(self.no_image_label)

    def set_image_face(self):
        self.display_face_layout.setCurrentWidget(self.image_frame)

    def swap_faces(self):
        if self.display_face_layout.currentWidget() == self.no_image_label:
            # self.display_face_layout.setCurrentWidget(self.image_frame)
            self.set_image_face()
        else:
            # self.display_face_layout.setCurrentWidget(self.no_image_label)
            self.set_no_image_face()

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, o, p, self)
