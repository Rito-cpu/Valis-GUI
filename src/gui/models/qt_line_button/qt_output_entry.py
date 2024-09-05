from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from .qt_button_line_edit import QtButtonLineEdit
from src.gui.models import PyPushButton
from src.gui.models.qt_marquee import QtMarqueeLabel


class QtOutputEntry(QWidget):
    directory_changed = pyqtSignal(QWidget)

    def __init__(
        self, 
        font_size: int = 13, 
        parent = None
    ):
        super().__init__()

        if parent is not None:
            self.setParent(parent)

        themes = Themes()
        self.themes = themes.items
        self._font_size = font_size

        self._setup_widget()

        self.submit_bttn.clicked.connect(self.submit_bttn_clicked)

    def _setup_widget(self):
        container_frame = QFrame(self)
        container_frame.setObjectName('container_frame')
        container_frame.setFrameShape(QFrame.Shape.NoFrame)
        container_frame.setFrameShadow(QFrame.Shadow.Plain)
        container_frame.setStyleSheet(f"""
            QFrame#container_frame {{
                border: 2px solid #eeeeee;
                border-radius: 8px;
            }}
        """)

        entry_row_frame = QFrame(container_frame)
        entry_row_frame.setObjectName('entry_row_frame')
        entry_row_frame.setFrameShape(QFrame.Shape.NoFrame)
        entry_row_frame.setFrameShadow(QFrame.Shadow.Plain)

        self.output_dir_entry = QtButtonLineEdit(
            title="Output Directory",
            title_color=self.themes["app_color"]["text_color"],
            color_three=self.themes['app_color']['blue_bg'],
            top_margin=18,
            parent=entry_row_frame
        )
        self.output_dir_entry.setObjectName('output_directory')
        self.output_dir_entry.setMinimumWidth(475)

        bttn_container = QFrame(container_frame)
        bttn_container.setObjectName('bttn_container')
        bttn_container.setFrameShape(QFrame.Shape.NoFrame)
        bttn_container.setFrameShadow(QFrame.Shadow.Plain)

        self.submit_bttn = PyPushButton(
            text="Submit",
            radius=8,
            color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            parent=bttn_container
        )
        self.submit_bttn.setObjectName('dir_submit_bttn')
        self.submit_bttn.setMinimumSize(78, 31)

        bttn_layout = QVBoxLayout(bttn_container)
        bttn_layout.setObjectName('bttn_layout')
        bttn_layout.setContentsMargins(0, 17, 3, 0)
        bttn_layout.addWidget(self.submit_bttn)

        entry_row_layout = QHBoxLayout(entry_row_frame)
        entry_row_layout.setObjectName('entry_row_layout')
        entry_row_layout.setContentsMargins(0, 0, 0, 0)
        entry_row_layout.setSpacing(15)
        entry_row_layout.addWidget(self.output_dir_entry)
        entry_row_layout.addWidget(bttn_container)

        marquee_frame = QFrame(container_frame)
        marquee_frame.setObjectName('marquee_frame')
        marquee_frame.setFrameShape(QFrame.Shape.NoFrame)
        marquee_frame.setFrameShadow(QFrame.Shadow.Plain)
        marquee_frame.setStyleSheet(f"""
            QFrame#marquee_frame{{
                background-color: {self.themes["app_color"]["blue_bg"]};
                border-radius: 6px;
            }}
        """)

        header_label = QLabel(marquee_frame)
        header_label.setObjectName('header_label')
        header_label.setText('Output Directory:')
        header_label.setStyleSheet(f'color: {self.themes["app_color"]["main_bg"]}; font-size: {self._font_size}px;')

        self.dir_marquee_label = QtMarqueeLabel(
            color=self.themes["app_color"]["main_bg"],
            parent=marquee_frame
        )
        self.dir_marquee_label.setObjectName('dir_marquee_label')
        self.dir_marquee_label.setMinimumWidth(415)
        self.dir_marquee_label.setText('None')

        marquee_layout = QHBoxLayout(marquee_frame)
        marquee_layout.setObjectName('marquee_layout')
        marquee_layout.setContentsMargins(10, 5, 10, 5)
        marquee_layout.setSpacing(10)
        marquee_layout.addWidget(header_label, alignment=Qt.AlignmentFlag.AlignLeft)
        marquee_layout.addWidget(self.dir_marquee_label, alignment=Qt.AlignmentFlag.AlignLeft)
        marquee_layout.addStretch(1)

        container_layout = QVBoxLayout(container_frame)
        container_layout.setObjectName('container_layout')
        container_layout.setContentsMargins(10, 10, 10, 10)
        container_layout.setSpacing(5)
        container_layout.addWidget(entry_row_frame)
        container_layout.addWidget(marquee_frame)

        main_layout = QVBoxLayout(self)
        main_layout.setObjectName('main_layout')
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container_frame)

    def get_text(self):
        return self.output_dir_entry.text()

    def set_text(self, new_text: str):
        self.dir_marquee_label.setText(new_text)

    def submit_bttn_clicked(self):
        self.directory_changed.emit(self)
