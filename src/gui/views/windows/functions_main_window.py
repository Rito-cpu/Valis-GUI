import json

from datetime import datetime
from src.core.pyqt_core import *
from src.core.app_config import *
from src.core.keyword_store import *
from src.core.json.json_themes import Themes
from src.core.validation.validate_file import is_json_file, is_excel_file, is_existing_dir
from src.core.scripts.valis.gui_options import *
from src.core.scripts.valis.valis_command import ValisWorker
from src.gui.views.windows.ui_main_window import UI_MainWindow
from src.gui.models import *


class MainFunctions():
    """Utility class that provides functions and logic for the MainWindow and its pages.
    """
    def __init__(self) -> None:
        super().__init__()
        # Setup Main Window
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        themes = Themes
        self.themes = themes.items

    def set_page(self, page):
        """Sets the current page in the MainWindow.

        Args:
            page (QWidget): The QWidget to be set as the current page.
        """
        self.ui.load_pages.pages.setCurrentWidget(page)

    def set_left_column_menu(
        self,
        menu,
        title,
        icon_path
    ):
        """Toggles the additional left column menu to be shown/hidden.

        Args:
            menu (QWidget): QWidget page to be set in the additional left column menu.
            title (str): descriptive title for the left column type.
            icon_path (str): path to image directory in project files.
        """
        self.ui.left_column.menus.menus.setCurrentWidget(menu)
        self.ui.left_column.title_label.setText(title)
        self.ui.left_column.icon.set_icon(icon_path)

    def left_column_is_visible(self):
        """Determines if left column is expanded.

        Returns:
            bool: Tells us the state of the left column's visibility.
        """
        width = self.ui.left_column_frame.width()
        if width == 0:
            return False
        else:
            return True

    def right_column_is_visible(self):
        """Determines if right column is expanded.

        Returns:
            bool: Tells us the state of the right columns visibility.
        """
        width = self.ui.right_column_frame.width()
        if width == 0:
            return False
        else:
            return True

    def set_right_column_menu(self, menu):
        """Displays a specified menu widget in the right column.

        Args:
            menu (QWidget): custom menu widget to be displayed.
        """
        self.ui.right_column.menus.setCurrentWidget(menu)

    def get_title_bar_btn(self, object_name):
        """Retrieves a QPushButton from the title bar by using its object name.

        Args:
            object_name (str): The object name of a specific QPushButton instance in the title bar.

        Returns:
            QPushButton: The found button in the title bar.
        """
        return self.ui.title_bar_frame.findChild(QPushButton, object_name)

    def get_left_menu_btn(self, object_name):
        """Retrieves a QPushButton from the left menu by using its object name.

        Args:
            object_name (str): The object name of a specific QPushButton instance in the left menu.

        Returns:
            QPushButton: The found QPushButton instance within the left menu.
        """
        return self.ui.left_menu.findChild(QPushButton, object_name)

    def toggle_left_column(self):
        """Hide or show left side column with it's according width relative to right column width.
        """
        width = self.ui.left_column_frame.width()
        right_column_width = self.ui.right_column_frame.width()

        MainFunctions.start_box_animation(self, width, right_column_width, "left")

    def toggle_right_column(self):
        """Hide or show right side column with it's according width relative to left column width.
        """
        width = self.ui.right_column_frame.width()
        left_column_width = self.ui.left_column_frame.width()

        MainFunctions.start_box_animation(self, left_column_width, width, "right")

    def start_box_animation(self, left_box_width, right_box_width, direction):
        """Initiates the collapse/expand animation for the columns.

        Args:
            left_box_width (int): integer value of the left side column width
            right_box_width (int): integer value of the right side column width
            direction (str): a predefined string allocating the animation direction
        """
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

    def launch_context_window(self):
        """Subwindow that displays the user provided slide directory and the contents that were selected for processing.
        """
        msg_bttns = {
            'Ok': QMessageBox.ButtonRole.AcceptRole
        }

        context_file_msg = QtMessage(
            buttons=msg_bttns,
            color=self.themes["app_color"]["main_bg"],
            bg_color_one=self.themes["app_color"]["dark_one"],
            bg_color_two=self.themes["app_color"]["bg_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
        )

        if UPLOAD_STATE == INCOMPLETE:
            context_file_msg.setText('No slide image files have been submitted.')
            context_file_msg.setDetailedText('Please upload slide image file(s) to proceed.')
            context_file_msg.exec()
        elif UPLOAD_STATE == COMPLETE:
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
        """Establishes a user provided directory as a project directory for application use.

        Args:
            directory (str): user defined directory path 
            label (QtMarqueeLabel): custom QWidget that displays a scrolling text
        """
        if is_existing_dir(directory):
            global PROJECT_DIRECTORY
            PROJECT_DIRECTORY = directory

            label.setText(directory)

    def on_thread_finished(self):
        """Slot function for QThread completion signal that brings the user to a new page upon valis registration completion.
        """
        # TODO: Needs to be set so that user can switch pages while valis is processing so they can view images
        if self.ui.left_menu._menu_list is not None:
                obj: QPushButton
                for obj in self.ui.left_menu._menu_list:
                    if obj.objectName() == 'results_bttn':
                        obj.click()
                        self.results_page_picker(self.ui.load_pages.result_page)

    def register_settings(
            self,
            bf_settings: QWidget,
            if_settings: QWidget,
            rigid_setting: QWidget,
            non_rigid_setting: QWidget,
    ):
        """Gathers the state of the widgets contained in the settings menu for valis registration.

        Args:
            process_setting (QWidget): container widget that provides process type settings for registration
            rigid_setting (QWidget): container widget that provides rigid registration settings
            non_rigid_setting (QWidget): container widget that provides non-rigid registration settings
        """
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

        global UPLOAD_STATE, REGISTRATION_STATE
        
        # Check if image slide upload stage has been completed
        if UPLOAD_STATE == INCOMPLETE:
            error_msg.setText("Missing Upload Process!")
            error_msg.setDetailedText(
                "The upload process in the Slide Directory menu is not complete." +
                "\nThere are no found submitted slide sub-directories to use settings on." +
                "\nPlease go back and upload slide sub-directories to apply registration settings."
            )
            error_msg.exec()
            return
        else:
            docker_path = QFileDialog.getExistingDirectory(self, 'Select Docker Project Directory')
            if docker_path == '':
                # Catch cancel button event to not trigger an error message
                return
            elif not docker_path or not is_existing_dir(docker_path):
                error_msg.setText("Invalid Docker path.")
                error_msg.setDetailedText("The path to the required valis docker container returned invalid.")
                error_msg.exec()
                return
            # processing_data = process_setting.get_data()
            if_data = if_settings.get_widget_settings()
            bf_data = bf_settings.get_widget_settings()
            rigid_data = rigid_setting.get_data()
            non_rigid_data = non_rigid_setting.get_data()

            data_dict = {
                SRC_DIR: '',
                DST_DIR: PROJECT_DIRECTORY,
                SERIES: None,
                NAME: None,
                IMAGE_TYPE: None,
                IMGS_ORDERED: True,
                NON_RIGID_REG_PARAMS: None,
                COMPOSE_NON_RIGID: False,
                IMG_LIST: None,
                REFERENCE_IMG_F: None,
                ALIGN_TO_REFERENCE: False,
                DO_RIGID: True,
                CROP: None,
                CREATE_MASKS: True,
                DENOISE_RIGID: False,
                RESOLUTION_XYU: None,
                SLIDE_DIMS_DICT_WH: None,
                MAX_IMAGE_DIM_PX: 1024,
                MAX_PROCESSED_IMAGE_DIM_PX: 1024,
                MAX_NON_RIGID_REGISTRAR_DIM_PX: 1024,
                THUMBNAIL_SIZE: 500,
                NORM_METHOD: "img_stats",
                MICRO_RIGID_REGISTRAR_PARAMS: None,
                QT_EMITTER: None,
                IF_PROCESSOR: if_data,
                BF_PROCESSOR: bf_data,
            }
            data_dict.update(rigid_data)
            data_dict.update(non_rigid_data)

            json_obj = json.dumps({'user_selections': data_dict}, indent=2)
            file_path = '/Users/4474613/Documents/user_settings.json'
            with open(file_path, 'w') as outfile:
                outfile.write(json_obj)

            #self.valis_worker = ValisWorker()
            #self.valis_worker.begin_process(docker_path, data_dict)
            #self.valis_worker.finished.connect(lambda: MainFunctions.on_thread_finished(self))

            REGISTRATION_STATE = COMPLETE

    def upload_slides(self, immuno_setting: QtImmunoWidget):
        """Validation checking for user provided images to be uploaded and processed in valis registration.

        Args:
            immuno_setting (QtImmunoWidget): custom widget that contains user interactive widgets to enable slide image uploading.
        """
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

    def export_data(self):
        """Handles the submit button on the export page to check if previous page has been completed and process further instructions for exporting
        """
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
