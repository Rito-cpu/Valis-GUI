import os

from src.core.pyqt_core import *
from src.core.app_config import IMG_RSC_PATH


class Ui_RightColumn(object):
    def setupUi(self, RightColumn):
        if not RightColumn.objectName():
            RightColumn.setObjectName(u"RightColumn")
        RightColumn.resize(240, 600)

        self.main_pages_layout = QVBoxLayout(RightColumn)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setObjectName(u"main_pages_layout")
        self.main_pages_layout.setContentsMargins(5, 5, 5, 5)

        self.menus = QStackedWidget(RightColumn)
        self.menus.setObjectName(u"menus")

        # Menu 1 page setup
        self.menu_1 = QWidget()
        self.menu_1.setObjectName(u"menu_1")

        self.verticalLayout = QVBoxLayout(self.menu_1)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)

        self.btn_1_widget = QWidget(self.menu_1)
        self.btn_1_widget.setObjectName(u"btn_1_widget")
        self.btn_1_widget.setMinimumSize(QSize(0, 40))
        self.btn_1_widget.setMaximumSize(QSize(16777215, 40))

        self.btn_1_layout = QVBoxLayout(self.btn_1_widget)
        self.btn_1_layout.setSpacing(0)
        self.btn_1_layout.setObjectName(u"btn_1_layout")
        self.btn_1_layout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout.addWidget(self.btn_1_widget)

        self.label_1 = QLabel(self.menu_1)
        self.label_1.setObjectName(u"label_1")

        font = QFont()
        font.setPointSize(16)

        self.label_1.setFont(font)
        self.label_1.setStyleSheet(u"font-size: 16pt")
        self.label_1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_1)

        self.menus.addWidget(self.menu_1)

        # ******************************************
        # **** Slide Upload and Settings Column ****
        # ******************************************
        self.slide_settings_column = QWidget()
        self.slide_settings_column.setObjectName(u"slide_settings_column")

        self.slide_navigation_label = QLabel(self.slide_settings_column)
        self.slide_navigation_label.setObjectName(u"slide_navigation_label")
        self.slide_navigation_label.setMaximumSize(QSize(16777215, 40))
        self.slide_navigation_label.setStyleSheet(u"font-size: 16pt;")
        self.slide_navigation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.slide_navigation_bttn_frame = QFrame(self.slide_settings_column)
        self.slide_navigation_bttn_frame.setObjectName(u"slide_navigation_bttn_frame")
        self.slide_navigation_bttn_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.slide_navigation_bttn_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.slide_navigation_bttn_layout = QVBoxLayout(self.slide_navigation_bttn_frame)
        self.slide_navigation_bttn_layout.setObjectName(u"slide_navigation_bttn_layout")
        self.slide_navigation_bttn_layout.setContentsMargins(5, 5, 5, 5)
        self.slide_navigation_bttn_layout.setSpacing(75)

        self.slide_navigation_layout = QVBoxLayout(self.slide_settings_column)
        self.slide_navigation_layout.setObjectName(u"slide_navigation_layout")
        self.slide_navigation_layout.setSpacing(5)
        self.slide_navigation_layout.setContentsMargins(5, 5, 5, 5)
        self.slide_navigation_layout.addWidget(self.slide_navigation_label)
        self.slide_navigation_layout.addStretch(1)
        self.slide_navigation_layout.addWidget(self.slide_navigation_bttn_frame)
        self.slide_navigation_layout.addStretch(1)

        # ************************************
        # **** Results Right Column Setup ****
        # ************************************
        self.results_right_column = QWidget()
        self.results_right_column.setObjectName(u"results_right_column")

        self.results_subpage_label = QLabel(self.results_right_column)
        self.results_subpage_label.setObjectName(u"results_subpage_label")
        self.results_subpage_label.setMaximumSize(QSize(16777215, 40))
        # self.results_subpage_label.setFont(font)
        self.results_subpage_label.setStyleSheet(u"font-size: 16pt")
        self.results_subpage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.results_button_frame = QFrame(self.results_right_column)
        self.results_button_frame.setObjectName(u"results_button_frame")
        self.results_button_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.results_button_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.results_bttn_layout = QVBoxLayout(self.results_button_frame)
        self.results_bttn_layout.setObjectName(u"results_bttn_layout")
        self.results_bttn_layout.setContentsMargins(5, 5, 5, 5)
        self.results_bttn_layout.setSpacing(75)

        self.results_column_layout = QVBoxLayout(self.results_right_column)
        self.results_column_layout.setObjectName(u"results_column_layout")
        self.results_column_layout.setContentsMargins(5, 5, 5, 5)
        self.results_column_layout.setSpacing(5)
        self.results_column_layout.addWidget(self.results_subpage_label)
        self.results_column_layout.addStretch(1)
        self.results_column_layout.addWidget(self.results_button_frame)
        self.results_column_layout.addStretch(1)

        # ******************
        # **** Finalize ****
        # ******************
        self.retranslateUi(RightColumn)

        self.menus.addWidget(self.slide_settings_column)
        self.menus.addWidget(self.results_right_column)
        self.menus.setCurrentIndex(1)

        self.main_pages_layout.addWidget(self.menus)

        QMetaObject.connectSlotsByName(RightColumn)
    # setupUi

    def retranslateUi(self, RightColumn):
        RightColumn.setWindowTitle(QCoreApplication.translate("RightColumn", u"Form", None))
        self.slide_navigation_label.setText(QCoreApplication.translate("RightColumn", u"Setup Navigation", None))
        self.label_1.setText(QCoreApplication.translate("RightColumn", u"Menu 1 - Right Menu", None))
        self.results_subpage_label.setText(QCoreApplication.translate("RightColumn", u"Results Navigation", None))
    # retranslateUi
