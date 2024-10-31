from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.core.image_functions import Functions
from src.core.app_config import IMG_RSC_PATH
from src.gui.models.qt_message import QtMessage
from src.gui.models.qt_collapsible_box import QtSectionalWidget
from src.gui.models.qt_clickable_label import QtClickableLabel


class NewTab(QWidget):
    def __init__(
        self,
        parent=None
    ):
        super().__init__(parent)

        if parent is not None:
            self.parent = parent

        themes = Themes()
        self.themes = themes.items

        self.setObjectName('NewTab')
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self._setup_widget()

    def _setup_widget(self):
        section_font = QFont()
        section_font.setPointSize(28)
        section_font.setBold(True)

        container_frame = QFrame(self)
        container_frame.setObjectName('container_frame')
        container_frame.setFrameShape(QFrame.Shape.NoFrame)
        container_frame.setFrameShadow(QFrame.Shadow.Plain)
        container_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        #container_frame.setStyleSheet('QFrame#container_frame{background-color: yellow;}')

        starting_label = QLabel(container_frame)
        starting_label.setObjectName('starting_label')
        starting_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        starting_label.setText("Getting Started with VALIS!")
        starting_label.setStyleSheet('font-weight: bold; font-size: 22px;')

        section_scroll_area = QScrollArea(container_frame)
        section_scroll_area.setObjectName("section_scroll_area")
        section_scroll_area.setStyleSheet("background: transparent;")
        section_scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        section_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        section_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        section_scroll_area.setWidgetResizable(True)

        sectional_house = QFrame(section_scroll_area)
        sectional_house.setObjectName('sectional_house')
        sectional_house.setFrameShape(QFrame.Shape.NoFrame)
        sectional_house.setFrameShadow(QFrame.Shadow.Plain)
        sectional_house.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        section_scroll_area.setWidget(sectional_house)

        navigation_frame = QtSectionalWidget(
            section_title="Quick Navigation",
            icon_name="compass_icon.svg",
            collapsed_info="Click here to open the quick navigation menu.",
            expanded_info="Quick navigation menu.",
            icon_size=63,
            parent=sectional_house
        )

        documentation_frame = QtSectionalWidget(
            section_title="Documentation",
            icon_name="internet_icon.svg",
            collapsed_info="Click here to open the documentation section.",
            expanded_info="Documentation section.",
            icon_size=65,
            parent=sectional_house
        )

        sectional_layout = QGridLayout(sectional_house)
        sectional_layout.setObjectName('sectional_layout')
        sectional_layout.setContentsMargins(80, 10, 80, 10)
        sectional_layout.setSpacing(20)
        sectional_layout.addWidget(navigation_frame)
        sectional_layout.addWidget(documentation_frame)

        self.valis_docs_label = QtClickableLabel(
            text='Valis Docs',
            font_size=12,
            parent=container_frame
        )
        self.valis_docs_label.setObjectName('valis_docs_label')
        self.valis_docs_label.setHyperLink("https://valis.readthedocs.io/en/latest/index.html#")
        self.valis_docs_label.linkActivated.connect(self.open_hyperlink)

        self.valis_install_label = QtClickableLabel(
            text='Valis Installation',
            font_size=12,
            parent=container_frame
        )
        self.valis_install_label.setObjectName('valis_install_label')
        self.valis_install_label.setHyperLink("https://valis.readthedocs.io/en/latest/installation.html#")
        self.valis_install_label.linkActivated.connect(self.open_hyperlink)

        container_layout = QVBoxLayout(container_frame)
        container_layout.setObjectName('container_layout')
        container_layout.setContentsMargins(10, 10, 10, 10)
        container_layout.setSpacing(15)
        container_layout.addWidget(starting_label, alignment=Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(section_scroll_area)
        #container_layout.addWidget(self.valis_docs_label, alignment=Qt.AlignmentFlag.AlignCenter)
        #container_layout.addWidget(self.valis_install_label, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout = QVBoxLayout(self)
        main_layout.setObjectName('main_layout')
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container_frame)

    def open_hyperlink(self, label_link: str):
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
        error_msg.setIcon(QMessageBox.Icon.Critical)

        try:
            QDesktopServices.openUrl(QUrl(label_link))
        except FileNotFoundError as file_err:
            error_msg.setText("No URL Handler!")
            error_msg.setInformativeText("No application associated with handling URL's was found on your system!")
            error_msg.exec()
            return
        except ValueError as val_err:
            error_msg.setText("Invalid URL!")
            error_msg.setInformativeText("The URL value no longer exists or is invalid.")
            error_msg.exec()
            return
        except OSError as os_err:
            error_msg.setText("Execution Error!")
            error_msg.setInformativeText("Encountered issue executing hyperlink command with current operating system constraints.")
            error_msg.exec()
            return
        except Exception as err:
            error_msg.setText("General Error!")
            error_msg.setInformativeText("Unanticipated error caught from URL execution!")
            error_msg.exec()
            return

    def label_clicked(self, obj_name):
        print(f'{obj_name} Hyperlink clicked!')
