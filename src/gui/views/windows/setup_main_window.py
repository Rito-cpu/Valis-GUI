from functools import partial
from src.core.pyqt_core import *
from src.core.json.json_settings import Settings
from src.core.json.json_themes import Themes
from src.core.image_functions import Functions
from src.core.scripts.test_script import *
from src.core.keyword_store import *
from src.gui.models import *
from src.gui.views.windows.ui_main_window import UI_MainWindow
from src.gui.views.windows.functions_main_window import *
from src.gui.models.qt_slide_entry import *
from src.gui.models.qt_process_images import BFProcessWidget, IFProcessWidget


class SetupMainWindow:
    def __init__(self) -> None:
        super().__init__()
        # SETUP MAIN WINDOW
        # Load widgets from "gui\uis\main_window\ui_main.py"
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

    # Setup Main Window with custom parameters
    def setup_gui(self):
        # App title
        self.setWindowTitle(self.settings["app_name"])

        # Remove title bar
        if self.settings["custom_title_bar"]:
            self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # ADD GRIPS
        if self.settings["custom_title_bar"]:
            self.left_grip = PyGrips(self, "left", self.hide_grips)
            self.right_grip = PyGrips(self, "right", self.hide_grips)
            self.top_grip = PyGrips(self, "top", self.hide_grips)
            self.bottom_grip = PyGrips(self, "bottom", self.hide_grips)
            self.top_left_grip = PyGrips(self, "top_left", self.hide_grips)
            self.top_right_grip = PyGrips(self, "top_right", self.hide_grips)
            self.bottom_left_grip = PyGrips(self, "bottom_left", self.hide_grips)
            self.bottom_right_grip = PyGrips(self, "bottom_right", self.hide_grips)

        # LEFT MENUS / GET SIGNALS WHEN LEFT MENU BTN IS CLICKED / RELEASED
        # ADD LEFT MENUS
        left_menu_bttns = [
        {
            "bttn_icon" : "icon_home.svg",
            "bttn_id" : "bttn_home",
            "bttn_text" : "Home",
            "bttn_tooltip" : "Home page",
            "show_top" : True,
            "is_active" : True
        },
        {
            "bttn_icon" : "parameters_icon.svg",
            "bttn_id" : "registration_bttn",
            "bttn_text" : "Registration",
            "bttn_tooltip" : "Slide image settings",
            "show_top" : True,
            "is_active" : False
        },
        {
            "bttn_icon" : "results_icon.svg",
            "bttn_id" : "results_bttn",
            "bttn_text" : "Results",
            "bttn_tooltip" : "Slide registration results",
            "show_top" : True,
            "is_active" : False
        },
        {
            "bttn_icon" : "icon_info.svg",
            "bttn_id" : "bttn_info",
            "bttn_text" : "Information",
            "bttn_tooltip" : "Open informations",
            "show_top" : False,
            "is_active" : False
        }
        ]

        # ADD MENUS
        self.ui.left_menu.add_menus(left_menu_bttns)

        # SET SIGNALS
        self.ui.left_menu.clicked.connect(self.menu_clicked)
        self.ui.left_menu.released.connect(self.menu_released)

        # TITLE BAR / ADD EXTRA BUTTONS
        # ADD TITLE BAR MENUS
        title_bar_bttns = [
            {
                "bttn_icon" : "icon_menu.svg",
                "bttn_id" : "bttn_top_settings",
                "bttn_tooltip" : "Top settings",
                "is_active" : False
            }
        ]

        # ADD MENUS
        self.ui.title_bar.add_menus(title_bar_bttns)

        # SET SIGNALS
        self.ui.title_bar.clicked.connect(self.menu_clicked)
        self.ui.title_bar.released.connect(self.menu_released)

        # ADD Title
        if self.settings["custom_title_bar"]:
            self.ui.title_bar.set_title(self.settings["app_name"])
        else:
            self.ui.title_bar.set_title("Testing")   # ("Welcome to PyOneDark")

        # LEFT COLUMN SET SIGNALS
        self.ui.left_column.clicked.connect(self.menu_clicked)
        self.ui.left_column.released.connect(self.menu_released)

        # Right Column
#         self.ui.right_column.bt_1.clicked.connect(partial(self.page_picker, self.ui.load_pages.file_menu_container))
#         self.ui.right_column.bt_2.clicked.connect(partial(self.page_picker, self.ui.load_pages.parameter_menu_container))

        # SET INITIAL PAGE / SET LEFT AND RIGHT COLUMN MENUS
        MainFunctions.set_page(self, self.ui.load_pages.home_menu_container)
        MainFunctions.set_left_column_menu(
            self,
            menu = self.ui.left_column.menus.settings_menu,
            title = "Settings Left Column",
            icon_path = Functions.set_svg_icon("icon_settings.svg")
        )
        MainFunctions.set_right_column_menu(self, self.ui.right_column.menu_1)

        # OBJECTS FOR LOAD PAGES, LEFT AND RIGHT COLUMNS
        # You can access objects inside Qt Designer projects using
        # the objects below:
        #
        # <OBJECTS>
        # LEFT COLUMN: self.ui.left_column.menus
        # RIGHT COLUMN: self.ui.right_column
        # LOAD PAGES: self.ui.load_pages
        # </OBJECTS>

        # Load settings
        settings = Settings()
        self.settings = settings.items

        # Load Theme
        themes = Themes()
        self.themes = themes.items

        # *********************
        # **** Left Column ****
        # *********************
        self.left_btn_1 = QPushButton(text="Push Me")
        self.left_btn_1.setMaximumHeight(40)
        self.ui.left_column.menus.btn_1_layout.addWidget(self.left_btn_1)

        # ******************************
        # **** Right Column Widgets ****
        # ******************************
        self.slide_menu_bttn = PyPushButton(
            text="Slide Directory Menu",
            radius=8,
            color=self.themes["app_color"]["text_color"],
            bg_color=self.themes["app_color"]["yellow_bg"],
            bg_color_hover=self.themes["app_color"]["highlight_bg"],
            bg_color_pressed=self.themes["app_color"]["highlight_bg"],
            highlight=self.themes["app_color"]["green_bg"],
            parent=self.ui.right_column.slide_navigation_bttn_frame
        )
        self.slide_menu_bttn.setObjectName('slide_menu_bttn')
        self.slide_menu_bttn.setFixedHeight(38)
        self.slide_menu_bttn.set_highlight()

        self.registration_menu_bttn = PyPushButton(
            text="Registration Menu",
            radius=8,
            color=self.themes["app_color"]["text_color"],
            bg_color=self.themes["app_color"]["yellow_bg"],
            bg_color_hover=self.themes["app_color"]["highlight_bg"],
            bg_color_pressed=self.themes["app_color"]["highlight_bg"],
            highlight=self.themes["app_color"]["green_bg"],
            parent=self.ui.right_column.slide_navigation_bttn_frame
        )
        self.registration_menu_bttn.setObjectName('registration_menu_bttn')
        self.registration_menu_bttn.setFixedHeight(38)

        self.results_menu_bttn = PyPushButton(
            text="Results Menu",
            radius=8,
            color=self.themes["app_color"]["text_color"],
            bg_color=self.themes["app_color"]["yellow_bg"],
            bg_color_hover=self.themes["app_color"]["highlight_bg"],
            bg_color_pressed=self.themes["app_color"]["highlight_bg"],
            highlight=self.themes["app_color"]["green_bg"],
            parent=self.ui.right_column.results_button_frame
        )
        self.results_menu_bttn.setObjectName('results_menu_bttn')
        self.results_menu_bttn.setFixedHeight(38)
        self.results_menu_bttn.set_highlight()

        self.export_menu_bttn = PyPushButton(
            text="Export Menu",
            radius=8,
            color=self.themes["app_color"]["text_color"],
            bg_color=self.themes["app_color"]["yellow_bg"],
            bg_color_hover=self.themes["app_color"]["highlight_bg"],
            bg_color_pressed=self.themes["app_color"]["highlight_bg"],
            highlight=self.themes["app_color"]["green_bg"],
            parent=self.ui.right_column.results_button_frame
        )
        self.export_menu_bttn.setObjectName('export_menu_bttn')
        self.export_menu_bttn.setFixedHeight(38)

        self.ui.right_column.slide_navigation_bttn_layout.addWidget(self.slide_menu_bttn)
        self.ui.right_column.slide_navigation_bttn_layout.addWidget(self.registration_menu_bttn)
        self.ui.right_column.results_bttn_layout.addWidget(self.results_menu_bttn)
        self.ui.right_column.results_bttn_layout.addWidget(self.export_menu_bttn)

        self.slide_menu_bttn.clicked.connect(lambda: self.registration_page_picker(self.ui.load_pages.image_dir_subpage))
        self.registration_menu_bttn.clicked.connect(lambda: self.registration_page_picker(self.ui.load_pages.registration_settings_subpage))
        self.results_menu_bttn.clicked.connect(lambda: self.results_page_picker(self.ui.load_pages.result_page))
        self.export_menu_bttn.clicked.connect(lambda: self.results_page_picker(self.ui.load_pages.export_page))
        self.ui.right_column.context_file_bttn.clicked.connect(lambda: MainFunctions.launch_context_window(self))

        # Pages
        # Page 1 - Add logo to main page
        # self.logo_svg = QSvgWidget(Functions.set_svg_image("logo_home.svg"))
        # self.ui.load_pages.logo_layout.addWidget(self.logo_svg, Qt.AlignCenter, Qt.AlignCenter)

        # *********************************
        # ******** Home Page Setup ********
        # *********************************
        self.proj_dir_entry = QtButtonLineEdit(
            title="Project Directory",
            title_color=self.themes["app_color"]["text_color"],
            color_three=self.themes['app_color']['blue_bg'],
            top_margin=18,
            parent=self.ui.load_pages.directory_frame
        )
        self.proj_dir_entry.setObjectName(u'proj_dir_entry')
        self.proj_dir_entry.setMinimumWidth(350)

        self.submit_dir_bttn = PyPushButton(
            text="Submit",
            radius=8,
            color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            parent=self.ui.load_pages.directory_frame
        )
        self.submit_dir_bttn.setObjectName(u"dir_submit_bttn")
        self.submit_dir_bttn.setMinimumSize(85, 31)

        self.project_dir_label = QtMarqueeLabel(
            color=self.themes["app_color"]["text_white"],
            parent=self.ui.load_pages.project_dir_frame
        )
        self.project_dir_label.setMinimumWidth(275)
        self.project_dir_label.setText('None')

        self.submit_dir_bttn.clicked.connect(
            lambda: MainFunctions.set_project_directory(
                self,
                self.proj_dir_entry.text(),
                self.project_dir_label
            )
        )

        self.ui.load_pages.dir_entry_interaction.addWidget(self.proj_dir_entry)

        self.ui.load_pages.bttn_holder.addWidget(self.submit_dir_bttn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.ui.load_pages.dir_entry_interaction.addLayout(self.ui.load_pages.bttn_holder)

        self.ui.load_pages.project_dir_layout.addWidget(self.project_dir_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.ui.load_pages.project_dir_layout.addStretch(1)

        self.ui.load_pages.project_dir_frame.setMaximumWidth(self.ui.load_pages.dir_entry_interaction.sizeHint().width())

        # ****************************************
        # ****** Slide Directory Page Setup ******
        # ****************************************
        self.slide_directory = QtSlideDirectory(
            text_color=self.themes['app_color']['text_color'],
            blue_color=self.themes['app_color']['blue_bg'],
            yellow_color=self.themes['app_color']['yellow_bg'],
            highlight_color=self.themes['app_color']['highlight_bg'],
            parent=self.ui.load_pages.immuno_dir_interaction
        )
        self.slide_directory.setObjectName('slide_directory')

        self.submit_file_bttn = PyPushButton(
            text="Submit",
            radius=8,
            color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            font_size=14,
            parent=self.ui.load_pages.immuno_dir_interaction
        )
        self.submit_file_bttn.setObjectName(u"submit_file_bttn")
        self.submit_file_bttn.setMinimumSize(120, 40)

        submit_file_bttn_layout = QHBoxLayout()
        submit_file_bttn_layout.addStretch(1)
        submit_file_bttn_layout.addWidget(self.submit_file_bttn)
        submit_file_bttn_layout.addStretch(1)

        self.slide_directory.dir_tree.clear_bttn.clicked.connect(lambda: MainFunctions.clear_pressed(self))
        self.submit_file_bttn.clicked.connect(lambda: MainFunctions.upload_slides(self, self.slide_directory))

        self.ui.load_pages.immuno_interaction_layout.addWidget(self.slide_directory, alignment=Qt.AlignmentFlag.AlignCenter)
        self.ui.load_pages.immuno_interaction_layout.addLayout(submit_file_bttn_layout)

        # ****************************************
        # *** Registration Settings Page Setup ***
        # ****************************************
        self.bf_process = BFProcessWidget(parent=self.ui.load_pages.registration_scroll_contents)
        self.if_process = IFProcessWidget(parent=self.ui.load_pages.registration_scroll_contents)
        self.rigid_settings = RigidSettings(parent=self.ui.load_pages.registration_scroll_contents)
        non_rigid_settings = NonRigidSettings(parent=self.ui.load_pages.registration_scroll_contents)

        self.register_setting_bttn = PyPushButton(
            text="Register",
            radius=8,
            color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            font_size=14,
            parent=self.ui.load_pages.registration_scroll_contents
        )
        self.register_setting_bttn.setObjectName(u"register_setting_bttn")
        self.register_setting_bttn.setMinimumSize(120, 40)
        self.register_setting_bttn.clicked.connect(
            lambda: MainFunctions.register_settings(
                self,
                self.bf_process,
                self.if_process,
                self.rigid_settings,
                non_rigid_settings
            )
        )

        register_settings_bttn_layout = QHBoxLayout()
        register_settings_bttn_layout.addStretch(1)
        register_settings_bttn_layout.addWidget(self.register_setting_bttn)
        register_settings_bttn_layout.addStretch(1)

        self.ui.load_pages.registration_scroll_layout.addWidget(self.bf_process)
        self.ui.load_pages.registration_scroll_layout.addWidget(self.if_process)
        self.ui.load_pages.registration_scroll_layout.addWidget(self.rigid_settings)
        self.ui.load_pages.registration_scroll_layout.addWidget(non_rigid_settings)
        self.ui.load_pages.registration_scroll_layout.addLayout(register_settings_bttn_layout)

        # **************************
        # *** Results Page Setup ***
        # **************************
        image_path_1 = '/Users/4474613/Downloads/ihc_2.png'
        img_1 = QPixmap.fromImage(QImage(image_path_1))

        image_path_2 = '/Users/4474613/Downloads/3_ihc_2_rigid.png'
        img_2 = QPixmap.fromImage(QImage(image_path_2))

        image_path_3 = '/Users/4474613/Downloads/3_ihc_2_deformation.png'
        img_3 = QPixmap.fromImage(QImage(image_path_3))

        img_list = [img_1, img_2, img_3]
        img_names = [os.path.basename(image_path_1), os.path.basename(image_path_2), os.path.basename(image_path_3)]

        self.results_area = QtResultsArea(
            sample_data=results_table_list,
            parent=self.ui.load_pages.results_sideways_frame
        )

        result_image_area = QFrame(self.ui.load_pages.results_sideways_frame)
        result_image_area.setObjectName('image_area')
        result_image_area.setFrameShape(QFrame.Shape.NoFrame)
        result_image_area.setFrameShadow(QFrame.Shadow.Raised)

        self.results_image_view = QtImageView(
            dimensions=(200, 200),
            parent=result_image_area
        )
        # self.results_image_view.add_images(results_table_list[0], img_list, img_names)
        # 325, 465

        self.results_type_combo = QtComboBox(
            bg_color=self.themes["app_color"]["yellow_bg"],
            text_color=self.themes["app_color"]["text_color"],
            parent=result_image_area
        )
        self.results_type_combo.setObjectName('results_type_combo')
        # self.sample_type_combo.addItems(self._detectors)
        self.results_type_combo.addItems(['Original', 'Processed', 'Aligned (Rigid)', 'Aligned (Non-Rigid)', 'Deformation', 'Error'])
        self.results_type_combo.setCurrentIndex(0)
        self.results_type_combo.setFixedHeight(30)
        self.results_type_combo.setMinimumWidth(250)

        result_image_area_layout = QVBoxLayout(result_image_area)
        result_image_area_layout.setObjectName('image_area_layout')
        result_image_area_layout.setContentsMargins(5, 5, 5, 5)
        result_image_area_layout.setSpacing(10)
        result_image_area_layout.addWidget(self.results_image_view)
        result_image_area_layout.addWidget(self.results_type_combo, alignment=Qt.AlignmentFlag.AlignCenter)

        results_bttn_frame = QFrame(self.ui.load_pages.results_scroll_content)
        results_bttn_frame.setObjectName('results_bttn_area')
        results_bttn_frame.setFrameShape(QFrame.Shape.NoFrame)
        results_bttn_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.export_data_bttn = PyPushButton(
            text="Export Results",
            radius=8,
            color=self.themes["app_color"]["text_color"],
            bg_color=self.themes["app_color"]["yellow_bg"],
            bg_color_hover=self.themes["app_color"]["highlight_bg"],
            bg_color_pressed=self.themes["app_color"]["highlight_bg"],
            font_size=14,
            parent=results_bttn_frame
        )
        self.export_data_bttn.setObjectName('export_data_bttn')
        self.export_data_bttn.clicked.connect(lambda: MainFunctions.export_data(self))
        self.export_data_bttn.setFixedSize(200, 35)

        self.cancel_results_bttn = PyPushButton(
            text="Cancel",
            radius=8,
            color=self.themes["app_color"]["text_color"],
            bg_color=self.themes["app_color"]["yellow_bg"],
            bg_color_hover=self.themes["app_color"]["highlight_bg"],
            bg_color_pressed=self.themes["app_color"]["highlight_bg"],
            font_size=14,
            parent=results_bttn_frame
        )
        self.cancel_results_bttn.setObjectName('cancel_results_bttn')
        self.cancel_results_bttn.setFixedSize(200, 35)

        results_bttn_layout = QHBoxLayout(results_bttn_frame)
        results_bttn_layout.setObjectName('results_bttn_layout')
        results_bttn_layout.setContentsMargins(5, 5, 5, 5)
        results_bttn_layout.setSpacing(15)
        results_bttn_layout.addWidget(self.export_data_bttn)
        results_bttn_layout.addWidget(self.cancel_results_bttn)

        self.ui.load_pages.results_sideways_layout.addWidget(self.results_area)
        # self.ui.load_pages.results_sideways_layout.addWidget(self.results_image_view)
        self.ui.load_pages.results_sideways_layout.addWidget(result_image_area)
        # self.ui.load_pages.results_scroll_layout.addWidget(self.export_data_bttn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.ui.load_pages.results_scroll_layout.addWidget(results_bttn_frame)

        # ***************************
        # **** Export Page Setup ****
        # ***************************
        self.export_area = QtExportArea(
            sample_data=export_obj_data,
            parent=self.ui.load_pages.export_sideways_frame
        )

        export_image_area = QFrame(self.ui.load_pages.export_sideways_frame)
        export_image_area.setObjectName('export_image_area')
        export_image_area.setFrameShape(QFrame.Shape.NoFrame)
        export_image_area.setFrameShadow(QFrame.Shadow.Raised)

        self.export_image_view = QtImageView(
            dimensions=(200, 200),
            parent=export_image_area
        )
        # self.export_image_view.add_images(results_table_list[0], img_list, img_names)

        self.export_type_combo = QtComboBox(
            bg_color=self.themes["app_color"]["yellow_bg"],
            text_color=self.themes["app_color"]["text_color"],
            parent=export_image_area
        )
        self.export_type_combo.setObjectName('export_type_combo')
        # self.sample_type_combo.addItems(self._detectors)
        self.export_type_combo.addItems(['Original', 'Processed', 'Aligned (Rigid)', 'Aligned (Non-Rigid)', 'Deformation', 'Error'])
        self.export_type_combo.setCurrentIndex(0)
        self.export_type_combo.setFixedHeight(30)
        self.export_type_combo.setMinimumWidth(250)

        export_image_area_layout = QVBoxLayout(export_image_area)
        export_image_area_layout.setObjectName('export_image_area_layout')
        export_image_area_layout.setContentsMargins(5, 5, 5, 5)
        export_image_area_layout.setSpacing(10)
        export_image_area_layout.addWidget(self.export_image_view)
        export_image_area_layout.addWidget(self.export_type_combo, alignment=Qt.AlignmentFlag.AlignCenter)

        export_bttn_frame = QFrame(self.ui.load_pages.export_scroll_contents)
        export_bttn_frame.setObjectName('export_bttn_frame')
        export_bttn_frame.setFrameShape(QFrame.Shape.NoFrame)
        export_bttn_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.export_slides_bttn = PyPushButton(
            text="Export Slides",
            radius=8,
            color=self.themes["app_color"]["text_color"],
            bg_color=self.themes["app_color"]["yellow_bg"],
            bg_color_hover=self.themes["app_color"]["highlight_bg"],
            bg_color_pressed=self.themes["app_color"]["highlight_bg"],
            highlight=self.themes["app_color"]["green_bg"],
            parent=export_bttn_frame
        )
        self.export_slides_bttn.setObjectName('_export_slides_bttn')
        self.export_slides_bttn.setFixedSize(200, 35)

        self.cancel_export_bttn = PyPushButton(
            text="Cancel",
            radius=8,
            color=self.themes["app_color"]["text_color"],
            bg_color=self.themes["app_color"]["yellow_bg"],
            bg_color_hover=self.themes["app_color"]["highlight_bg"],
            bg_color_pressed=self.themes["app_color"]["highlight_bg"],
            highlight=self.themes["app_color"]["green_bg"],
            parent=export_bttn_frame
        )
        self.cancel_export_bttn.setObjectName('cancel_export_bttn')
        self.cancel_export_bttn.setFixedSize(150, 35)
        self.cancel_export_bttn.hide()

        self.export_slides_bttn.clicked.connect(
            lambda: MainFunctions.export_clicked(
                self,
                self.export_area.show_bar_frame,
                self.cancel_export_bttn.show
            )
        )
        self.cancel_export_bttn.clicked.connect(
            lambda: MainFunctions.cancel_export(
                self,
                self.export_area.hide_bar_frame,
                self.cancel_export_bttn.hide
            )
        )

        export_bttn_layout = QHBoxLayout(export_bttn_frame)
        export_bttn_layout.setObjectName('export_bttn_layout')
        export_bttn_layout.setContentsMargins(5, 5, 5, 5)
        export_bttn_layout.setSpacing(15)
        export_bttn_layout.addWidget(self.export_slides_bttn)
        export_bttn_layout.addWidget(self.cancel_export_bttn)

        self.ui.load_pages.export_sideways_layout.addWidget(self.export_area)
        # self.ui.load_pages.export_sideways_layout.addWidget(self.export_image_view)
        self.ui.load_pages.export_sideways_layout.addWidget(export_image_area)
        # self.ui.load_pages.export_scroll_layout.addWidget(self.export_slides_bttn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.ui.load_pages.export_scroll_layout.addWidget(export_bttn_frame)

        # PAGE 2
        # CIRCULAR PROGRESS 1
        # self.circular_progress_1 = PyCircularProgress(
        #     value = 80,
        #     progress_color = self.themes["app_color"]["context_color"],
        #     text_color = self.themes["app_color"]["text_title"],
        #     font_size = 14,
        #     bg_color = self.themes["app_color"]["dark_four"]
        # )
        # self.circular_progress_1.setFixedSize(200,200)

        # Add widgets
        # Accessing layout from load pages itself
        # self.ui.load_pages.row_1_layout.addWidget(widget)

    # RESIZE GRIPS AND CHANGE POSITION
    # Resize or change position when window is resized

    def resize_grips(self):
        if self.settings["custom_title_bar"]:
            self.left_grip.setGeometry(5, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 15, 10, 10, self.height())
            self.top_grip.setGeometry(5, 5, self.width() - 10, 10)
            self.bottom_grip.setGeometry(5, self.height() - 15, self.width() - 10, 10)
            self.top_right_grip.setGeometry(self.width() - 20, 5, 15, 15)
            self.bottom_left_grip.setGeometry(5, self.height() - 20, 15, 15)
            self.bottom_right_grip.setGeometry(self.width() - 20, self.height() - 20, 15, 15)
