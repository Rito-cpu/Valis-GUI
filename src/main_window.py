from src.core.pyqt_core import *
from src.core.json.json_settings import Settings
from src.core.json.json_themes import Themes
from src.gui.views.windows.ui_main_window import *
from src.gui.views.windows.setup_main_window import *
from src.gui.models import *


class MainWindow(QMainWindow):
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

    # LEFT MENU BTN IS CLICKED
    # Check funtion by object name / btn_id
    def menu_clicked(self, menu_bttn):
        # GET BTTN CLICKED

        # Remove Selection If Clicked By "btn_close_left_column"
        if menu_bttn.objectName() != "bttn_settings":
            self.ui.left_menu.deselect_all_tab()

        # Get Title Bar Btn And Reset Active
        top_settings = MainFunctions.get_title_bar_btn(self, "bttn_top_settings")
        top_settings.set_active(False)

        # LEFT MENU
        # HOME BTN
        if menu_bttn.objectName() == "bttn_home":
            # Close right panel and disable it, nothing to show
            if MainFunctions.right_column_is_visible(self):
                menu_bttn.set_active(False)
                MainFunctions.toggle_right_column(self)
            top_settings.setDisabled(True)
            # Select Menu
            self.ui.left_menu.select_only_one(menu_bttn.objectName())

            # Load Page 1
            MainFunctions.set_page(self, self.ui.load_pages.home_menu_container)
            # MainFunctions.set_right_column_menu(self, self.ui.right_column.menu_1)

        # WIDGETS BTN
        if menu_bttn.objectName() == "registration_bttn":
            # Select Menu
            self.ui.left_menu.select_only_one(menu_bttn.objectName())
            top_settings.setEnabled(True)

            # Load Page 2
            if self.first_two_pages == None:
                MainFunctions.set_page(self, self.ui.load_pages.image_dir_subpage)
            else:
                MainFunctions.set_page(self, self.first_two_pages)
            MainFunctions.set_right_column_menu(self, self.ui.right_column.slide_settings_column)

        # LOAD USER PAGE
        if menu_bttn.objectName() == "results_bttn":
            # Select Menu
            self.ui.left_menu.select_only_one(menu_bttn.objectName())
            top_settings.setEnabled(True)

            # Load Page 3
            # MainFunctions.set_page(self, self.ui.load_pages.result_page)
            # MainFunctions.set_right_column_menu(self, self.ui.right_column.results_right_column)
            if self.second_two_pages == None:
                MainFunctions.set_page(self, self.ui.load_pages.result_page)
            else:
                MainFunctions.set_page(self, self.second_two_pages)
            MainFunctions.set_right_column_menu(self, self.ui.right_column.results_right_column)

        # BOTTOM INFORMATION
        if menu_bttn.objectName() == "bttn_info":
            # CHECK IF LEFT COLUMN IS VISIBLE
            if not MainFunctions.left_column_is_visible(self):
                self.ui.left_menu.select_only_one_tab(menu_bttn.objectName())

                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(menu_bttn.objectName())
            else:
                if menu_bttn.objectName() == "bttn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    # Show / Hide
                    MainFunctions.toggle_left_column(self)

                self.ui.left_menu.select_only_one_tab(menu_bttn.objectName())

            # Change Left Column Menu
            if menu_bttn.objectName() != "bttn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self,
                    menu = self.ui.left_column.menus.info_menu,
                    title = "Info tab",
                    icon_path = Functions.set_svg_icon("icon_info.svg")
                )

        # SETTINGS LEFT
        if menu_bttn.objectName() == "bttn_settings" or menu_bttn.objectName() == "bttn_close_left_column":
            # CHECK IF LEFT COLUMN IS VISIBLE
            if not MainFunctions.left_column_is_visible(self):
                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(menu_bttn.objectName())
            else:
                if menu_bttn.objectName() == "bttn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    # Show / Hide
                    MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(menu_bttn.objectName())

            # Change Left Column Menu
            if menu_bttn.objectName() != "bttn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self,
                    menu = self.ui.left_column.menus.settings_menu,
                    title = "Settings Left Column",
                    icon_path = Functions.set_svg_icon("icon_settings.svg")
                )

        # TITLE BAR MENU
        # SETTINGS TITLE BAR
        if menu_bttn.objectName() == "bttn_top_settings":
            # Toogle Active
            if not MainFunctions.right_column_is_visible(self):
                menu_bttn.set_active(True)

                # Show / Hide
                MainFunctions.toggle_right_column(self)
            else:
                menu_bttn.set_active(False)

                # Show / Hide
                MainFunctions.toggle_right_column(self)

            # Get Left Menu Btn
            # top_settings = MainFunctions.get_left_menu_btn(self, "bttn_settings")
            # top_settings.set_active_tab(False)

        # DEBUG
        # print(f"Button {menu_bttn.objectName()}, clicked!")

    # LEFT MENU BTN IS RELEASED
    # Run function when menu_bttn is released
    # Check funtion by object name / btn_id
    def menu_released(self, menu_bttn):
        pass
        # GET BT CLICKED
        # menu_bttn = SetupMainWindow.setup_btns(self)

        # DEBUG
        # print(f"Button {menu_bttn.objectName()}, released!")

    def registration_page_picker(self, page):
        MainFunctions.set_page(self, page)

        slide_menu_bttn = self.ui.right_column.slide_navigation_bttn_frame.findChild(PyPushButton, 'slide_menu_bttn')
        registration_menu_bttn = self.ui.right_column.slide_navigation_bttn_frame.findChild(PyPushButton, 'registration_menu_bttn')
        if page == self.ui.load_pages.image_dir_subpage:
            slide_menu_bttn.set_highlight()
            registration_menu_bttn.remove_highlight()
        elif page == self.ui.load_pages.registration_settings_subpage:
            slide_menu_bttn.remove_highlight()
            registration_menu_bttn.set_highlight()

        self.first_two_pages = page

    def results_page_picker(self, page):
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

    # RESIZE EVENT
    def resizeEvent(self, event):
        SetupMainWindow.resize_grips(self)

    # MOUSE CLICK EVENTS
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPosition().toPoint()

    def closeEvent(self, event) -> None:
        #sender = self.sender()
        #if sender is not None:
        exit_buttons = {
            "Yes": QMessageBox.ButtonRole.YesRole,
            "No": QMessageBox.ButtonRole.NoRole
        }

        exit_message = QtMessage(buttons=exit_buttons,
                        color=self.themes["app_color"]["main_bg"],
                        bg_color_one=self.themes["app_color"]["dark_one"],
                        bg_color_two=self.themes["app_color"]["bg_one"],
                        bg_color_hover=self.themes["app_color"]["dark_three"],
                        bg_color_pressed=self.themes["app_color"]["dark_four"])
        exit_message.setIcon(QMessageBox.Icon.Warning)
        exit_message.setText("Are you sure you want to exit?")
        exit_message.setInformativeText("Any unsaved work will be lost.")
        exit_message.exec()

        if exit_message.clickedButton() == exit_message.buttons["Yes"]:
            QApplication.instance().closeAllWindows()
            event.accept()
        else:
            event.ignore()
        #else:
        #    print(f'Sender is none!')
        #    QApplication.instance().closeAllWindows()
        #    event.accept()
            # super().closeEvent(event)
