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

        nav_message = """
        <h3>Familiarize Yourself</h3>
        <p>
            The work flow for this app starts with providing whole slide image samples, adjusting settings to incorporate in the valis 
            registration, viewing registration results and finally exporting registered slides to ome.tiff. After initial 
            registration, you can always go back to settings to rerun valis and achieve different results.
        </p>
        <p>
            The left-side panel is constantly visible throughout this application's life cycle and can be expanded via the arrow in the top left corner. 
            From here, you are able to access major work flows from 3 different categories, with sub-menus within each category. 
            The categories are: Home, Registration, and Results.
        </p>
        <p>
            The hamburger icon near the top right corner allows you to access sub-menus within each tabbed-category. This button is disabled for the Home menu
            only, but can be used to switch menus during Registration setup or Results viewing.
        </p><br>

        <h3>Registration Tab</h3>
        <p>
            From the left-side tab menu, click on the "Registration" tab. This workflow is about setting up the Registration process for your
            samples by providing space to supply samples and presenting settings to interact with before execution.
        </p>

        <h4>Sample Upload Menu</h4>
        <p>
            Initially, you will be brought to the "Sample Upload" menu where you will be able to supply sample folders to be registered
            by valis. Using the text entry provided and the file icon, you may search for the sample folder host directory to be used. 
            Then you will click the "update" button to update the directory contents scene to manage which samples will be chosen for this process. 
            This menu can be accessed using the hamburger icon near the top right corner.
        </p>

        <h4>Registration Settings Menu</h4>
        <p>
            The second menu within the Registration tab is the "Registration Settings" menu, which can be accessed via the hamburger icon. 
            This menu presents different settings that can be used within VALIS slide registration. The top-side of this menu offers 
            a text-entry to procvide a desired output directory to store results/process info which is required. By default, there are 
            pre-selected options chosen for each setting category, which can be changed/manipulated by using the toggle button. Use the "Register"
            button to start the VALIS registration process.
        </p><br>

        <h3>Results Tab</h3>
        <p>
            Click the "Results" tab in the left-side panel to access this work flow. This tab deals with viewing and confirming VALIS 
            registration results, while offering an option to export images to a 3D format (ome.tiff).
        </p>

        <h4>Results View Menu</h4>
        <p>
            This is the inital menu that is shown, which allows you to view the registration progress while viewing completed samples in the image viewer 
            located to the right. Clicking on a sample in the table (if it is completed) will present that sample in the image viewer, with a drop 
            down to view different masks.
        </p>

        <h4>Export Results Menu</h4>
        <p>
            The last menu available, here you will find options to format and export your registered slides into a 3D image file of type "ome.tiff".
            A plot will also be available 
        </p>
        """

        nav_text_browser = QTextBrowser()
        nav_text_browser.setObjectName("nav_text_browser")
        nav_text_browser.setHtml(nav_message)
        nav_text_browser.setOpenExternalLinks(False)
        nav_text_browser.setReadOnly(True)
        nav_text_browser.setStyleSheet(f'font-size: 13px; color: {self.themes["app_color"]["text_color"]};')

        navigation_frame.set_expanded_content(nav_text_browser)

        documentation_frame = QtSectionalWidget(
            section_title="Documentation",
            icon_name="internet_icon.svg",
            collapsed_info="Project information and documentation can be found here.",
            expanded_info="Documentation section.",
            icon_size=65,
            parent=sectional_house
        )

        doc_message = """
        <h3>Summary</h3>
        <p>
            This application utilizes valis-wsi and Docker Desktop software, both of which are necessary for this pipeline.
            While valis-wsi software is already packaged with this application, Docker Desktop and the VALIS Docker Image are required
            for execution. Details about these requirements are provided below.
        </p>

        <h3>readthedocs</h3>
        <p>
            This website hosts software documentation. You can find the full technical documentation for 
            valis-wsi <a href="https://valis.readthedocs.io/en/latest/#">here</a>.
        </p>

        <h3>GitHub</h3>
        <p>
            GitHub is a platform for developers to create, store, manage, and share their code. The project 
            repository, including code and files, is available <a href="https://github.com/MathOnco/valis">here</a>, along with brief documentation.
        </p>

        <h3>Docker Desktop</h3>
        <p>
            Docker Desktop is a free tool for creating and managing Docker containers, which are necessary for running VALIS within 
            this application. More information and the download link can be found <a href="https://www.docker.com/products/docker-desktop/">here</a>.
        </p>

        <h3>DockerHub</h3>
        <p>
            While VALIS is available as a downloadable package (valis-wsi), it is also provided as a Docker Image via DockerHub. This image is required
            for proper execution within the application. The VALIS image can be found <a href="https://hub.docker.com/r/cdgatenbee/valis-wsi">here</a>.
        </p>
        """
        
        doc_text_browser = QTextBrowser()
        doc_text_browser.setObjectName("doc_label")
        doc_text_browser.setHtml(doc_message)
        doc_text_browser.setOpenExternalLinks(True)
        doc_text_browser.setReadOnly(True)
        doc_text_browser.setStyleSheet(f'font-size: 13px; color: {self.themes["app_color"]["text_color"]};')

        documentation_frame.set_expanded_content(doc_text_browser)

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
        container_layout.setContentsMargins(10, 25, 10, 10)
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
