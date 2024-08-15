import pathlib
import os

from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.core.app_config import SUBMITTED_SLIDES, SLIDE_UPLOAD_STATE, INCOMPLETE
from src.core.keyword_store import FLUORESCENCE_KEY, BF_KEY
from src.gui.models import PyToggle, QtComboBox, PyPushButton
from .qt_dir_widget import DirectoryWidget


class QtTree(QWidget):
    def __init__(
        self,
        font_size: int = 12,
        parent=None
    ):
        super().__init__()

        if parent is not None:
            self.parent = parent

        self._font_size = font_size
        self._file_dict = {}
        self._dir_holder = None

        themes = Themes()
        self.themes = themes.items

        self._setup_widget()

        self.clear_bttn.clicked.connect(self.clear)

    def _setup_widget(self):
        tree_title_frame = QFrame(self)
        tree_title_frame.setObjectName('tree_title_frame')
        tree_title_frame.setFrameShape(QFrame.Shape.NoFrame)
        tree_title_frame.setFrameShadow(QFrame.Shadow.Plain)

        container_frame = QFrame(tree_title_frame)
        container_frame.setObjectName('container_frame')
        container_frame.setFrameShape(QFrame.Shape.NoFrame)
        container_frame.setFrameShadow(QFrame.Shadow.Plain)
        container_frame.setStyleSheet(f"""
            QFrame#container_frame {{
                background-color: {self.themes['app_color']['yellow_bg']};
                border: none;
                border-radius: 9px;
            }}""")
        
        title_container = QFrame(tree_title_frame)
        title_container.setObjectName('title_container')
        title_container.setFrameShape(QFrame.Shape.NoFrame)
        title_container.setFrameShadow(QFrame.Shadow.Plain)
        title_container.setStyleSheet(f"""
            QFrame#title_container {{
                background-color: {self.themes['app_color']['yellow_bg']};
                border: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }}""")
        
        title_label = QLabel(title_container)
        title_label.setObjectName('title_label')
        title_label.setText('Directory Contents')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(f'color: {self.themes["app_color"]["text_color"]}; font-size: {self._font_size}px; font-weight: bold;')

        title_layout = QVBoxLayout(title_container)
        title_layout.setObjectName('title_layout')
        title_layout.setContentsMargins(15, 10, 15, 5)
        title_layout.addWidget(title_label)

        self._stack_widget = QStackedWidget(container_frame)

        self._file_tree = QTreeWidget(self._stack_widget)
        self._file_tree.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._file_tree.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._file_tree.setColumnCount(5)
        self._file_tree.setHeaderLabels(['Directory', 'Filename', 'Include', 'Type', 'Reference File'])
        self._file_tree.setColumnWidth(0, 140)
        self._file_tree.setColumnWidth(1, 150)
        self._file_tree.setColumnWidth(2, 60)
        self._file_tree.setColumnWidth(3, 150)
        self._file_tree.setColumnWidth(4, 75)
        self._file_tree.setMinimumSize(625, 350)
        #self._file_tree.setFixedWidth(600)
        self._file_tree.setStyleSheet(f"""
            QTreeWidget {{
                border: 1px solid black;
                background: white;
                font-size: 12px;
            }}
            QTreeWidget::item {{
                font-size: 12px;
                border: 1px solid lightgray;
            }}
            QTreeView::item {{
                background: transparent;
                border: none;
                color: {self.themes['app_color']['text_color']};
            }}
            QHeaderView::section {{
                font-size: 12px;
                color: {self.themes['app_color']['main_bg']};
                background: {self.themes['app_color']['dark_three']};
                padding-left: 5px;
            }}""")

        self._empty_label = QLabel(self._stack_widget)
        self._empty_label.setObjectName('empty_label')
        self._empty_label.setText('No Directory')
        self._empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty_label.setStyleSheet(f'color: {self.themes["app_color"]["text_color"]}; font-size: {self._font_size}px;')

        self._stack_widget.addWidget(self._file_tree)
        self._stack_widget.addWidget(self._empty_label)
        self._stack_widget.setCurrentIndex(1)

        button_buffer = QFrame(self)
        button_buffer.setObjectName('button_buffer')
        button_buffer.setFrameShape(QFrame.Shape.NoFrame)
        button_buffer.setFrameShadow(QFrame.Shadow.Plain)
        button_buffer.setStyleSheet(f"""
            QFrame#button_buffer{{
                background: {self.themes['app_color']['yellow_bg']};
                border: none;
                border-top-left-radius: 9px;
                border-bottom-left-radius: 9px;
            }}""")

        button_container = QFrame(button_buffer)
        button_container.setObjectName('button_container')
        button_container.setFrameShape(QFrame.Shape.NoFrame)
        button_container.setFrameShadow(QFrame.Shadow.Raised)
        button_container.setStyleSheet(f"""
            QFrame#button_container {{
                background: rgba(255, 255, 255, 0.75);
                border: none;
                border-radius: 9px;
            }}
        """)

        self.update_slides_bttn = PyPushButton(
            text="Update",
            radius=8,
            color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["blue_bg"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            font_size=14,
            parent=button_container
        )
        self.update_slides_bttn.setObjectName('submit_slides_bttn')
        self.update_slides_bttn.setFixedSize(60, 28)

        self.clear_bttn = PyPushButton(
            text="Clear",
            radius=8,
            color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["blue_bg"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            font_size=14,
            parent=button_container
        )
        self.clear_bttn.setObjectName('clear_bttn')
        self.clear_bttn.setFixedSize(60, 28)
        self.clear_bttn.setDisabled(True)

        button_layout = QVBoxLayout(button_container)
        button_layout.setObjectName('button_layout')
        button_layout.setContentsMargins(8, 10, 8, 10)
        button_layout.setSpacing(30)
        button_layout.addWidget(self.update_slides_bttn, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.clear_bttn, alignment=Qt.AlignmentFlag.AlignCenter)

        buffer_layout = QVBoxLayout(button_buffer)
        buffer_layout.setObjectName('buffer_layout')
        buffer_layout.setContentsMargins(7, 18, 5, 18)
        buffer_layout.addWidget(button_container)

        container_layout = QHBoxLayout(container_frame)
        container_layout.setObjectName('container_layout')
        # container_layout.setContentsMargins(40, 15, 40, 10)
        container_layout.setContentsMargins(10, 15, 10, 10)
        container_layout.setSpacing(8)
        #container_layout.addWidget(button_container, alignment=Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(self._stack_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        container_frame.setFixedSize(container_layout.sizeHint())

        tree_title_layout = QVBoxLayout(tree_title_frame)
        tree_title_layout.setObjectName('tree_title_layout')
        tree_title_layout.setContentsMargins(0, 0, 0, 0)
        tree_title_layout.setSpacing(0)
        tree_title_layout.addWidget(title_container, alignment=Qt.AlignmentFlag.AlignHCenter)
        tree_title_layout.addWidget(container_frame, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout = QHBoxLayout(self)
        main_layout.setObjectName('main_layout')
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(button_buffer, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(tree_title_frame)

    def use_empty_widget(self):
        self._stack_widget.setCurrentWidget(self._empty_label)
        self.clear_bttn.setDisabled(True)

    def use_directory_widget(self):
        self._stack_widget.setCurrentWidget(self._file_tree)
        self.clear_bttn.setEnabled(True)

    def add_data(self, data_dict: dict):
        # TODO: How to handle filepaths for different OS?
        if data_dict:
            samples_dict: dict
            for dir, samples_dict in data_dict.items():
                dir_item = DirectoryWidget(dir_name=dir, parent=self._file_tree)
                top_level_item = QTreeWidgetItem(self._file_tree)
                self._file_tree.setItemWidget(top_level_item, 0, dir_item)

                sample_data: dict
                for sample_name, sample_data in samples_dict.items():
                    sample_path = sample_data['File']
                    leaf = os.path.basename(sample_path)
                    self._file_dict[leaf] = sample_path
                    include_sample = sample_data['Include']
                    img_type = sample_data['Image type']

                    include_container = QWidget(self._file_tree)
                    include_container.setObjectName('include_container')

                    include_toggle = PyToggle(
                        width=28,
                        height=16,
                        ellipse_y=2,
                        bg_color = self.themes['app_color']['text_color'],
                        circle_color = self.themes['app_color']['yellow_bg'],
                        active_color = self.themes['app_color']['blue_bg'],
                        parent=include_container
                    )
                    include_toggle.setObjectName('include_toggle')
                    include_toggle.setChecked(include_sample)

                    include_layout = QVBoxLayout(include_container)
                    include_layout.setObjectName('include_layout')
                    include_layout.setContentsMargins(5, 5, 5, 5)
                    include_layout.addWidget(include_toggle)

                    combo_container = QWidget(self._file_tree)
                    combo_container.setObjectName('combo_container')

                    image_type_dropdown = QtComboBox(
                        bg_color=self.themes["app_color"]["dark_one"],
                        text_color=self.themes["app_color"]["text_color"],
                        parent=combo_container
                    )
                    image_type_dropdown.setObjectName('image_type_dropdown')
                    image_type_dropdown.setCursor(Qt.CursorShape.PointingHandCursor)
                    image_type_dropdown.addItems([FLUORESCENCE_KEY, BF_KEY])
                    image_type_dropdown.setCurrentText(img_type)
                    image_type_dropdown.setFixedHeight(23)
                    image_type_dropdown.setMinimumWidth(95)
                    image_type_dropdown.setMaximumWidth(120)

                    combo_layout = QVBoxLayout(combo_container)
                    combo_layout.setObjectName('combo_layout')
                    combo_layout.setContentsMargins(5, 5, 5, 5)
                    combo_layout.addWidget(image_type_dropdown)

                    reference_container = QWidget(self._file_tree)
                    reference_container.setObjectName('reference_container')

                    reference_toggle = PyToggle(
                        width=28,
                        height=16,
                        ellipse_y=2,
                        bg_color = self.themes['app_color']['text_color'],
                        circle_color = self.themes['app_color']['yellow_bg'],
                        active_color = self.themes['app_color']['blue_bg'],
                        parent=reference_container
                    )
                    reference_toggle.setObjectName('reference_toggle')
                    reference_toggle.setChecked(False)

                    reference_layout = QVBoxLayout(reference_container)
                    reference_layout.setObjectName('reference_layout')
                    reference_layout.setContentsMargins(5, 5, 5, 5)
                    reference_layout.addWidget(reference_toggle)

                    dir_child = QTreeWidgetItem(top_level_item)
                    dir_child.setText(1, leaf)
                    dir_child.setTextAlignment(1, Qt.AlignmentFlag.AlignCenter)
                    self._file_tree.setItemWidget(dir_child, 2, include_container)
                    dir_child.setTextAlignment(2, Qt.AlignmentFlag.AlignCenter)
                    self._file_tree.setItemWidget(dir_child, 3, combo_container)
                    dir_child.setTextAlignment(3, Qt.AlignmentFlag.AlignCenter)
                    self._file_tree.setItemWidget(dir_child, 4, reference_container)
                    dir_child.setTextAlignment(4, Qt.AlignmentFlag.AlignCenter)
        else:
            self.clear()
            self.use_empty_widget()
            return

    def gather_states(self):
        result = {
            'src_dir': None
        }

        root = self._file_tree.invisibleRootItem()
        for index in range(root.childCount()):
            dir_item = root.child(index)
            dir_widget: DirectoryWidget
            dir_widget = self._file_tree.itemWidget(dir_item, 0)
            dir_name = dir_widget.get_text()
            is_dir_sorted = dir_widget.is_sorted()

            dir_info = {
                'is_sorted': is_dir_sorted
            }
            files_info = {}
            for file_index in range(dir_item.childCount()):
                file_item = dir_item.child(file_index)
                file_name = self._file_dict[file_item.text(1)]
                include_toggle = self._file_tree.itemWidget(file_item, 2).findChild(PyToggle, 'include_toggle')
                include_file = include_toggle.isChecked()
                img_type_dropdown = self._file_tree.itemWidget(file_item, 3).findChild(QComboBox, 'image_type_dropdown')
                img_type = img_type_dropdown.currentText()
                reference_toggle = self._file_tree.itemWidget(file_item, 4).findChild(PyToggle, 'reference_toggle')
                use_reference = reference_toggle.isChecked()

                files_info[file_index] = {
                    "File": file_name,
                    "Include": include_file,
                    "Image type": img_type,
                    "Use reference": use_reference
                }

            dir_info["files"] = files_info
            result[dir_name] = dir_info
        return result
    
    def check_all_disabled(self):
        bool_list = []

        root = self._file_tree.invisibleRootItem()
        for index in range(root.childCount()):
            dir_item = root.child(index)
            for file_index in range(dir_item.childCount()):
                file_item = dir_item.child(file_index)
                combo_wid = self._file_tree.itemWidget(file_item, 2).findChild(PyToggle, 'include_toggle')
                bool_list.append(combo_wid.isChecked())

        all_false = all(not state for state in bool_list)
        return all_false

    def check_empty(self):
        if self._file_tree.topLevelItemCount() > 0:
            return False
        else:
            return True

    def set_temp_dir(self, dir: str):
        self._dir_holder = dir

    def clear(self):
        self._file_tree.clear()
        self._file_dict.clear()
        self._dir_holder = None
        self.use_empty_widget()
