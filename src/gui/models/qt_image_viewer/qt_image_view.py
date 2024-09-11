import os
import numpy as np

from .styles import *
from src.core.pyqt_core import *
from src.core.app_config import IMG_RSC_PATH
from src.core.json.json_themes import Themes
from src.core.keyword_store import THMB_DIM
from src.gui.models import PyPushButton
from src.gui.models.qt_combo_widget import QtComboBox
from .qt_graphics_view import QtGraphicsView


class ZoomFrame(QWidget):
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


class ImageNavFrame(QWidget):
    def __init__(
        self,
        left_arrow_path = ['svg_icons', 'icon_arrow_left.svg'],
        right_arrow_path = ['svg_icons', 'icon_arrow_right.svg'],
        parent=None
    ):
        super().__init__()

        if parent is not None:
            self.setParent(parent)

        themes = Themes()
        self.themes = themes.items

        self.left_arrow = os.path.join(IMG_RSC_PATH, *left_arrow_path)
        self.right_arrow = os.path.join(IMG_RSC_PATH, *right_arrow_path)

        self._setup_widget()

    def _setup_widget(self):
        testing_temp = """
            QToolButton {{
                background: {_color};
                border: none;
                border-radius: 6px;
                color: {text_color};
            }}
        """
        tool_bttn_format = testing_temp.format(
            _color = self.themes['app_color']['blue_bg'],
            text_color = self.themes['app_color']['main_bg']
        )

        #container_frame = QFrame(self)

        self.previous_bttn = QToolButton(self)
        self.previous_bttn.setObjectName('previous_bttn')
        self.previous_bttn.setIcon(QIcon(self.left_arrow))
        self.previous_bttn.setText('Previous')
        self.previous_bttn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.previous_bttn.setIconSize(QSize(18, 18))
        self.previous_bttn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.previous_bttn.setStyleSheet(tool_bttn_format)

        self.next_bttn = QToolButton(self)
        self.next_bttn.setObjectName('next_bttn')
        self.next_bttn.setIcon(QIcon(self.right_arrow))
        self.next_bttn.setText('Next')
        self.next_bttn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.next_bttn.setIconSize(QSize(18, 18))
        self.next_bttn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.next_bttn.setStyleSheet(tool_bttn_format)

        main_layout = QHBoxLayout(self)
        main_layout.setObjectName('main_layout')
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.previous_bttn)
        main_layout.addWidget(self.next_bttn)


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
        self.last_bttn.clicked.connect(self.last_image)
        self.next_bttn.clicked.connect(self.next_image)
        self.zoom_frame.zoom_in.connect(self.zoom_in)
        self.zoom_frame.zoom_out.connect(self.zoom_out)

    def _setup_widget(self):
        title_format = title_label_template.format(
            _title_size=self._title_size,
            _color = self.themes['app_color']['main_bg']
        )

        body_format = body_label_template.format(
            _font_size = self._font_size,
            _color = self.themes['app_color']['main_bg']
        )

        tool_bttn_format = tool_bttn_template.format(
            _color = self.themes['app_color']['blue_bg']
        )

        self.sample_label = QLabel(self)
        self.sample_label.setObjectName('sample_label')
        self.sample_label.setText('Sample: None')
        self.sample_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sample_label.setStyleSheet(title_format)

        self.image_name = QLabel(self)
        self.image_name.setObjectName('image_name')
        self.image_name.setText('None')
        self.image_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_name.setStyleSheet(title_format)

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

        self.zoom_frame = ZoomFrame(parent=navigation_frame)

        navigation_layout = QGridLayout(navigation_frame)
        navigation_layout.setObjectName('navigation_layout')
        navigation_layout.setContentsMargins(10, 10, 10, 10)
        navigation_layout.setSpacing(10)
        navigation_layout.addWidget(self.navigation_label, 0, 0, 1, 2)
        navigation_layout.addWidget(self.last_bttn, 1, 0, 1, 1)
        navigation_layout.addWidget(self.next_bttn, 1, 1, 1, 1)
        #navigation_layout.addWidget(test, 2, 0, 1, 2)
        navigation_layout.addWidget(self.zoom_frame, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        navigation_frame.setFixedHeight(navigation_layout.sizeHint().height()+10)
        navigation_frame.setMinimumWidth(navigation_layout.sizeHint().width() + 10)

        self.results_type_combo = QtComboBox(
            bg_color=self.themes["app_color"]["yellow_bg"],
            text_color=self.themes["app_color"]["text_color"],
            parent=self.image_frame
        )
        self.results_type_combo.setObjectName('results_type_combo')
        self.results_type_combo.addItems(['None'])
        self.results_type_combo.setCurrentIndex(0)
        self.results_type_combo.setFixedHeight(30)
        self.results_type_combo.setMinimumWidth(250)

        frame_layout = QVBoxLayout(self.image_frame)
        frame_layout.setContentsMargins(5, 5, 5, 5)
        frame_layout.setSpacing(5)
        frame_layout.addWidget(self.display)
        frame_layout.addWidget(self.image_name, Qt.AlignmentFlag.AlignCenter)
        frame_layout.addWidget(navigation_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        frame_layout.addWidget(self.results_type_combo, alignment=Qt.AlignmentFlag.AlignCenter)

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
                self.navigation_label.setText(f'{self.image_counter+1}/{self.num_images}')

    def next_image(self):
        if self.image_counter < self.num_images - 1:
            self.image_counter += 1
            self.display.set_image(self.pixmap_list[self.image_counter])
            self.display.reset_zoom()

            if self.names_list is not None:
                self.image_name.setText(self.names_list[self.image_counter])
                self.navigation_label.setText(f'{self.image_counter+1}/{self.num_images}')

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
                self.navigation_label.setText(f'{self.image_counter+1}/{self.num_images}')

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
        self.navigation_label.setText('Empty')

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
