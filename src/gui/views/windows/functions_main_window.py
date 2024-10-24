import json
import shutil
import pathlib
import subprocess

from datetime import datetime
from src.core.pyqt_core import *
from src.core.app_config import *
from src.core.json.json_themes import Themes
from src.core.validation.validate_file import is_json_file, is_excel_file, is_existing_dir
from src.core.scripts.valis.gui_options import *
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

    def set_project_directory(self, output_widget: QWidget):
        """Establishes a user provided directory as a project directory for application use.

        Args:
            directory (str): user defined directory path 
            label (QtMarqueeLabel): custom QWidget that displays a scrolling text
        """
        directory = pathlib.Path(output_widget.get_text())
        if is_existing_dir(directory):
            global OUTPUT_DIRECTORY
            OUTPUT_DIRECTORY = str(directory)

            output_widget.set_text(str(directory))
        else:
            OUTPUT_DIRECTORY = None

    def check_project_directory(self):
        if OUTPUT_DIRECTORY:
            return True
        else:
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
            error_msg.setText('No set project directory.')
            error_msg.setDetailedText('A project directory has not yet been configured and is needed for the next step. Please submit a valid project directory in the home page.')
            error_msg.exec()

            return False

    def clear_pressed(self):
        global SUBMITTED_SLIDES, SAMPLE_UPLOAD_STATE
        SUBMITTED_SLIDES = None
        SAMPLE_UPLOAD_STATE = INCOMPLETE

    def jump_to_results(self):
        """Function that brings the user to a new page upon valis registration initiation.
        """
        # self.v_bar.my_thread.terminate()

        if self.ui.left_menu._menu_list is not None:
                obj: QPushButton
                for obj in self.ui.left_menu._menu_list:
                    if obj.objectName() == 'results_bttn':
                        obj.click()
                        self.results_page_picker(self.ui.load_pages.result_page)

    def register_settings(
            self,
            output_dir_widget: QWidget,
            if_settings: QWidget,
            bf_settings: QWidget,
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

        global SAMPLE_UPLOAD_STATE, REGISTRATION_STATE, SUBMITTED_SLIDES, OUTPUT_DIRECTORY
        # Check if image slide upload stage has been completed
        if SAMPLE_UPLOAD_STATE == INCOMPLETE:
            error_msg.setText("Missing Sample Upload!")
            error_msg.setDetailedText(
                "The sample upload is incomplete: no uploaded samples were found." +
                "\nPlease go back and upload samples to apply registration settings."
            )
            error_msg.exec()
            return
        else:
            # Check for invalid project directory submission
            if not OUTPUT_DIRECTORY:
                error_msg.setText('No Output Directory!')
                error_msg.setDetailedText(
                    'A output directory has not yet been configured and is needed for the next step.' +
                    'Please submit a valid output directory to store results.'
                )
                error_msg.exec()
                return
            
            output_dir_widget.submit_bttn_clicked()
            # Gather widget states for registration
            if_data = if_settings.get_widget_settings()
            bf_data = bf_settings.get_widget_settings()
            rigid_data = rigid_setting.get_data()
            non_rigid_data = non_rigid_setting.get_data()

            # Package user settings from registration
            user_settings = {
                SRC_DIR: '',
                DST_DIR: OUTPUT_DIRECTORY,
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
                MAX_NON_RIGID_REGISTRATION_DIM_PX: 1024,
                THUMBNAIL_SIZE: 500,
                NORM_METHOD: "img_stats",
                MICRO_RIGID_REGISTRAR_PARAMS: None,
                QT_EMITTER: None,
                IF_PROCESSOR: if_data,
                BF_PROCESSOR: bf_data
            }
            user_settings.update(rigid_data)
            user_settings.update(non_rigid_data)

            if OUTPUT_DIRECTORY is not None:
                # Create session settings folder in user output directory
                try:
                    session_settings_dir = pathlib.Path(OUTPUT_DIRECTORY) / "session_settings"
                    session_settings_dir.mkdir(exist_ok=True)
                    
                    json_user_settings = json.dumps({'user_selections': user_settings}, indent=2)
                    local_user_settings = (APP_ROOT / "src" / "core"/ "output" / "states" / "user_settings.json").resolve()
                    with open(local_user_settings, 'w') as outfile:
                        outfile.write(json_user_settings)
                    shutil.copyfile(local_user_settings, session_settings_dir / local_user_settings.name)

                    slides_dict = SUBMITTED_SLIDES
                    json_slides_settings = json.dumps(slides_dict, indent=2)
                    local_slide_settings = (APP_ROOT / "src" / "core" / "output" / "states" / "sample.json").resolve()
                    with open(local_slide_settings, 'w') as outfile:
                        outfile.write(json_slides_settings)
                    shutil.copyfile(local_slide_settings, session_settings_dir / local_slide_settings.name)
                except FileExistsError as file_error:
                    error_msg.setText('File Already Exists!')
                    error_msg.setDetailedText(f'An error occurred while trying to create a file/folder: \n{str(e)}')
                    error_msg.exec()
                    return
                except OSError as os_error:
                    error_msg.setText('Received OS Error!')
                    error_msg.setDetailedText(f'An error occurred while handling files: \n{str(os_error)}')
                    error_msg.exec()
                    return
                except Exception as exception:
                    error_msg.setText('Encountered Error!')
                    error_msg.setDetailedText(f'An error occurred while trying to register settings: \n{str(exception)}')
                    error_msg.exec()
                    return

                results_area = self.ui.load_pages.results_scroll_content.findChild(QtResultsArea, "results_area")
                # Create valis-wsi QProcess thread
                try:
                    self.valis_process = ValisProcessObject()
                    successful_startup = self.valis_process.start_process()
                    if not successful_startup:
                        return
                    MainFunctions.jump_to_results(self)
                    self.valis_process.finished.connect(lambda: MainFunctions.valis_completed(self))

                    results_area.cancel_valis_bttn.clicked.connect(self.valis_process.kill)
                    results_area.cancel_valis_bttn.setEnabled(True)
                except Exception as e:
                    self.valis_process.kill()
                    error_msg.setText('Error occurred during registration process.')
                    error_msg.setDetailedText(f'An error occurred while trying to register settings: {str(e)}')
                    error_msg.exec()
                    return

                # Create monitoring script QThread
                try:
                    results_area.prepare_menu()
                    results_area.create_thread()
                except Exception as e:
                    self.valis_process.kill()
                    # TODO: Process is not killed if error thrown
                    if results_area._monitoring_thread:
                        results_area._monitoring_thread.terminate()
                    error_msg.setText('Error occurred during registration process (within progress bar thread).')
                    error_msg.setDetailedText(f'An error occurred while trying to create the Valis thread: {str(e)}')
                    error_msg.exec()
                    return
            else:
                error_msg.setIcon(QMessageBox.Icon.Information)
                error_msg.setText('No home directory found.')
                error_msg.setDetailedText('The home directory path has not been set. To continue, please configure a home directory.')
                error_msg.exec()
            REGISTRATION_STATE = COMPLETE

    def upload_slides(self, slide_dir_widget: QtSlideDirectory):
        """Validation checking for user provided images to be uploaded and processed in valis registration.

        Args:
            slide_dir_widget (QtSlideDirectory): custom widget that contains user interactive widgets to enable slide image uploading.
        """
        global OUTPUT_DIRECTORY, SAMPLE_UPLOAD_STATE, SUBMITTED_SLIDES
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

        if not slide_dir_widget.is_valid_path():
            # Invalid or non-existent file path provided
            error_msg.setText("Invalid File Path.")
            error_msg.setDetailedText(
                "Please ensure that the file path provided in the text entry is a valid path " +
                "and exists within your file system."
            )
            error_msg.exec()
            return
        elif slide_dir_widget.check_empty_tree():
            error_msg.setText("File Tree Incomplete.")
            error_msg.setDetailedText(
                "Please ensure that the file tree is populated with the desired images to be registered."
            )
            error_msg.exec()
            return
        elif slide_dir_widget.all_toggle_deactivated():
            error_msg.setText("No Selected Files.")
            error_msg.setDetailedText(
                "All files within the tree have been toggled to not be included. Please include at least one file."
            )
            error_msg.exec()
            return

        if self.ui.left_menu._menu_list is not None:
            obj: QPushButton
            for obj in self.ui.left_menu._menu_list:
                if obj.objectName() == 'registration_bttn':
                    obj.click()
                    self.registration_page_picker(self.ui.load_pages.registration_settings_subpage)

        slide_dict = slide_dir_widget.get_data()
        SUBMITTED_SLIDES = slide_dict

        SAMPLE_UPLOAD_STATE = COMPLETE

    def valis_completed(self):
        results_area = self.ui.load_pages.results_scroll_content.findChild(QtResultsArea, "results_area")

        if not self.valis_process.process_killed:
            results_area.cancel_valis_bttn.clicked.disconnect(self.valis_process.kill)
            #if results_area._monitoring_thread:
                #results_area._monitoring_thread.terminate()
            print(f'Cleaned up!')
        else:
            results_area.process_terminated()
            print(f'Canceled!')
        self.valis_process = None
        results_area.cancel_valis_bttn.setEnabled(False)

    def move_to_export_menu(self):
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
            error_msg.setText("Registration Incomplete!")
            error_msg.setDetailedText(
                "The Registration Settings have not been submitted." +
                "\nPlease go back to the Registration Settings menu and submit the parameters."
            )
            error_msg.exec()
            return

        if self.ui.left_menu._menu_list is not None:
            obj: QPushButton
            for obj in self.ui.left_menu._menu_list:
                if obj.objectName() == 'results_bttn':
                    obj.click()
                    self.results_page_picker(self.ui.load_pages.export_page)

    def export_clicked(self, show_prog_bar, show_button):
        show_prog_bar()
        show_button()

    def cancel_export(self, hide_prog_bar, hide_button):
        hide_prog_bar()
        hide_button()
