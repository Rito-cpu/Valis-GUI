import pathlib
import os

from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.core.keyword_store import FLUORESCENCE_KEY, BF_KEY
from src.gui.models import PyToggle, QtComboBox
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

        themes = Themes()
        self.themes = themes.items

        self._setup_widget()

    def _setup_widget(self):
        container_frame = QFrame(self)
        container_frame.setObjectName('container_frame')
        container_frame.setFrameShape(QFrame.Shape.NoFrame)
        container_frame.setFrameShadow(QFrame.Shadow.Plain)
        container_frame.setStyleSheet(f"""
            QFrame#container_frame {{
                background-color: {self.themes['app_color']['yellow_bg']};
                border: none;
                border-radius: 8px;
            }}""")
        
        title_label = QLabel(container_frame)
        title_label.setObjectName('title_label')
        title_label.setText('Directory Contents')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(f'color: {self.themes["app_color"]["text_color"]}; font-size: {self._font_size}px;')

        self._stack_widget = QStackedWidget(container_frame)

        self._file_tree = QTreeWidget(self._stack_widget)
        self._file_tree.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._file_tree.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._file_tree.setColumnCount(4)
        self._file_tree.setHeaderLabels(['Directory', 'Filename', 'Include', 'Type'])
        self._file_tree.setColumnWidth(0, 200)
        self._file_tree.setColumnWidth(1, 150)
        self._file_tree.setColumnWidth(2, 60)
        self._file_tree.setMinimumSize(650, 350)
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

        container_layout = QVBoxLayout(container_frame)
        container_layout.setObjectName('container_layout')
        container_layout.setContentsMargins(40, 15, 40, 10)
        container_layout.setSpacing(15)
        container_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(self._stack_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        container_frame.setFixedSize(container_layout.sizeHint())

        main_layout = QVBoxLayout(self)
        main_layout.setObjectName('main_layout')
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container_frame)

    def use_empty_widget(self):
        self._stack_widget.setCurrentWidget(self._empty_label)

    def use_directory_widget(self):
        self._stack_widget.setCurrentWidget(self._file_tree)

    def add_row(self):
        dir_item = DirectoryWidget(dir_name='Dir Name', parent=self._file_tree)
        item_1 = QTreeWidgetItem(self._file_tree)
        self._file_tree.setItemWidget(item_1, 0, dir_item)
        child_1 = QTreeWidgetItem(item_1)
        child_1.setText(1, 'Testing 1')
        child_1.setText(2, 'Testing 2')
        child_2 = QTreeWidgetItem(item_1)
        child_2.setText(1, 'Testing 3')
        child_2.setText(2, 'Testing 4')

    def add_data(self, data_dict: dict):
        # TODO: How to handle filepaths for different OS?
        # TODO: If search returns empty, need to display
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
                    include_sample = sample_data['Include']
                    img_type = sample_data['Image type']

                    include_toggle = PyToggle(
                        width=28,
                        height=16,
                        ellipse_y=2,
                        bg_color = self.themes['app_color']['text_color'],
                        circle_color = self.themes['app_color']['yellow_bg'],
                        active_color = self.themes['app_color']['blue_bg'],
                        parent=self._file_tree
                    )
                    include_toggle.setChecked(include_sample)

                    image_type_dropdown = QtComboBox(
                        bg_color=self.themes["app_color"]["dark_one"],
                        text_color=self.themes["app_color"]["text_color"],
                        parent=self._file_tree
                    )
                    image_type_dropdown.setObjectName('image_type_dropdown')
                    image_type_dropdown.setCursor(Qt.CursorShape.PointingHandCursor)
                    image_type_dropdown.addItems([FLUORESCENCE_KEY, BF_KEY])
                    image_type_dropdown.setCurrentText(img_type)
                    image_type_dropdown.setFixedHeight(20)
                    image_type_dropdown.setMinimumWidth(75)

                    dir_child = QTreeWidgetItem(top_level_item)
                    #dir_child.setTextAlignment(column=1, alignment=Qt.AlignmentFlag.AlignCenter)
                    #dir_child.setTextAlignment(column=2, alignment=Qt.AlignmentFlag.AlignCenter)
                    dir_child.setText(1, leaf)
                    self._file_tree.setItemWidget(dir_child, 2, include_toggle)
                    self._file_tree.setItemWidget(dir_child, 3, image_type_dropdown)
        else:
            self.clear()
            self.use_empty_widget()
            return

    def gather_states(self):
        result = {}

        root = self._file_tree.invisibleRootItem()
        for index in range(root.childCount()):
            dir_item = root.child(index)
            dir_widget: DirectoryWidget
            dir_widget = self._file_tree.itemWidget(dir_item, 0)
            dir_name = dir_widget.get_text()
            is_dir_sorted = dir_widget.is_sorted()

            files_info = []
            for file_index in range(dir_item.childCount()):
                file_item = dir_item.child(file_index)
                file_name = file_item.text(1)
                file_chbx = self._file_tree.itemWidget(file_item, 2)
                file_include = file_chbx.isChecked()

                files_info.append((file_name, file_include))
            result[dir_name] = files_info
        print(f'Result:\n{result}')
        return result

    def clear(self):
        self._file_tree.clear()
