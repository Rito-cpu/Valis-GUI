import os
from PyQt6.QtGui import QMouseEvent
import numpy as np

from .styles import body_label_template, title_label_template, viewer_template, navigation_template
from src.core.pyqt_core import *
from src.core.app_config import IMG_RSC_PATH
from src.core.json.json_themes import Themes
from src.core.keyword_store import THMB_DIM
from src.gui.models import PyPushButton
from src.gui.models.qt_combo_widget import QtComboBox
from .qt_graphics_view import QtGraphicsView
from .qt_zoom_frame import QtZoomFrame
from .qt_image_nav import QtImageNav


class QtImageView(QWidget):
    def __init__(
            self,
            dimensions=(THMB_DIM, THMB_DIM),
            padding: int = 100,
            title_size: int = 16,
            font_size: int = 14,
            plus_path: list = ['downloads', 'white_plus.png'],
            minus_path: list = ['downloads', 'white_minus.png'],
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
        self._sample_lookup = None
        self._dropdown_signal_connected = False

        self._plus_path = os.path.join(IMG_RSC_PATH, *plus_path)
        self._minus_path = os.path.join(IMG_RSC_PATH, *minus_path)

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
        self._image_navigator.last_clicked.connect(self.last_image)
        self._image_navigator.next_clicked.connect(self.next_image)
        self._zoom_frame.zoom_in.connect(self.zoom_in)
        self._zoom_frame.zoom_out.connect(self.zoom_out)

    def _setup_widget(self):
        title_format = title_label_template.format(
            _title_size=self._title_size,
            _color = self.themes['app_color']['main_bg']
        )

        image_name_format = title_label_template.format(
            _title_size=self._title_size,
            _color = self.themes['app_color']['text_color']
        )

        body_format = body_label_template.format(
            _font_size = 18,
            _color = self.themes['app_color']['text_color'],
            _bg=self.themes['app_color']['main_bg']
        )

        self.sample_label = QLabel(self)
        self.sample_label.setObjectName('sample_label')
        self.sample_label.setText('Sample: None')
        self.sample_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sample_label.setStyleSheet(title_format)

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

        bottom_frame = QFrame(self.image_frame)
        bottom_frame.setObjectName('bottom_frame')
        bottom_frame.setFrameShape(QFrame.Shape.NoFrame)
        bottom_frame.setFrameShadow(QFrame.Shadow.Plain)

        navigation_frame = QFrame(bottom_frame)
        navigation_frame.setObjectName('navigation_frame')
        navigation_frame.setFrameShape(QFrame.Shape.NoFrame)
        navigation_frame.setFrameShadow(QFrame.Shadow.Plain)
        navigation_format = navigation_template.format(
            _obj_name = navigation_frame.objectName(),
            _color = self.themes['app_color']['main_bg']
        )
        navigation_frame.setStyleSheet(navigation_format)

        self.image_name = QLabel(navigation_frame)
        self.image_name.setObjectName('image_name')
        self.image_name.setText('None')
        self.image_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_name.setStyleSheet(image_name_format)

        self._zoom_frame = QtZoomFrame(parent=navigation_frame)

        self._image_navigator = QtImageNav(parent=navigation_frame)

        navigation_layout = QGridLayout(navigation_frame)
        navigation_layout.setObjectName('navigation_layout')
        navigation_layout.setContentsMargins(10, 10, 10, 10)
        navigation_layout.setSpacing(10)
        navigation_layout.addWidget(self.image_name, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        navigation_layout.addWidget(self._image_navigator, 1, 0, 1, 2)
        navigation_layout.addWidget(self._zoom_frame, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        #navigation_frame.setFixedHeight(navigation_layout.sizeHint().height()+10)
        #navigation_frame.setMinimumWidth(navigation_layout.sizeHint().width() + 10)

        self.results_type_combo = QtComboBox(
            bg_color=self.themes["app_color"]["yellow_bg"],
            text_color=self.themes["app_color"]["text_color"],
            font_size=14,
            parent=bottom_frame
        )
        self.results_type_combo.setObjectName('results_type_combo')
        self.results_type_combo.addItems(['None'])
        self.results_type_combo.setCurrentIndex(0)
        self.results_type_combo.setFixedHeight(30)
        self.results_type_combo.setMinimumWidth(250)

        bottom_layout = QVBoxLayout(bottom_frame)
        bottom_layout.setObjectName('bottom_layout')
        bottom_layout.setContentsMargins(20, 0, 20, 0)
        bottom_layout.setSpacing(15)
        bottom_layout.addWidget(navigation_frame)
        bottom_layout.addWidget(self.results_type_combo, alignment=Qt.AlignmentFlag.AlignCenter)

        frame_layout = QVBoxLayout(self.image_frame)
        frame_layout.setContentsMargins(5, 5, 5, 5)
        frame_layout.setSpacing(18)
        frame_layout.addWidget(self.display)
        frame_layout.addWidget(bottom_frame)
        #frame_layout.addWidget(self.image_name, Qt.AlignmentFlag.AlignCenter)
        #frame_layout.addWidget(navigation_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        #frame_layout.addWidget(self.results_type_combo, alignment=Qt.AlignmentFlag.AlignCenter)

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
                self.image_name.setText(self.names_list[self.image_counter])
                self._image_navigator.change_text(f'{self.image_counter+1}/{self.num_images}')

    def next_image(self):
        if self.image_counter < self.num_images - 1:
            self.image_counter += 1
            self.display.set_image(self.pixmap_list[self.image_counter])
            self.display.reset_zoom()

            if self.names_list is not None:
                self.image_name.setText(self.names_list[self.image_counter])
                self._image_navigator.change_text(f'{self.image_counter+1}/{self.num_images}')

    def add_images(self, image_list, image_names=None):
        if image_list:
            self.image_counter = 0
            self.num_images = len(image_list)
            self.names_list = image_names
            self.pixmap_list = [None] * len(image_list)

            for index, image in enumerate(image_list):
                self.pixmap_list[index] = image # self.img2pixmap(image)

            self.display.set_image(self.pixmap_list[self.image_counter])

            if self.names_list is not None:
                self.image_name.setText(self.names_list[self.image_counter])
                self._image_navigator.change_text(f'{self.image_counter+1}/{self.num_images}')

    def set_dropdown_selections(self, items: list):
        self.results_type_combo.clear()
        self.results_type_combo.addItems(items)
        self.results_type_combo.setCurrentIndex(0)

    def on_index_change(self):
        new_list, new_names = self.get_image_data()
        self.add_images(new_list, new_names)

    def get_image_data(self):
        if self._sample_lookup is not None:
            image_locations = self._sample_lookup[self.results_type_combo.currentText()]
            
            image_list = []
            image_names = []
            for image_path in image_locations:
                head_tail = os.path.split(image_path)
                image_names.append(head_tail[1])

                image_pixmap = QPixmap.fromImage(QImage(image_path))
                image_list.append(image_pixmap)
            
            return image_list, image_names

    def import_sample_data(self, sample_name: str, sample_lookup: dict):
        self.clear()
        self.sample_label.setText(f'Sample: {sample_name}')

        self._sample_lookup = sample_lookup

        selection_keys = sample_lookup.keys()
        self.set_dropdown_selections(selection_keys)

        image_list, image_names = self.get_image_data()
        self.add_images(image_list, image_names)

        self.results_type_combo.currentIndexChanged.connect(self.on_index_change)
        self._dropdown_signal_connected = True

    def clear(self):
        # if len(self.pixmap_list) > 0:
        self.display.clear_image()
        self.pixmap_list = []
        self.names_list = []
        self.image_counter = 0
        self.num_images = 0
        self.sample_label.setText('Sample: None')
        self.image_name.setText('None')
        self._image_navigator.reset()

        self._sample_lookup = None
        if self._dropdown_signal_connected:
            self.results_type_combo.currentIndexChanged.disconnect(self.on_index_change)
            self._dropdown_signal_connected = False

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
