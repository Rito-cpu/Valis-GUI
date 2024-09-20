import os
import re
import shutil

from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.core.validation.validate_file import is_existing_dir
from .qt_button_line_edit import QtButtonLineEdit
from src.gui.models import PyPushButton
from src.gui.models.qt_marquee import QtMarqueeLabel
from src.gui.models.qt_message import QtMessage


class QtOutputEntry(QWidget):
    directory_changed = pyqtSignal(QWidget)

    def __init__(
        self, 
        font_size: int = 13, 
        parent = None
    ):
        super().__init__()

        if parent is not None:
            self.setParent(parent)

        themes = Themes()
        self.themes = themes.items
        self._font_size = font_size

        self._setup_widget()

        self.submit_bttn.clicked.connect(self.submit_bttn_clicked)

    def _setup_widget(self):
        container_frame = QFrame(self)
        container_frame.setObjectName('container_frame')
        container_frame.setFrameShape(QFrame.Shape.NoFrame)
        container_frame.setFrameShadow(QFrame.Shadow.Plain)
        container_frame.setStyleSheet(f"""
            QFrame#container_frame {{
                border: 2px solid #eeeeee;
                border-radius: 8px;
            }}
        """)

        entry_row_frame = QFrame(container_frame)
        entry_row_frame.setObjectName('entry_row_frame')
        entry_row_frame.setFrameShape(QFrame.Shape.NoFrame)
        entry_row_frame.setFrameShadow(QFrame.Shadow.Plain)

        self.output_dir_entry = QtButtonLineEdit(
            title="Output Directory",
            title_color=self.themes["app_color"]["text_color"],
            color_three=self.themes['app_color']['blue_bg'],
            top_margin=18,
            parent=entry_row_frame
        )
        self.output_dir_entry.setObjectName('output_directory')
        self.output_dir_entry.setMinimumWidth(475)

        bttn_container = QFrame(container_frame)
        bttn_container.setObjectName('bttn_container')
        bttn_container.setFrameShape(QFrame.Shape.NoFrame)
        bttn_container.setFrameShadow(QFrame.Shadow.Plain)

        self.submit_bttn = PyPushButton(
            text="Submit",
            radius=8,
            color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            parent=bttn_container
        )
        self.submit_bttn.setObjectName('dir_submit_bttn')
        self.submit_bttn.setMinimumSize(78, 31)

        bttn_layout = QVBoxLayout(bttn_container)
        bttn_layout.setObjectName('bttn_layout')
        bttn_layout.setContentsMargins(0, 17, 3, 0)
        bttn_layout.addWidget(self.submit_bttn)

        entry_row_layout = QHBoxLayout(entry_row_frame)
        entry_row_layout.setObjectName('entry_row_layout')
        entry_row_layout.setContentsMargins(0, 0, 0, 0)
        entry_row_layout.setSpacing(15)
        entry_row_layout.addWidget(self.output_dir_entry)
        entry_row_layout.addWidget(bttn_container)

        marquee_frame = QFrame(container_frame)
        marquee_frame.setObjectName('marquee_frame')
        marquee_frame.setFrameShape(QFrame.Shape.NoFrame)
        marquee_frame.setFrameShadow(QFrame.Shadow.Plain)
        marquee_frame.setStyleSheet(f"""
            QFrame#marquee_frame{{
                background-color: {self.themes["app_color"]["blue_bg"]};
                border-radius: 6px;
            }}
        """)

        header_label = QLabel(marquee_frame)
        header_label.setObjectName('header_label')
        header_label.setText('Output Directory:')
        header_label.setStyleSheet(f'color: {self.themes["app_color"]["main_bg"]}; font-size: {self._font_size}px;')

        self.dir_marquee_label = QtMarqueeLabel(
            color=self.themes["app_color"]["main_bg"],
            parent=marquee_frame
        )
        self.dir_marquee_label.setObjectName('dir_marquee_label')
        self.dir_marquee_label.setMinimumWidth(415)
        self.dir_marquee_label.setText('None')

        marquee_layout = QHBoxLayout(marquee_frame)
        marquee_layout.setObjectName('marquee_layout')
        marquee_layout.setContentsMargins(10, 5, 10, 5)
        marquee_layout.setSpacing(10)
        marquee_layout.addWidget(header_label, alignment=Qt.AlignmentFlag.AlignLeft)
        marquee_layout.addWidget(self.dir_marquee_label, alignment=Qt.AlignmentFlag.AlignLeft)
        marquee_layout.addStretch(1)

        container_layout = QVBoxLayout(container_frame)
        container_layout.setObjectName('container_layout')
        container_layout.setContentsMargins(10, 10, 10, 10)
        container_layout.setSpacing(5)
        container_layout.addWidget(entry_row_frame)
        container_layout.addWidget(marquee_frame)

        main_layout = QVBoxLayout(self)
        main_layout.setObjectName('main_layout')
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container_frame)

    def get_text(self):
        return self.output_dir_entry.text()

    def set_text(self, new_text: str):
        self.dir_marquee_label.setText(new_text)

    def submit_bttn_clicked(self):
        return_val = self.check_empty()
        if return_val is None:
            return
        else:
            self.directory_changed.emit(self)

    def validate_directory(self):
        current_dir = self.output_dir_entry.text()
        if not is_existing_dir(current_dir):
            message = f"The directory '{current_dir}' does not exist. Please enter a valid directory."
            msg_bttns = {
                "Ok": QMessageBox.ButtonRole.AcceptRole
            }
            error_msg = QtMessage(
                buttons=msg_bttns,
                color=self.themes["app_color"]["main_bg"],
                bg_color_one=self.themes["app_color"]["dark_one"],
                bg_color_two=self.themes["app_color"]["bg_one"],
                bg_color_hover=self.themes["app_color"]["dark_three"],
                bg_color_pressed=self.themes["app_color"]["dark_four"]
            )
            error_msg.setIcon(QMessageBox.Icon.Warning)
            error_msg.setText('Non-existing directory entered.')
            error_msg.setDetailedText(message)
            error_msg.exec()
            return None
        return current_dir

    def check_empty(self):
        return_val = self.validate_directory()
        if return_val is None:
            return None
        
        items = [entry.name for entry in os.scandir(return_val)]
        if items:
            message = """Existing folders/files have been found. Would you like to delete these items?
            \nNot deleting the contents will create a new folder inside the entered directory to store data from the current run.
            \nNote: If these existing folders/files are not from a previous run and are unrelated to the Valis process, we recommend deleting these items."""
            msg_bttns = {
                "Yes": QMessageBox.ButtonRole.YesRole,
                "No": QMessageBox.ButtonRole.NoRole
            }
            error_msg = QtMessage(
                buttons=msg_bttns,
                color=self.themes["app_color"]["main_bg"],
                bg_color_one=self.themes["app_color"]["dark_one"],
                bg_color_two=self.themes["app_color"]["bg_one"],
                bg_color_hover=self.themes["app_color"]["dark_three"],
                bg_color_pressed=self.themes["app_color"]["dark_four"]
            )
            error_msg.setIcon(QMessageBox.Icon.Information)
            error_msg.setText('Output directory is not empty. Do you want to delete its contents?')
            error_msg.setDetailedText(message)
            error_msg.exec()

            if error_msg.clickedButton() == error_msg.buttons["Yes"]:
                # Yes is pressed, delete existing items
                for item in items:
                    item_path = os.path.join(return_val, item)
                    try:
                        if os.path.isfile(item_path) or os.path.islink(item_path):
                            os.unlink(item_path)
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                    except Exception as error:
                        msg_bttns = {
                            "Ok": QMessageBox.ButtonRole.AcceptRole
                        }
                        error_msg = QtMessage(
                            buttons=msg_bttns,
                            color=self.themes["app_color"]["main_bg"],
                            bg_color_one=self.themes["app_color"]["dark_one"],
                            bg_color_two=self.themes["app_color"]["bg_one"],
                            bg_color_hover=self.themes["app_color"]["dark_three"],
                            bg_color_pressed=self.themes["app_color"]["dark_four"]
                        )
                        error_msg.setIcon(QMessageBox.Icon.Critical)
                        error_msg.setText(f'Error ocurred while deleting {item_path}.')
                        error_msg.setDetailedText(f'Error found:\n{error}')
                        error_msg.exec()
                        return None
                return return_val
            else:
                # No is pressed, create additional folder
                basename = 'valis_output'
                regex_pattern = re.compile(rf"^{re.escape(basename)} \((d+)\)$")
                copy_num = 1

                for item in items:
                    item_path = os.path.join(return_val, item)
                    if os.path.isdir(item_path):
                        match = regex_pattern.match(item)
                        if match:
                            existing_num = int(match.group(1))
                            if existing_num == copy_num:
                                copy_num = existing_num + 1
                    else:
                        continue

                new_folder_name = f"{basename} ({copy_num+1})"
                new_folder_path = os.path.join(return_val, new_folder_name)
                os.mkdir(new_folder_path)

                self.output_dir_entry.set_text(new_folder_path)

                return new_folder_path
        else:
            return return_val
