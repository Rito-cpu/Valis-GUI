from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.gui.models.qt_line_button import QtOutputEntry, QtButtonLineEdit
from src.gui.models.py_push_button import PyPushButton

tab_description = '''
<p style=\"text-align: center\">This tab gives the ability to enter valis gui settings that were saved 
from a previous session and run the valis registration software using these entered settings.</p>'''


class SavedSettingsTab(QWidget):
    def __init__(
        self,
        parent=None
    ):
        super().__init__()
        
        if parent is not None:
            self.parent = parent
        
        themes = Themes()
        self.themes = themes.items

        self._setup_widget()

    def _setup_widget(self):
        container_frame = QFrame(self)
        container_frame.setObjectName('container_frame')
        container_frame.setFrameShape(QFrame.Shape.NoFrame)
        container_frame.setFrameShadow(QFrame.Shadow.Plain)

        # TODO: Gotta create:
        #   - Short description DONE
        #   - Entry line widget DONE
        #   - Submit button     DONE
        #   - Found files pop-up window
        #   - Selected files
        #   - Run button

        short_description_frame = QFrame(container_frame)
        short_description_frame.setObjectName('short_description_frame')
        short_description_frame.setFrameShape(QFrame.Shape.NoFrame)
        short_description_frame.setFrameShadow(QFrame.Shadow.Plain)
        short_description_frame.setStyleSheet('QFrame#short_description_frame{border: none;}')
        
        top_label = QLabel(short_description_frame)
        top_label.setObjectName('top_label')
        top_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_label.setText("Already Used VALIS Before?")
        top_label.setStyleSheet('font-weight: bold; font-size: 22px;')

        short_description = QTextEdit(short_description_frame)
        short_description.setObjectName("short_description")
        short_description.setReadOnly(True)
        short_description.setText(tab_description)
        short_description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        short_description.setStyleSheet(f'border: none; background: transparent; font-size: 16px;')
        doc_height = short_description.document().size().height()
        margin_top = short_description.contentsMargins().top()
        margin_bottom = short_description.contentsMargins().bottom()
        # short_description.setFixedHeight(doc_height + margin_top + margin_bottom + 4)
        short_description.setFixedHeight(60)

        short_description_layout = QVBoxLayout(short_description_frame)
        short_description_layout.setObjectName('short_description_layout')
        short_description_layout.setContentsMargins(60, 0, 60, 10)
        short_description_layout.setSpacing(15)
        short_description_layout.addWidget(top_label)
        short_description_layout.addWidget(short_description)
        short_description_frame.setFixedHeight(short_description_layout.sizeHint().height() + 8)

        dir_entry_frame = QFrame(container_frame)
        dir_entry_frame.setObjectName('dir_entry_frame')
        dir_entry_frame.setFrameShape(QFrame.Shape.NoFrame)
        dir_entry_frame.setFrameShadow(QFrame.Shadow.Plain)

        self.settings_dir_entry = QtButtonLineEdit(
            title="Valis Settings",
            title_color=self.themes["app_color"]["text_color"],
            color_three=self.themes['app_color']['blue_bg'],
            top_margin=18,
            parent=dir_entry_frame
        )
        self.settings_dir_entry.setObjectName('settings_dir_entry')
        self.settings_dir_entry.setMaximumWidth(975)

        self.find_settings_bttn = PyPushButton(
            text="Find Settings",
            radius=8,
            color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            font_size=16,
            parent=dir_entry_frame
        )
        self.find_settings_bttn.setObjectName(u"find_settings_bttn")
        self.find_settings_bttn.setFixedHeight(40)
        self.find_settings_bttn.setMaximumWidth(960)

        dir_entry_layout = QGridLayout(dir_entry_frame)
        dir_entry_layout.setObjectName('dir_entry_layout')
        dir_entry_layout.setContentsMargins(40, 10, 40, 10)
        dir_entry_layout.addWidget(self.settings_dir_entry)
        dir_entry_layout.addWidget(self.find_settings_bttn)
        dir_entry_frame.setMaximumHeight(dir_entry_layout.sizeHint().height() + 4)

        # TODO: Create modified results box for found settings

        test_box = self.create_box(container_frame)

        container_layout = QGridLayout(container_frame)
        container_layout.setObjectName('container_layout')
        container_layout.setContentsMargins(10, 25, 10, 10)
        container_layout.setSpacing(5)
        container_layout.addWidget(short_description_frame)
        container_layout.addWidget(dir_entry_frame)
        container_layout.addWidget(test_box)

        main_layout = QVBoxLayout(self)
        main_layout.setObjectName('main_layout')
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container_frame)

    def create_box(self, parent_frame: QFrame):
        groupbox_template = """
            QGroupBox {{
                color: {color};
                background: {bg_color};
                font-size: {title_size}px;
                border: 1px solid black;
                border-radius: {border_radius}px;
                margin-top: {margin_top}px;
            }}
            QGroupBox:title {{
                color: {color_two};
                subcontrol-origin: margin;
                left: 17px;
            }}
        """
        gb_style = groupbox_template.format(
            color=self.themes['app_color']['main_bg'],
            color_two=self.themes['app_color']['text_color'],
            bg_color=self.themes['app_color']['main_bg'],
            title_size=16,
            border_radius=8,
            margin_top=20,
            font_size=13
        )

        main_gb = QGroupBox()
        main_gb.setTitle("Testing")
        main_gb.setStyleSheet(gb_style)

        box_container = QFrame(parent_frame)
        box_container.setObjectName('box_container')
        box_container.setFrameShape(QFrame.Shape.NoFrame)
        box_container.setFrameShadow(QFrame.Shadow.Plain)
        box_container.setStyleSheet(f"""
            QFrame#box_container{{
                background: {self.themes['app_color']['blue_bg']};
                border: none;
                border-radius: 10px;
            }}
        """)

        lab = QLabel(box_container)
        lab.setText('Selected Files')

        box_layout = QVBoxLayout(box_container)
        box_layout.setContentsMargins(10, 10, 10, 10)
        box_layout.setSpacing(5)
        box_layout.addWidget(lab)

        lele = QVBoxLayout(main_gb)
        lele.setContentsMargins(10, 10, 10, 10)
        lele.addWidget(box_container)

        return main_gb
