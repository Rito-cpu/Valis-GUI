from src.core.pyqt_core import *
from src.core.json.json_settings import Settings
from src.core.json.json_themes import Themes
from src.gui.views.windows.ui_main_window import *
from src.gui.views.windows.setup_main_window import *
from src.gui.models import *


class MainWindow(QMainWindow):
    """Main Window widget that will contain all other child widgets.

    Args:
        QMainWindow (QWidget): _description_
    Attributes:
        first_two_pages (QWidget): a holder variable that keeps track of which pages (first two pages of system, 1-2) are in use.
        second_two_pages (QWidget): a holder variable that keeps track of which pages  (second two pages, 3-4) are in use.
    """
    first_two_pages = None
    second_two_pages = None

    def __init__(self) -> None:
        super().__init__()

        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        settings = Settings()
        self.settings = settings.items

        self.hide_grips = True
        SetupMainWindow.setup_gui(self)

        themes = Themes()
        self.themes = themes.items

        self.show()

    def menu_clicked(self, menu_bttn):
        """Handles button click events from the left menu and title menu.

        Args:
            menu_bttn (PyPushButton): custom QPushButton object
        """
        # Remove Selection If Clicked By "btn_close_left_column"
        if menu_bttn.objectName() != "bttn_settings":
            self.ui.left_menu.deselect_all_tab()

        # Deactive title bar settings by default
        top_settings = MainFunctions.get_title_bar_btn(self, "bttn_top_settings")
        top_settings.set_active(False)

        # Left Menu Buttons
        if menu_bttn.objectName() == "bttn_home":
            # Right panel must not show in the home page
            if MainFunctions.right_column_is_visible(self):
                menu_bttn.set_active(False)
                MainFunctions.toggle_right_column(self)
            top_settings.setDisabled(True)
            self.ui.left_menu.select_only_one(menu_bttn.objectName())
            # Load first page
            MainFunctions.set_page(self, self.ui.load_pages.home_menu_container)
        elif menu_bttn.objectName() == "registration_bttn":
            self.ui.left_menu.select_only_one(menu_bttn.objectName())
            top_settings.setEnabled(True)
            # Load second page
            if self.first_two_pages is None:
                MainFunctions.set_page(self, self.ui.load_pages.image_dir_subpage)
            else:
                MainFunctions.set_page(self, self.first_two_pages)
            MainFunctions.set_right_column_menu(self, self.ui.right_column.slide_settings_column)
        elif menu_bttn.objectName() == "results_bttn":
            self.ui.left_menu.select_only_one(menu_bttn.objectName())
            top_settings.setEnabled(True)
            # Load third page
            if self.second_two_pages is None:
                MainFunctions.set_page(self, self.ui.load_pages.result_page)
            else:
                MainFunctions.set_page(self, self.second_two_pages)
            MainFunctions.set_right_column_menu(self, self.ui.right_column.results_right_column)
        elif menu_bttn.objectName() == "bttn_info":
            # Ensure that left column is visible
            if not MainFunctions.left_column_is_visible(self):
                self.ui.left_menu.select_only_one_tab(menu_bttn.objectName())
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(menu_bttn.objectName())
            else:
                if menu_bttn.objectName() == "bttn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(menu_bttn.objectName())

            if menu_bttn.objectName() != "bttn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self,
                    menu = self.ui.left_column.menus.info_menu,
                    title = "Info tab",
                    icon_path = Functions.set_svg_icon("icon_info.svg")
                )
        elif menu_bttn.objectName() == "bttn_settings" or menu_bttn.objectName() == "bttn_close_left_column":
            if not MainFunctions.left_column_is_visible(self):
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(menu_bttn.objectName())
            else:
                if menu_bttn.objectName() == "bttn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(menu_bttn.objectName())

            if menu_bttn.objectName() != "bttn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self,
                    menu = self.ui.left_column.menus.settings_menu,
                    title = "Settings Left Column",
                    icon_path = Functions.set_svg_icon("icon_settings.svg")
                )

        # Title Bar Button(s)
        if menu_bttn.objectName() == "bttn_top_settings":
            if not MainFunctions.right_column_is_visible(self):
                menu_bttn.set_active(True)
                MainFunctions.toggle_right_column(self)
            else:
                menu_bttn.set_active(False)
                MainFunctions.toggle_right_column(self)

    def menu_released(self, menu_bttn):
        """Handles button release events from the left menu and title menu.

        Args:
            menu_bttn (PyPushButton): custom QPushButton widget.
        """
        pass
        # menu_bttn = SetupMainWindow.setup_btns(self)
        # print(f"Button {menu_bttn.objectName()}, released!")

    def registration_page_picker(self, page):
        """Keeps track of which page is in use between the import page and the registration page.

        Args:
            page (QWidget): custom QWidget container with interactive child widgets.
        """
        MainFunctions.set_page(self, page)

        sample_menu_bttn = self.ui.right_column.slide_navigation_bttn_frame.findChild(PyPushButton, 'sample_menu_bttn')
        registration_menu_bttn = self.ui.right_column.slide_navigation_bttn_frame.findChild(PyPushButton, 'registration_menu_bttn')
        if page == self.ui.load_pages.image_dir_subpage:
            sample_menu_bttn.set_highlight()
            registration_menu_bttn.remove_highlight()
        elif page == self.ui.load_pages.registration_settings_subpage:
            sample_menu_bttn.remove_highlight()
            registration_menu_bttn.set_highlight()

        self.first_two_pages = page

    def results_page_picker(self, page):
        """Keeps track of which page is in use between the results page and the export page.

        Args:
            page (QWidget): custom QWidget container with interactive child widgets.
        """
        MainFunctions.set_page(self, page)

        results_menu_bttn = self.ui.right_column.results_button_frame.findChild(PyPushButton, 'results_menu_bttn')
        export_menu_bttn = self.ui.right_column.results_button_frame.findChild(PyPushButton, 'export_menu_bttn')
        if page == self.ui.load_pages.result_page:
            results_menu_bttn.set_highlight()
            export_menu_bttn.remove_highlight()
        elif page == self.ui.load_pages.export_page:
            results_menu_bttn.remove_highlight()
            export_menu_bttn.set_highlight()

        self.second_two_pages = page

    def resizeEvent(self, event):
        SetupMainWindow.resize_grips(self)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()

    def closeEvent(self, event) -> None:
        """Custom close event that triggers a messagebox for confirmation.

        Args:
            event (QCloseEvent): event triggered when closing an application in PyQt6.
        """
        exit_buttons = {
            "Yes": QMessageBox.ButtonRole.YesRole,
            "No": QMessageBox.ButtonRole.NoRole
        }

        exit_message_box = QtMessage(
            buttons=exit_buttons,
            color=self.themes["app_color"]["main_bg"],
            bg_color_one=self.themes["app_color"]["dark_one"],
            bg_color_two=self.themes["app_color"]["bg_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        exit_message_box.setIcon(QMessageBox.Icon.Warning)
        exit_message_box.setText("Exit Application?")
        exit_message_box.setInformativeText("All unsaved work will be lost.")
        exit_message_box.exec()

        if exit_message_box.clickedButton() == exit_message_box.buttons["Yes"]:
            QApplication.instance().closeAllWindows()
            event.accept()
        else:
            # Ignoring event resumes application use
            event.ignore()
