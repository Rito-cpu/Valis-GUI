import os
from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.gui.models.py_table_widget import PyTableWidget
from src.gui.models.py_toggle import PyToggle


class ImmunoFolderView(QWidget):
    def __init__(
            self,
            font_size: int = 12,
            parent=None
    ) -> None:
        super().__init__()

        if parent != None:
            self.setParent(parent)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setObjectName('ImmunoFolderView')

        themes = Themes()
        self.themes = themes.items

        self._font_size = font_size

        self._setup_widget()
        self.setStyleSheet('QWidget#ImmunoFolderView {{background: {bg_color}; border-radius: 8px;}}'.format(bg_color=self.themes['app_color']['yellow_bg']))

    def _setup_widget(self):
        stack_container = QWidget(self)
        stack_container.setObjectName('stack_container')

        # *** Create default face for widget with no folder entry ***
        self.default_face = QWidget(stack_container)
        self.default_face.setObjectName('default_face')
        # self.default_face.setStyleSheet('background: {bg_color}; border-radius: 8px;'.format(bg_color=self.themes['app_color']['yellow_bg']))

        default_label = QLabel(self.default_face)
        default_label.setObjectName('default_label')
        default_label.setText('No Items')
        default_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        default_label.setStyleSheet('font-size: 12px;')

        default_layout =  QVBoxLayout(self.default_face)
        default_layout.setObjectName('default_layout')
        default_layout.setContentsMargins(5, 5, 5, 5)
        default_layout.addWidget(default_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # *** Create table for sub-folders ***
        self.folder_face = QWidget(stack_container)
        self.folder_face.setObjectName('folder_face')
        # self.folder_face.setStyleSheet('QWidget#folder_face{{background: {bg_color}; border-radius: 8px;}}'.format(bg_color=self.themes['app_color']['yellow_bg']))

        self.folder_table = PyTableWidget(
            radius = 4,
            color = self.themes["app_color"]["text_color"],
            selection_color = self.themes["app_color"]["yellow_bg"],
            bg_color = self.themes["app_color"]["main_bg"],
            header_horizontal_color = self.themes["app_color"]["blue_bg"],
            header_vertical_color = self.themes["app_color"]["blue_bg"],
            bottom_line_color = self.themes["app_color"]["bg_one"],
            grid_line_color = self.themes["app_color"]["bg_one"],
            scroll_bar_bg_color = self.themes["app_color"]["bg_one"],
            scroll_bar_btn_color = self.themes["app_color"]["dark_four"],
            context_color = self.themes["app_color"]["context_color"],
            enable_header_color=True,
            parent=self.folder_face
        )
        self.folder_table.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.folder_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.folder_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.folder_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.folder_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.folder_table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.folder_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        folder_layout = QVBoxLayout(self.folder_face)
        folder_layout.setObjectName('folder_layout')
        folder_layout.setContentsMargins(15, 15, 15, 15)
        folder_layout.addWidget(self.folder_table)

        # *** Create Stack to add multiple widgets ***
        self.face_stack_layout = QStackedLayout(stack_container)
        self.face_stack_layout.setContentsMargins(0, 0, 0, 0)
        self.face_stack_layout.addWidget(self.default_face)
        self.face_stack_layout.addWidget(self.folder_face)
        self.face_stack_layout.setCurrentWidget(self.default_face)

        directory_title = QLabel(self)
        directory_title.setObjectName('directory_title')
        directory_title.setText('Directory Contents')
        directory_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        directory_title.setStyleSheet('font-size: 13px; font-weight: bold; color: {color};'.format(color=self.themes['app_color']['text_color']))

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 17, 10, 5)
        main_layout.setSpacing(3)
        main_layout.addWidget(directory_title, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(stack_container)

    def set_default_face(self):
        self.face_stack_layout.setCurrentWidget(self.default_face)

    def set_table_face(self):
        self.face_stack_layout.setCurrentWidget(self.folder_face)

    def populate_table(self, file_path: str):
        if os.path.isdir(file_path):
            # File directory exists, grab children
            subdirectories = [d for d in os.listdir(file_path) if os.path.isdir(os.path.join(file_path, d))]

            self.folder_table.setRowCount(0)
            self.folder_table.setColumnCount(2)
            self.folder_table.setHorizontalHeaderLabels(['Sub-Directory', 'Include'])
            self.folder_table.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
            self.folder_table.verticalHeader().show()
            self.folder_table.horizontalHeader().show()

            for row, subdirectory in enumerate(subdirectories):
                self.folder_table.insertRow(row)

                label_cell_widget = QWidget(self.folder_table)
                label_cell_widget.setObjectName('label_cell_widget')

                subdir_label = QLabel(label_cell_widget)
                subdir_label.setObjectName('subdir_label')
                subdir_label.setText(subdirectory)
                subdir_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                subdir_label.setStyleSheet('font-size: 11px;')

                label_cell_layout = QHBoxLayout(label_cell_widget)
                label_cell_layout.setContentsMargins(5, 1, 5, 1)
                label_cell_layout.addWidget(subdir_label)

                self.folder_table.setCellWidget(row, 0, label_cell_widget)

                toggle_cell_widget = QWidget(self.folder_table)
                toggle_cell_widget.setObjectName('toggle_cell_widget')

                subdir_toggle = PyToggle(
                    width=28,
                    height=16,
                    ellipse_y=2,
                    bg_color = self.themes['app_color']['text_color'],
                    circle_color = self.themes['app_color']['yellow_bg'],
                    active_color = self.themes['app_color']['blue_bg'],
                    parent=toggle_cell_widget
                )
                subdir_toggle.setObjectName('folder_toggle')
                subdir_toggle.setChecked(True)

                toggle_cell_layout = QHBoxLayout(toggle_cell_widget)
                toggle_cell_layout.setContentsMargins(5, 1, 5, 1)
                toggle_cell_layout.addWidget(subdir_toggle)

                self.folder_table.setCellWidget(row, 1, toggle_cell_widget)

            self.set_table_face()
        else:
            self.folder_table.clearContents()
            self.set_default_face()

    def get_table_data(self):
        subdir_names = []
        subdir_included = []

        for row in range(self.folder_table.rowCount()):
            for col in range(self.folder_table.columnCount()):
                cell_widget = self.folder_table.cellWidget(row, col)

                if cell_widget is not None:
                    if col == 0:
                        # col=0 is subdirectory label
                        widget = cell_widget.findChild(QLabel, 'subdir_label')
                        slide_subdir = widget.text()
                        subdir_names.append(slide_subdir)
                    else:
                        # col=1 is toggle widget
                        widget = cell_widget.findChild(PyToggle, 'folder_toggle')
                        include_subdir = widget.isChecked()
                        subdir_included.append(include_subdir)

        return subdir_names, subdir_included

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, o, p, self)
