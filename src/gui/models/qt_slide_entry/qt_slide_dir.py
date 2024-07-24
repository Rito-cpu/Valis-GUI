import os

from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.core.scripts.valis import slide_search
from src.gui.models import *
from src.gui.models.qt_line_button import QtButtonLineEdit
from src.gui.models.py_push_button import PyPushButton
from src.gui.models.qt_tree_widget import QtTree
from .immuno_folder_widget import ImmunoFolderView


class QtSlideDirectory(QWidget):
    def __init__(
            self,
            text_color: str = 'black',
            blue_color: str = 'blue',
            yellow_color: str = 'yellow',
            highlight_color: str = 'yellow',
            parent=None
        ):
        super().__init__()

        if parent != None:
            self.setParent(parent)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self._text_color = text_color
        self._blue_color = blue_color
        self._yellow_color = yellow_color
        self._highlight_color = highlight_color

        themes = Themes()
        self.themes = themes.items

        self.setup_widget()

        # *** Slots/Signals ***
        self.submit_slides_bttn.clicked.connect(self.check_entry)
        self.clear_bttn.clicked.connect(self.clear_tree)
        # self.image_dir_entry.entry_changed.connect(self.update_table)

    def setup_widget(self):
        entry_frame = QFrame(self)
        entry_frame.setObjectName('entry_frame')
        entry_frame.setFrameShape(QFrame.Shape.NoFrame)
        entry_frame.setFrameShadow(QFrame.Shadow.Raised)
        entry_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.image_dir_entry = QtButtonLineEdit(
            title="Slide Directory",
            title_color=self._text_color,
            color_three=self._blue_color,
            top_margin=18,
            parent=entry_frame
        )
        self.image_dir_entry.setObjectName(u'image_dir_entry')
        self.image_dir_entry.setMinimumWidth(350)

        button_container = QFrame(entry_frame)
        button_container.setObjectName('button_container')
        button_container.setFrameShape(QFrame.Shape.NoFrame)
        button_container.setFrameShadow(QFrame.Shadow.Raised)
        button_container.setStyleSheet(f"""
        QFrame#button_container {{
            background: lightgray;
            border-radius: 10px;
            border: none;
        }}""")

        self.submit_slides_bttn = PyPushButton(
            text="Update",
            radius=8,
            color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            font_size=14,
            parent=button_container
        )
        self.submit_slides_bttn.setObjectName('submit_slides_bttn')
        self.submit_slides_bttn.setFixedSize(73, 30)

        self.clear_bttn = PyPushButton(
            text="Clear",
            radius=8,
            color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            font_size=14,
            parent=button_container
        )
        self.clear_bttn.setObjectName('clear_bttn')
        self.clear_bttn.setFixedSize(73, 30)

        button_layout = QHBoxLayout(button_container)
        button_layout.setObjectName('button_layout')
        button_layout.setContentsMargins(15, 10, 15, 10)
        button_layout.setSpacing(15)
        button_layout.addWidget(self.submit_slides_bttn)
        button_layout.addWidget(self.clear_bttn)

        entry_layout = QVBoxLayout(entry_frame)
        entry_layout.setContentsMargins(5, 5, 5, 5)
        entry_layout.setSpacing(15)
        entry_layout.addWidget(self.image_dir_entry)
        entry_layout.addWidget(button_container, alignment=Qt.AlignmentFlag.AlignCenter)
        entry_frame.setFixedHeight(entry_layout.sizeHint().height() + 5)
        entry_frame.setMinimumWidth(800)
        entry_frame.setMaximumWidth(950)

        # **** Table view ****
        tree_container = QFrame(self)
        tree_container.setObjectName('tree_container')
        tree_container.setFrameShape(QFrame.Shape.NoFrame)
        tree_container.setFrameShadow(QFrame.Shadow.Plain)

        # self.image_folder_view = ImmunoFolderView(parent=folder_view_container)
        self.dir_tree = QtTree(parent=tree_container)

        tree_layout = QVBoxLayout(tree_container)
        tree_layout.setObjectName('tree_layout')
        tree_layout.setContentsMargins(65, 0, 65, 0)
        tree_layout.addWidget(self.dir_tree)

        # **** Finalize ****
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(30)
        main_layout.addWidget(entry_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(tree_container, alignment=Qt.AlignmentFlag.AlignCenter)

    def set_text(self, text: str):
        self.image_dir_entry.set_text(text)

    def check_entry(self):
        slide_path = self.image_dir_entry.text()

        if self.is_valid_path() and os.path.isdir(slide_path):
            # TODO: Run script to gather files data and add here
            data_dict = slide_search.initiate_process(slide_path)
            if data_dict:
                self.dir_tree.clear()
                self.dir_tree.use_directory_widget()
                self.dir_tree.add_data(data_dict)
            else:
                self.clear_tree()

    def clear_tree(self):
        self.dir_tree.clear()
        self.dir_tree.use_empty_widget()

    def update_table(self):
        directory = self.image_dir_entry.text()
        self.dir_tree.populate_table(directory)

    def is_empty(self):
        empty_entry_check = self.image_dir_entry.text() == ''

        subdir_names, subdir_included = self.dir_tree.get_table_data()
        empty_table_check = len(subdir_names) == 0 and len(subdir_included) == 0

        if empty_entry_check and empty_table_check:
            return True
        return False

    def is_valid_path(self):
        return os.path.exists(self.image_dir_entry.text())

    def has_all_toggled(self):
        # All toggle buttons are in the unchecked position
        _, subdir_included = self.dir_tree.get_table_data()

        all_false = all(not state for state in subdir_included)

        return all_false

    def is_valid_data(self):
        '''
            Checks if the data we have is legitimate for valis process to move forward.
        '''
        # Insert script here? To check for specific files and slides?
        empty_data = self.is_empty()
        valid_path = self.is_valid_path()

        if empty_data or not valid_path:
            return False
        return True

    def get_data(self):
        slide_parent_dir = self.image_dir_entry.text()
        subdir_names, subdir_included = self.dir_tree.get_table_data()

        filtered_names = [name for index, name in enumerate(subdir_names) if subdir_included[index]]

        data_dict = {
            'parent_dir': slide_parent_dir,
            'slide_dirs': filtered_names,
        }

        return data_dict
