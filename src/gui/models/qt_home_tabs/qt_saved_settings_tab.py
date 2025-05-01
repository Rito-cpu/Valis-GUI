import pathlib

from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.gui.models.qt_line_button import QtOutputEntry, QtButtonLineEdit
from src.gui.models.py_push_button import PyPushButton
from src.gui.models.qt_message import QtMessage
from .qt_file_obj import QtFileWidget

tab_description = '''
<p style=\"text-align: center\">This tab gives the ability to enter valis gui settings that were saved 
from a previous session and run the valis registration software using these entered settings.</p>'''


class SavedSettingsTab(QWidget):
    emit_dict = pyqtSignal(dict)

    def __init__(
        self,
        parent=None
    ):
        super().__init__()
        
        if parent is not None:
            self.parent = parent
        
        themes = Themes()
        self.themes = themes.items
        self._obj_counter = 0
        self._obj_dict = {}

        self._setup_widget()
        self.add_file_bttn.clicked.connect(self.add_file)
        self.clear_bttn.clicked.connect(self.clear_files)
        self.run_bttn.clicked.connect(self.submit_files)

    def _setup_widget(self):
        groupbox_template = """
            QGroupBox {{
                color: {color};
                background: {bg_color};
                font-size: {title_size}px;
                border: 1px solid black;
                border-radius: {border_radius}px;
                margin-top: {margin_top}px;
            }}
            QGroupBox:title {{
                color: {color_two};
                subcontrol-origin: margin;
                subcontrol-position: top-center;
            }}
        """
        gb_style = groupbox_template.format(
            color=self.themes['app_color']['main_bg'],
            color_two=self.themes['app_color']['text_color'],
            bg_color=self.themes['app_color']['main_bg'],
            title_size=16,
            border_radius=8,
            margin_top=20,
            font_size=13
        )
        
        container_frame = QFrame(self)
        container_frame.setObjectName('container_frame')
        container_frame.setFrameShape(QFrame.Shape.NoFrame)
        container_frame.setFrameShadow(QFrame.Shadow.Plain)

        short_description_frame = QFrame(container_frame)
        short_description_frame.setObjectName('short_description_frame')
        short_description_frame.setFrameShape(QFrame.Shape.NoFrame)
        short_description_frame.setFrameShadow(QFrame.Shadow.Plain)
        short_description_frame.setStyleSheet('QFrame#short_description_frame{border: none;}')
        
        top_label = QLabel(short_description_frame)
        top_label.setObjectName('top_label')
        top_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_label.setText("Already Used VALIS Before?")
        top_label.setStyleSheet('font-weight: bold; font-size: 22px;')

        short_description = QTextEdit(short_description_frame)
        short_description.setObjectName("short_description")
        short_description.setReadOnly(True)
        short_description.setText(tab_description)
        short_description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        short_description.setStyleSheet(f'border: none; background: transparent; font-size: 16px;')
        doc_height = short_description.document().size().height()
        margin_top = short_description.contentsMargins().top()
        margin_bottom = short_description.contentsMargins().bottom()
        # short_description.setFixedHeight(doc_height + margin_top + margin_bottom + 4)
        short_description.setFixedHeight(60)

        short_description_layout = QVBoxLayout(short_description_frame)
        short_description_layout.setObjectName('short_description_layout')
        short_description_layout.setContentsMargins(60, 0, 60, 10)
        short_description_layout.setSpacing(15)
        short_description_layout.addWidget(top_label)
        short_description_layout.addWidget(short_description)
        short_description_frame.setFixedHeight(short_description_layout.sizeHint().height() + 8)

        file_scroll_area = QScrollArea(container_frame)
        file_scroll_area.setObjectName("scroll_area")
        file_scroll_area.setStyleSheet("background: transparent;")
        file_scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        file_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        file_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        file_scroll_area.setWidgetResizable(True)

        bottom_frame = QFrame(file_scroll_area)
        bottom_frame.setObjectName('bottom_frame')
        bottom_frame.setFrameShape(QFrame.Shape.NoFrame)
        bottom_frame.setFrameShadow(QFrame.Shadow.Plain)

        dir_entry_frame = QFrame(bottom_frame)
        dir_entry_frame.setObjectName('dir_entry_frame')
        dir_entry_frame.setFrameShape(QFrame.Shape.NoFrame)
        dir_entry_frame.setFrameShadow(QFrame.Shadow.Plain)

        self.settings_dir_entry = QtButtonLineEdit(
            title="Session Settings",
            title_color=self.themes["app_color"]["text_color"],
            color_three=self.themes['app_color']['blue_bg'],
            top_margin=18,
            mode="file",
            parent=dir_entry_frame
        )
        self.settings_dir_entry.setObjectName('settings_dir_entry')
        self.settings_dir_entry.setMaximumWidth(975)

        add_bttn_frame = QFrame(dir_entry_frame)
        add_bttn_frame.setObjectName('add_bttn_frame')
        add_bttn_frame.setFrameShape(QFrame.Shape.NoFrame)
        add_bttn_frame.setFrameShadow(QFrame.Shadow.Plain)

        self.add_file_bttn = PyPushButton(
            text="Add File",
            radius=8,
            color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            font_size=16,
            parent=add_bttn_frame
        )
        self.add_file_bttn.setObjectName("find_settings_bttn")
        self.add_file_bttn.setFixedHeight(40)
        self.add_file_bttn.setFixedWidth(300)

        add_bttn_layout = QVBoxLayout(add_bttn_frame)
        add_bttn_layout.setContentsMargins(50, 5, 50, 5)
        add_bttn_layout.addWidget(self.add_file_bttn, alignment=Qt.AlignmentFlag.AlignCenter)

        dir_entry_layout = QGridLayout(dir_entry_frame)
        dir_entry_layout.setObjectName('dir_entry_layout')
        dir_entry_layout.setContentsMargins(40, 10, 40, 10)
        dir_entry_layout.addWidget(self.settings_dir_entry)
        dir_entry_layout.addWidget(add_bttn_frame)
        dir_entry_frame.setMaximumHeight(dir_entry_layout.sizeHint().height() + 4)

        file_interaction_frame = QFrame(bottom_frame)
        file_interaction_frame.setObjectName('file_interaction_frame')
        file_interaction_frame.setFrameShape(QFrame.Shape.NoFrame)
        file_interaction_frame.setFrameShadow(QFrame.Shadow.Plain)

        self.file_box = QGroupBox(parent=file_interaction_frame)
        self.file_box.setTitle("File Submission")
        self.file_box.setStyleSheet(gb_style)
        self.file_box.hide()

        self.box_container = QFrame(self.file_box)
        self.box_container.setObjectName('box_container')
        self.box_container.setFrameShape(QFrame.Shape.NoFrame)
        self.box_container.setFrameShadow(QFrame.Shadow.Plain)
        self.box_container.setStyleSheet(f"""
            QFrame#box_container{{
                background: {self.themes['app_color']['main_bg']};
                border: none;
                border-radius: 10px;
            }}
        """)

        self.box_layout = QHBoxLayout(self.box_container)
        self.box_layout.setContentsMargins(10, 10, 10, 10)
        self.box_layout.setSpacing(10)
        
        file_control_frame = QFrame(self.file_box)
        file_control_frame.setObjectName("file_control_frame")
        file_control_frame.setFrameShape(QFrame.Shape.NoFrame)
        file_control_frame.setFrameShadow(QFrame.Shadow.Plain)
        file_control_frame.setStyleSheet(f"background: {self.themes['app_color']['text_title']}; border-bottom-right-radius: 8px; border-bottom-left-radius: 8px;")

        #self.output_dir_widget = QtOutputEntry(parent=file_control_frame)
        #self.output_dir_widget.setObjectName('output_dir_widget')
        self.output_dir_entry = QtButtonLineEdit(
            title="Output Directory",
            title_color=self.themes["app_color"]["text_color"],
            color_three=self.themes['app_color']['blue_bg'],
            top_margin=18,
            parent=file_control_frame
        )
        self.output_dir_entry.setObjectName('output_dir_entry')
        self.output_dir_entry.setMinimumWidth(500)

        file_bttn_frame = QFrame(file_control_frame)
        file_bttn_frame.setObjectName("file_bttn_frame")
        file_bttn_frame.setFrameShape(QFrame.Shape.NoFrame)
        file_bttn_frame.setFrameShadow(QFrame.Shadow.Plain)

        self.clear_bttn = PyPushButton(
            text="Clear",
            radius=8,
            color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["red_bg"],
            bg_color_hover=self.themes["app_color"]["red_hover"],
            bg_color_pressed=self.themes["app_color"]["red_pressed"],
            font_size=16,
            parent=file_control_frame
        )
        self.clear_bttn.setObjectName("clear_bttn")
        self.clear_bttn.setFixedSize(65, 38)

        self.run_bttn = PyPushButton(
            text="Run",
            radius=8,
            color=self.themes["app_color"]["text_color"],
            bg_color=self.themes["app_color"]["green_bg"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            font_size=16,
            parent=file_control_frame
        )
        self.run_bttn.setObjectName("run_bttn")
        self.run_bttn.setFixedSize(65, 38)

        file_bttn_layout = QHBoxLayout(file_bttn_frame)
        file_bttn_layout.setContentsMargins(0, 0, 0, 0)
        file_bttn_layout.setSpacing(125)
        file_bttn_layout.addStretch(1)
        file_bttn_layout.addWidget(self.clear_bttn, alignment=Qt.AlignmentFlag.AlignCenter)
        file_bttn_layout.addWidget(self.run_bttn, alignment=Qt.AlignmentFlag.AlignCenter)
        file_bttn_layout.addStretch(1)

        file_control_layout = QVBoxLayout(file_control_frame)
        file_control_layout.setContentsMargins(40, 10, 40, 10)
        file_control_layout.setSpacing(5)
        file_control_layout.addWidget(self.output_dir_entry)
        file_control_layout.addWidget(file_bttn_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        file_control_frame.setFixedHeight(file_control_layout.sizeHint().height() + 10)

        self.file_box_layout = QVBoxLayout(self.file_box)
        self.file_box_layout.setContentsMargins(0, 0, 0, 0)
        self.file_box_layout.addWidget(self.box_container)
        self.file_box_layout.addWidget(file_control_frame)

        file_interaction_layout = QVBoxLayout(file_interaction_frame)
        file_interaction_layout.setContentsMargins(75, 0, 75, 0)
        file_interaction_layout.addWidget(self.file_box)

        bottom_frame_layout = QVBoxLayout(bottom_frame)
        bottom_frame_layout.setContentsMargins(10, 10, 10, 10)
        bottom_frame_layout.addSpacing(25)
        bottom_frame_layout.addWidget(dir_entry_frame)
        bottom_frame_layout.addWidget(file_interaction_frame)

        file_scroll_area.setWidget(bottom_frame)

        container_layout = QGridLayout(container_frame)
        container_layout.setObjectName('container_layout')
        container_layout.setContentsMargins(10, 25, 10, 10)
        container_layout.setSpacing(5)
        container_layout.addWidget(short_description_frame)
        container_layout.addWidget(file_scroll_area)

        main_layout = QVBoxLayout(self)
        main_layout.setObjectName('main_layout')
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container_frame)

    def add_file(self):
        error_bttns = {
            "Ok": QMessageBox.ButtonRole.AcceptRole
        }
        error_msg = QtMessage(
            buttons=error_bttns,
            color=self.themes["app_color"]["main_bg"],
            bg_color_one=self.themes["app_color"]["dark_one"],
            bg_color_two=self.themes["app_color"]["bg_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        error_msg.setIcon(QMessageBox.Icon.Warning)

        input_file = pathlib.Path(self.settings_dir_entry.text())
        if self.is_valid_entry():
            # Create file object
            if input_file.name in self._obj_dict:
                error_msg.setText("File already added.")
                error_msg.setDetailedText("The provided file already exists in the list. Please enter a new, unique JSON file from a previous session.")
                error_msg.exec()
                return
            else:
                if (self._obj_counter + 1) <= 2:
                    self._obj_counter += 1
                    file_obj = QtFileWidget(file=input_file, parent=self.box_container)
                    file_obj.setObjectName(f"file_obj_{self._obj_counter}")
                    self.box_layout.addWidget(file_obj, alignment=Qt.AlignmentFlag.AlignCenter)
                    self._obj_dict[input_file.name] = file_obj
                    file_obj.request_removal.connect(self.remove_file)
                    height = self.file_box_layout.sizeHint().height() + 35
                    if self.file_box.height() != height:
                        self.file_box.setFixedHeight(height)
                    self.settings_dir_entry.clear_text()

                    if self.file_box.isHidden():
                        self.file_box.show()
                else:
                    error_msg.setText("File limit reached.")
                    error_msg.setDetailedText("The maximum amount of files have been added (2). Please remove other files before adding another file.")
                    error_msg.exec()
                    return

    def remove_file(self, file_widget: QWidget):
        file_name = file_widget.get_file_name()
        if file_name in self._obj_dict:
            self._obj_dict.pop(file_name)
            self.box_layout.removeWidget(file_widget)
            file_widget.deleteLater()
            self._obj_counter -= 1
            if self._obj_counter < 1:
                self.file_box.hide()

    def is_valid_entry(self):
        error_bttns = {
            "Ok": QMessageBox.ButtonRole.AcceptRole
        }
        error_msg = QtMessage(
            buttons=error_bttns,
            color=self.themes["app_color"]["main_bg"],
            bg_color_one=self.themes["app_color"]["dark_one"],
            bg_color_two=self.themes["app_color"]["bg_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        error_msg.setIcon(QMessageBox.Icon.Warning)

        input_file = pathlib.Path(self.settings_dir_entry.text())
        # Check that file exists
        if not input_file.exists():
            error_msg.setText("File does not exist.")
            error_msg.setDetailedText("Please select a valid JSON file from a previous session.")
            error_msg.exec()
            return False
        
        # Check that the path is a file
        if not input_file.is_file():
            error_msg.setText("Not a file.")
            error_msg.setDetailedText("Please select a valid JSON file from a previous session.")
            error_msg.exec()
            return False
        
        # Check that the file type is JSON
        if input_file.suffix != ".json":
            error_msg.setText("Invalid file type.")
            error_msg.setDetailedText("Please select a valid JSON file from a previous session.")
            error_msg.exec()
            return False

        return True

    def clear_files(self):
        self._obj_counter = 0
        self._obj_dict = {}
        self.output_dir_entry.clear_text()
        self.file_box.hide()

        for index in range(self.box_layout.count()):
            item = self.box_layout.itemAt(index)
            if item.widget():
                item.widget().deleteLater()

    def submit_files(self):
        error_bttns = {
            "Ok": QMessageBox.ButtonRole.AcceptRole
        }
        error_msg = QtMessage(
            buttons=error_bttns,
            color=self.themes["app_color"]["main_bg"],
            bg_color_one=self.themes["app_color"]["dark_one"],
            bg_color_two=self.themes["app_color"]["bg_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        error_msg.setIcon(QMessageBox.Icon.Warning)

        output_dir = pathlib.Path(self.output_dir_entry.text())

        if self._obj_counter != 2:
            # Check if 2 files are submitted
            error_msg.setText("Please provide two files.")
            error_msg.setDetailedText("VALIS requires two unique JSON settings files, saved from a previous session, to continue.\nNamely, these files are: \"sample.json\" and \"user_settings.json\".")
            error_msg.exec()
            return
        elif "sample.json" not in self._obj_dict.keys():
            # Check for sample settings
            error_msg.setText("Missing \"sample.json\" file.")
            error_msg.setDetailedText("One of the unique settings files is missing. Expected file is \"sample.json\".")
            error_msg.exec()
            return
        elif "user_settings.json" not in self._obj_dict.keys():
            # Check for user settings
            error_msg.setText("Missing \"user_settings.json\" file.")
            error_msg.setDetailedText("One of the unique settings files is missing. Expected file is \"user_settings.json\".")
            error_msg.exec()
            return
        elif self.output_dir_entry.text() == "":
            # Check for empty entry
            error_msg.setText("Please provide an output directory.")
            error_msg.setDetailedText("Please select a valid output directory for the VALIS output files.")
            error_msg.exec()
            return
        elif not output_dir.exists():
            # Check if output directory exists
            error_msg.setText("Invalid output directory.")
            error_msg.setDetailedText("The specified output directory does not exist.")
            error_msg.exec()
            return
        elif not output_dir.is_dir():
            # Check if output directory is a directory
            error_msg.setText("Invalid output directory.")
            error_msg.setDetailedText("The specified output directory is not a directory.")
            error_msg.exec()
            return
        else:
            self._obj_dict["dst_dir"] = output_dir
            self.emit_dict.emit(self._obj_dict)


