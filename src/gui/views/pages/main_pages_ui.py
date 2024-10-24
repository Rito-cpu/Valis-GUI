# -*- coding: utf-8 -*-
from src.core.pyqt_core import *
from src.core.image_functions import Functions
from src.gui.models import *


class Ui_MainPages(object):
    """Creates multiple QWidget pages to be placed in a QStackedWidget and placed in the Main Window.

    Args:
        MainPages (object): The main window or parents widget that will contain the pages.
    """
    def setupUi(self, MainPages):
        if not MainPages.objectName():
            MainPages.setObjectName(u"MainPages")
        MainPages.resize(860, 600)

        # ***********************************
        # * Home page Frame/Layout creation *
        # ***********************************
        self.home_menu_container = QWidget()
        self.home_menu_container.setObjectName(u"home_page")
        self.home_menu_container.setStyleSheet(u"font-size: 14pt")

        home_menu_layout = QVBoxLayout(self.home_menu_container)
        home_menu_layout.setContentsMargins(5, 5, 5, 5)
        home_menu_layout.setSpacing(75)
        home_menu_layout.setObjectName(u"home_menu_layout")

        home_upper_frame = QFrame(self.home_menu_container)
        home_upper_frame.setObjectName(u"logo_frame")
        home_upper_frame.setFrameShape(QFrame.Shape.NoFrame)
        home_upper_frame.setFrameShadow(QFrame.Shadow.Raised)

        home_label = QLabel(home_upper_frame)
        home_label.setObjectName(u"label")
        home_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        home_label.setText(QCoreApplication.translate("MainPages", u"", None))
        home_label.setStyleSheet('font-size: 16px; font-weight: bold;')
        home_label.hide()

        home_logo_frame = QFrame(home_upper_frame)
        home_logo_frame.setObjectName(u"home_logo_frame")
        home_logo_frame.setMinimumSize(QSize((2107/5), (517/5)))
        home_logo_frame.setMaximumSize(QSize((2107/5), (517/5)))
        home_logo_frame.setFrameShape(QFrame.Shape.NoFrame)
        home_logo_frame.setFrameShadow(QFrame.Shadow.Raised)

        valis_logo = QSvgWidget(Functions.set_svg_image("valis_logo.svg"))

        home_logo_layout = QVBoxLayout(home_logo_frame)
        home_logo_layout.setContentsMargins(0, 0, 0, 0)
        home_logo_layout.setSpacing(0)
        home_logo_layout.setObjectName(u"home_logo_layout")
        home_logo_layout.addWidget(valis_logo, Qt.AlignmentFlag.AlignCenter, Qt.AlignmentFlag.AlignCenter)

        home_upper_layout = QVBoxLayout(home_upper_frame)
        home_upper_layout.setContentsMargins(0, 30, 0, 0)
        home_upper_layout.setSpacing(75)
        home_upper_layout.addWidget(home_label, alignment=Qt.AlignmentFlag.AlignCenter)
        home_upper_layout.addWidget(home_logo_frame, alignment=Qt.AlignmentFlag.AlignCenter)

        home_tab_container = QFrame(self.home_menu_container)
        home_tab_container.setObjectName('home_tab_container')
        home_tab_container.setFrameShape(QFrame.Shape.NoFrame)
        home_tab_container.setFrameShadow(QFrame.Shadow.Raised)

        self.home_tab_layout = QVBoxLayout(home_tab_container)
        self.home_tab_layout.setObjectName('home_tab_layout')
        self.home_tab_layout.setContentsMargins(30, 0, 30, 30)

        home_menu_layout.addWidget(home_upper_frame, 0, Qt.AlignmentFlag.AlignHCenter)
        home_menu_layout.addWidget(home_tab_container)

        # *********************************
        # **** Image Directory Page ****
        # *********************************
        self.image_dir_subpage = QWidget()
        self.image_dir_subpage.setObjectName(u"image_dir_subpage")

        self.file_scroll_area = QScrollArea(self.image_dir_subpage)
        self.file_scroll_area.setObjectName(u"scroll_area")
        self.file_scroll_area.setStyleSheet(u"background: transparent;")
        self.file_scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.file_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.file_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.file_scroll_area.setWidgetResizable(True)

        # self.file_scroll_contents = QWidget(self.image_dir_subpage)
        self.file_scroll_contents = QWidget(self.file_scroll_area)
        self.file_scroll_contents.setObjectName(u"contents")
        self.file_scroll_contents.setGeometry(QRect(0, 0, 840, 580))
        # self.etb_scroll_contents.setStyleSheet(u"border: 2px solid lightblue;")
        self.file_scroll_contents.setStyleSheet(u"background: transparent;")

        font = QFont()
        font.setPointSize(16)
        self.image_dir_title = QLabel(self.file_scroll_contents)
        self.image_dir_title.setObjectName(u"image_dir_title")
        self.image_dir_title.setMaximumSize(QSize(16777215, 40))
        # self.import_data_title.font().setPointSize(22)
        # self.import_data_title.font().setBold(True)
        self.image_dir_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.image_dir_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.slide_dir_interaction = QWidget(self.file_scroll_contents)
        self.slide_dir_interaction.setObjectName('slide_dir_interaction')

        self.slide_interaction_layout = QVBoxLayout(self.slide_dir_interaction)
        self.slide_interaction_layout.setObjectName('slide_interaction_layout')
        self.slide_interaction_layout.setContentsMargins(0, 0, 0, 0)
        self.slide_interaction_layout.setSpacing(15)

        self.file_content_layout = QVBoxLayout(self.file_scroll_contents)
        self.file_content_layout.setObjectName(u"file_content_layout")
        self.file_content_layout.setContentsMargins(5, 5, 5, 5)
        self.file_content_layout.setSpacing(50)
        # self.file_content_layout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.file_content_layout.addWidget(self.image_dir_title)
        self.file_content_layout.addWidget(self.slide_dir_interaction)

        self.file_scroll_area.setWidget(self.file_scroll_contents)

        self.dir_interaction_layout = QVBoxLayout(self.image_dir_subpage)
        self.dir_interaction_layout.setSpacing(50)
        self.dir_interaction_layout.setObjectName(u"page_2_layout")
        self.dir_interaction_layout.setContentsMargins(5, 5, 5, 5)
        # self.dir_interaction_layout.addWidget(self.file_scroll_contents)
        self.dir_interaction_layout.addWidget(self.file_scroll_area)

        # ***************************************
        # **** Registration Settings Page ****
        # ***************************************
        self.registration_settings_subpage = QWidget()
        self.registration_settings_subpage.setObjectName(u"registration_settings_subpage")

        registration_scroll_area = QScrollArea(self.registration_settings_subpage)
        registration_scroll_area.setObjectName(u"registration_scroll_area")
        registration_scroll_area.setStyleSheet(u"background: transparent;")
        registration_scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        registration_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        registration_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        registration_scroll_area.setWidgetResizable(True)

        self.registration_scroll_contents = QWidget(parent=registration_scroll_area)
        self.registration_scroll_contents.setObjectName(u"registration_scroll_contents")
        self.registration_scroll_contents.setGeometry(QRect(0, 0, 840, 580))
        self.registration_scroll_contents.setStyleSheet(u"background: transparent;")
        registration_scroll_area.setWidget(self.registration_scroll_contents)

        self.registration_title = QLabel(self.registration_scroll_contents)
        self.registration_title.setObjectName(u"registration_title")
        self.registration_title.setMaximumSize(QSize(16777215, 40))
        # self.parameter_title.font().setPointSize(22)
        # self.parameter_title.font().setBold(True)
        self.registration_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.registration_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.registration_scroll_layout = QVBoxLayout(self.registration_scroll_contents)
        self.registration_scroll_layout.setObjectName(u"registration_scroll_layout")
        self.registration_scroll_layout.setContentsMargins(5, 5, 5, 5)
        self.registration_scroll_layout.setSpacing(25)
        # self.parameter_scroll_layout.addWidget(self.parameter_title)

        self.registration_center_layout = QVBoxLayout(self.registration_settings_subpage)
        self.registration_center_layout.setSpacing(40)
        self.registration_center_layout.setContentsMargins(15, 5, 15, 5)
        self.registration_center_layout.setObjectName(u"registration_center_layout")
        self.registration_center_layout.addWidget(self.registration_title)
        self.registration_center_layout.addWidget(registration_scroll_area)

        # ****************************
        # **** Results Page Setup ****
        # ****************************
        self.result_page = QWidget()
        self.result_page.setObjectName(u"result_page")

        self.results_scroll_content = QWidget()
        self.results_scroll_content.setObjectName(u"results_scroll_content")
        self.results_scroll_content.setGeometry(QRect(0, 0, 840, 580))
        self.results_scroll_content.setStyleSheet(u"background: transparent;")

        self.results_sideways_frame = QFrame(self.results_scroll_content)
        self.results_sideways_frame.setObjectName('results_sideways_frame')
        self.results_sideways_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.results_sideways_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.results_sideways_layout = QHBoxLayout(self.results_sideways_frame)
        self.results_sideways_layout.setObjectName('results_sideways_layout')
        self.results_sideways_layout.setContentsMargins(0, 0, 0, 0)
        self.results_sideways_layout.setSpacing(10)

        results_scroll_area = QScrollArea(self.result_page)
        results_scroll_area.setObjectName(u"results_scroll_area")
        results_scroll_area.setStyleSheet(u"background: transparent;")
        results_scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        results_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        results_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        results_scroll_area.setWidgetResizable(True)
        results_scroll_area.setWidget(self.results_scroll_content)

        self.result_page_title = QLabel(self.result_page)
        self.result_page_title.setObjectName("result_page_title")
        self.result_page_title.setMaximumSize(QSize(16777215, 40))
        self.result_page_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.result_page_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.results_scroll_layout = QVBoxLayout(self.results_scroll_content)
        self.results_scroll_layout.setObjectName('results_scroll_layout')
        self.results_scroll_layout.setContentsMargins(5, 5, 5, 5)
        self.results_scroll_layout.setSpacing(25)
        self.results_scroll_layout.addWidget(self.results_sideways_frame)

        self.result_page_layout = QVBoxLayout(self.result_page)
        self.result_page_layout.setObjectName(u"result_page_layout")
        self.result_page_layout.setContentsMargins(15, 5, 15, 5)
        self.result_page_layout.setSpacing(5)
        self.result_page_layout.addWidget(self.result_page_title)
        self.result_page_layout.addWidget(results_scroll_area)

        # ********************************
        # **** Export Data Page Setup ****
        # ********************************
        self.export_page = QWidget()
        self.export_page.setObjectName('export_page')

        self.export_scroll_contents = QWidget()
        self.export_scroll_contents.setObjectName(u"export_scroll_contents")
        self.export_scroll_contents.setGeometry(QRect(0, 0, 840, 580))
        self.export_scroll_contents.setStyleSheet(u"background: transparent;")

        self.export_sideways_frame = QFrame(self.export_scroll_contents)
        self.export_sideways_frame.setObjectName('export_sideways_frame')
        self.export_sideways_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.export_sideways_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.export_sideways_layout = QHBoxLayout(self.export_sideways_frame)
        self.export_sideways_layout.setObjectName('export_sideways_layout')
        self.export_sideways_layout.setContentsMargins(0, 0, 0, 0)
        self.export_sideways_layout.setSpacing(10)

        export_scroll_area = QScrollArea(self.export_page)
        export_scroll_area.setObjectName(u"export_scroll_area")
        export_scroll_area.setStyleSheet(u"background: transparent;")
        export_scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        export_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        export_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        export_scroll_area.setWidgetResizable(True)
        export_scroll_area.setWidget(self.export_scroll_contents)

        self.export_title_label = QLabel(self.export_scroll_contents)
        self.export_title_label.setObjectName(u"export_title_label")
        self.export_title_label.setMaximumSize(QSize(16777215, 40))
        self.export_title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.export_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.export_scroll_layout = QVBoxLayout(self.export_scroll_contents)
        self.export_scroll_layout.setObjectName(u"export_scroll_layout")
        self.export_scroll_layout.setContentsMargins(5, 5, 5, 5)
        self.export_scroll_layout.setSpacing(25)
        self.export_scroll_layout.addWidget(self.export_sideways_frame)

        self.export_page_layout = QVBoxLayout(self.export_page)
        self.export_page_layout.setObjectName(u"export_page_layout")
        self.export_page_layout.setContentsMargins(15, 5, 15, 5)
        self.export_page_layout.setSpacing(5)
        self.export_page_layout.addWidget(self.export_title_label)
        self.export_page_layout.addWidget(export_scroll_area)

        # ************************
        # **** Finalize Pages ****
        # ************************
        self.pages = QStackedWidget(MainPages)
        self.pages.setObjectName(u"pages")
        self.pages.addWidget(self.home_menu_container)
        self.pages.addWidget(self.image_dir_subpage)
        self.pages.addWidget(self.registration_settings_subpage)
        self.pages.addWidget(self.result_page)
        self.pages.addWidget(self.export_page)
        self.pages.setCurrentIndex(1)

        self.main_pages_layout = QVBoxLayout(MainPages)
        self.main_pages_layout.setContentsMargins(5, 5, 5, 5)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setObjectName(u"main_pages_layout")
        self.main_pages_layout.addWidget(self.pages)

        self.retranslate_ui(MainPages)

        QMetaObject.connectSlotsByName(MainPages)
    # setupUi

    def retranslate_ui(self, MainPages):
        MainPages.setWindowTitle(QCoreApplication.translate("MainPages", u"Form", None))
        self.image_dir_title.setText(QCoreApplication.translate("MainPages", u"Sample Upload ", None))
        self.registration_title.setText(QCoreApplication.translate("MainPages", u"Registration Settings", None))
        self.result_page_title.setText(QCoreApplication.translate("MainPages", u"Results View", None))
        self.export_title_label.setText(QCoreApplication.translate("MainPages", u"Export Results", None))
