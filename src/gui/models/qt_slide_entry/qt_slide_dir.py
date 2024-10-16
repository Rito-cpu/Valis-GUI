import pathlib

from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.core.scripts.valis import slide_search
from src.gui.models import *
from src.gui.models.qt_line_button import QtButtonLineEdit
from src.gui.models.py_push_button import PyPushButton
from src.gui.models.qt_tree_widget import QtTree
# from .immuno_folder_widget import ImmunoFolderView


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
        self.dir_tree.update_slides_bttn.clicked.connect(self.check_entry)
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
        self.image_dir_entry.setMinimumWidth(750)

        entry_layout = QVBoxLayout(entry_frame)
        entry_layout.setContentsMargins(5, 5, 5, 5)
        entry_layout.setSpacing(15)
        entry_layout.addWidget(self.image_dir_entry, alignment=Qt.AlignmentFlag.AlignCenter)
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
        slide_path = pathlib.Path(self.image_dir_entry.text())

        if self.is_valid_path() and slide_path.is_dir():
            data_dict = slide_search.initiate_process(slide_path)
            if data_dict:
                self.dir_tree.clear()
                self.dir_tree.set_temp_dir(slide_path)
                self.dir_tree.use_directory_widget()
                self.dir_tree.add_data(data_dict)
            else:
                msg_bttns = {
                    "Ok": QMessageBox.ButtonRole.AcceptRole,
                }

                exit_message_box = QtMessage(
                    buttons=msg_bttns,
                    color=self.themes["app_color"]["main_bg"],
                    bg_color_one=self.themes["app_color"]["dark_one"],
                    bg_color_two=self.themes["app_color"]["bg_one"],
                    bg_color_hover=self.themes["app_color"]["dark_three"],
                    bg_color_pressed=self.themes["app_color"]["dark_four"]
                )
                exit_message_box.setIcon(QMessageBox.Icon.Critical)
                exit_message_box.setText("No slide data found.")
                exit_message_box.setDetailedText("No valid slide image files were found in the directory entered.")
                exit_message_box.exec()

                self.dir_tree.clear()

    def check_empty_tree(self):
        is_empty = self.dir_tree.check_empty()

        return is_empty

    def is_valid_path(self):
        return pathlib.Path(self.image_dir_entry.text()).exists()

    def all_toggle_deactivated(self):
        # All toggle buttons are in the unchecked position
        all_false = self.dir_tree.check_all_disabled()

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
        result_dict = self.dir_tree.gather_states()
        result_dict['src_dir'] = str(self.dir_tree._dir_holder)

        return result_dict
