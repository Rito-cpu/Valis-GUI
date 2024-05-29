import os

from datetime import datetime
from src.core.pyqt_core import *
from src.core.app_config import *
from src.core.json.json_themes import Themes
from src.core.validation.validate_file import is_json_file, is_excel_file
from src.core.scripts.valis.gui_options import *
from src.core.scripts.valis.command_line import start_valis_process
from src.gui.views.windows.ui_main_window import UI_MainWindow
from src.gui.models import *


class MainFunctions():
    def __init__(self) -> None:
        super().__init__()
        # Setup Main Window
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        themes = Themes
        self.themes = themes.items

    # SET MAIN WINDOW PAGES
    def set_page(self, page):
        self.ui.load_pages.pages.setCurrentWidget(page)

    # SET LEFT COLUMN PAGES
    def set_left_column_menu(
        self,
        menu,
        title,
        icon_path
    ):
        self.ui.left_column.menus.menus.setCurrentWidget(menu)
        self.ui.left_column.title_label.setText(title)
        self.ui.left_column.icon.set_icon(icon_path)

    # RETURN IF LEFT COLUMN IS VISIBLE
    def left_column_is_visible(self):
        width = self.ui.left_column_frame.width()
        if width == 0:
            return False
        else:
            return True

    # RETURN IF RIGHT COLUMN IS VISIBLE
    def right_column_is_visible(self):
        width = self.ui.right_column_frame.width()
        if width == 0:
            return False
        else:
            return True

    # SET RIGHT COLUMN PAGES
    def set_right_column_menu(self, menu):
        self.ui.right_column.menus.setCurrentWidget(menu)

    # GET TITLE BUTTON BY OBJECT NAME
    def get_title_bar_btn(self, object_name):
        return self.ui.title_bar_frame.findChild(QPushButton, object_name)

    # GET TITLE BUTTON BY OBJECT NAME
    def get_left_menu_btn(self, object_name):
        return self.ui.left_menu.findChild(QPushButton, object_name)

    # LEFT AND RIGHT COLUMNS / SHOW / HIDE
    def toggle_left_column(self):
        # GET ACTUAL CLUMNS SIZE
        width = self.ui.left_column_frame.width()
        right_column_width = self.ui.right_column_frame.width()

        MainFunctions.start_box_animation(self, width, right_column_width, "left")

    def toggle_right_column(self):
        # GET ACTUAL CLUMNS SIZE
        width = self.ui.right_column_frame.width()
        left_column_width = self.ui.left_column_frame.width()

        MainFunctions.start_box_animation(self, left_column_width, width, "right")

    def start_box_animation(self, left_box_width, right_box_width, direction):
        right_width = 0
        left_width = 0
        time_animation = self.ui.settings["time_animation"]
        minimum_left = self.ui.settings["left_column_size"]["minimum"]
        maximum_left = self.ui.settings["left_column_size"]["maximum"]
        minimum_right = self.ui.settings["right_column_size"]["minimum"]
        maximum_right = self.ui.settings["right_column_size"]["maximum"]

        # Check Left Values
        if left_box_width == minimum_left and direction == "left":
            left_width = maximum_left
        else:
            left_width = minimum_left

        # Check Right values
        if right_box_width == minimum_right and direction == "right":
            right_width = maximum_right
        else:
            right_width = minimum_right

        # ANIMATION LEFT BOX
        self.left_box = QPropertyAnimation(self.ui.left_column_frame, b"minimumWidth")
        self.left_box.setDuration(time_animation)
        self.left_box.setStartValue(left_box_width)
        self.left_box.setEndValue(left_width)
        self.left_box.setEasingCurve(QEasingCurve.Type.InOutQuart)

        # ANIMATION RIGHT BOX
        self.right_box = QPropertyAnimation(self.ui.right_column_frame, b"minimumWidth")
        self.right_box.setDuration(time_animation)
        self.right_box.setStartValue(right_box_width)
        self.right_box.setEndValue(right_width)
        self.right_box.setEasingCurve(QEasingCurve.Type.InOutQuart)

        # GROUP ANIMATION
        self.group = QParallelAnimationGroup()
        self.group.stop()
        self.group.addAnimation(self.left_box)
        self.group.addAnimation(self.right_box)
        self.group.start()

    def convert_date_format(self, date: str):
        date_obj = datetime.strptime(date, "%Y-%m-%d")

        formatted_date = datetime.strftime("%m/%d/%Y")

        return formatted_date

    def launch_context_window(self):
        bttn_list = {
            'Ok': QMessageBox.ButtonRole.AcceptRole
        }

        context_file_msg = QtMessage(
            buttons=bttn_list,
            color=self.themes["app_color"]["main_bg"],
            bg_color_one=self.themes["app_color"]["dark_one"],
            bg_color_two=self.themes["app_color"]["bg_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
        )

        #immuno_widget = self.ui.load_pages.immuno_dir_interaction.findChild(QtImmunoWidget, 'immuno_entry')
        if UPLOAD_STATE == INCOMPLETE:#if not immuno_widget.is_valid_data() or UPLOAD_STATE == INCOMPLETE:
            context_file_msg.setText('No slide image files have been submitted.')
            context_file_msg.setDetailedText('Please upload slide image file(s) to proceed.')
            context_file_msg.exec()
        elif UPLOAD_STATE == COMPLETE:#elif immuno_widget.is_valid_data() and UPLOAD_STATE == COMPLETE:
            data = UPLOADED_DATA
            slide_dirs = data['slide_dirs']

            parent_portion = """
                <html>
                    <body>
                        <p><b>Parent Directory:</b></p>
                        <p>%s</p>
                        <br></br>
                    </body>
                </html>
            """ % data['parent_dir']

            child_portion = """
                <html>
                    <body>
                        <p><b>Slide Sub-Directories:</b></p>
                    </body>
                </html>
            """

            child_list = ''
            for name in slide_dirs:
                if name == slide_dirs[0]:
                    child_list += name
                else:
                    child_list += '\n%s' % name

            context_file_msg.setText('Submitted Slide Image Data')
            context_file_msg.setInformativeText(parent_portion + child_portion)
            context_file_msg.setDetailedText(child_list)
            context_file_msg.exec()

    def check_project_directory(self, directory: str, label: QtMarqueeLabel):
        if os.path.isdir(directory):
            global PROJECT_DIRECTORY
            PROJECT_DIRECTORY = directory

            label.setText(directory)

    def show_non_rigid(self, setting: QWidget, show):
        if show:
            setting.show()
        else:
            setting.hide()

    def register_settings(
            self,
            process_setting: QWidget,
            rigid_setting: QWidget,
            non_rigid_setting: QWidget,
            empty_immuno: bool
    ):
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

        global UPLOAD_STATE, REGISTRATION_STATE, REGISTRATION_SETTINGS
        if UPLOAD_STATE == INCOMPLETE:  # if empty_immuno:
            # No directory or slides were provided
            error_msg.setText("Missing Upload Process!")
            error_msg.setDetailedText(
                "The upload process in the Slide Directory menu is not complete." +
                "\nThere are no found submitted slide sub-directories to use settings on." +
                "\nPlease go back and upload slide sub-directories to apply registration settings."
            )
            error_msg.exec()
            return
        else:
            # Slides were provided, proceed to switch menu and run valis
            if self.ui.left_menu._menu_list is not None:
                obj: QPushButton
                for obj in self.ui.left_menu._menu_list:
                    if obj.objectName() == 'results_bttn':
                        obj.click()
                        self.results_page_picker(self.ui.load_pages.result_page)

            processing_data = process_setting.get_data()
            rigid_data = rigid_setting.get_data()
            non_rigid_data = non_rigid_setting.get_data()

            print(f'Processing Data: \n{processing_data}\n')
            print(f'Rigid Data: \n{rigid_data}\n')
            print(f'Non-Rigid Data: \n{non_rigid_data}\n')

            data_dict = {
                'processing_settings': processing_data,
                'rigid_settings': rigid_data,
                'non_rigid_settings': non_rigid_data
            }
            REGISTRATION_SETTINGS = data_dict
            start_valis_process(data_dict)

            REGISTRATION_STATE = COMPLETE

    def upload_slides(self, immuno_setting: QtImmunoWidget):
        global PROJECT_DIRECTORY, UPLOAD_STATE, UPLOADED_DATA
        print(f'Project Working Directory: {PROJECT_DIRECTORY}')

        # Prepare message box for user errors
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

        if immuno_setting.is_empty():
            # Empty data entered, fire msg box
            error_msg.setText("Empty parameters were submitted.")
            error_msg.setDetailedText(
                "Please provide a valid parent directory of slide image directories " +
                "in the file path and make selections accordingly using the toggle buttons."
            )
            error_msg.exec()
            return
        elif not immuno_setting.is_valid_path():
            # Invalid or non-existent file path provided
            error_msg.setText("Invalid file path submitted.")
            error_msg.setDetailedText(
                "Please ensure that the file path provided in the text entry is a valid path " +
                "and exists within your file system."
            )
            error_msg.exec()
            return
        elif immuno_setting.has_all_toggled():
            error_msg.setText("No sub-directories were chosen.")
            error_msg.setDetailedText(
                "All the sub-directory toggle buttons are unchecked in the \'Directory Contents\' widget. " +
                "\nValis requires slide images, so please ensure that at least one (1) sub-directory toggle button is checked."
            )
            error_msg.exec()
            return

        if self.ui.left_menu._menu_list is not None:
            obj: QPushButton
            for obj in self.ui.left_menu._menu_list:
                if obj.objectName() == 'registration_bttn':
                    obj.click()
                    self.registration_page_picker(self.ui.load_pages.registration_settings_subpage)

        data_dict = immuno_setting.get_data()
        UPLOADED_DATA = data_dict

        UPLOAD_STATE = COMPLETE
        # print(data)

    def close_instance(self):
        self.close_window(use_box=False)

    def export_data(self):
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

        global REGISTRATION_STATE
        if REGISTRATION_STATE == INCOMPLETE:
            error_msg.setText("Registration settings are incomplete.")
            error_msg.setDetailedText(
                "Registration Settings Menu is incomplete (data has not be submitted)." +
                "\nPlease go back to the Registration Settings Menu and submit the parameters."
            )
            error_msg.exec()
            return

        if self.ui.left_menu._menu_list is not None:
            obj: QPushButton
            for obj in self.ui.left_menu._menu_list:
                if obj.objectName() == 'results_bttn':
                    obj.click()
                    self.bookmark_second_half(self.ui.load_pages.export_page)

    def export_clicked(self, show_prog_bar, show_button):
        show_prog_bar()
        show_button()

    def cancel_export(self, hide_prog_bar, hide_button):
        hide_prog_bar()
        hide_button()
