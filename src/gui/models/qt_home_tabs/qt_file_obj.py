import pathlib

from src.core.app_config import APP_ROOT
from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.core.image_functions import Functions
from src.gui.models.py_push_button import PyPushButton
from src.gui.models.py_title_bar.py_title_button import PyTitleButton


class QtFileWidget(QWidget):
    def __init__(
        self,
        file_name: str,
        icon_file: str = "icon_file.svg",
        icon_remove: str = "icon_remove.svg",
        font_size: int = 13,
        parent=None
    ):
        super().__init__()
        if parent is not None:
            self.setParent(parent)

        themes = Themes()
        self.themes = themes.items

        self._file_name = file_name
        self._icon_file_path = Functions.set_svg_icon(icon_file)
        self._icon_remove_path = Functions.set_svg_icon(icon_remove)
        self._font_size = font_size

        self._setup_widget()

    def _setup_widget(self):
        """
        1. File Icon
        2. File name
        3. File type
        4. File delete icon
        5. Object pathlib variable
        6. File validation method (return either sample or user settings type)

        self._icon_path = Functions.set_svg_icon(icon_path)
        # DRAW BG BLUE
        p.setBrush(QColor(self._context_color))
        p.drawRoundedRect(rect_blue, 8, 8)

        # BG INSIDE
        p.setBrush(QColor(self._bg_one))
        p.drawRoundedRect(rect_inside_active, 8, 8)

        # DRAW ACTIVE
        icon_path = self._icon_active_menu
        icon_path = os.path.abspath(os.path.join(APP_ROOT, icon_path))
        self._set_icon_color = self._icon_color_active
        self.icon_active(p, icon_path, self.width())

        # DRAW TEXT
        p.setPen(QColor(self._set_text_active))
        p.drawText(rect_text, Qt.AlignmentFlag.AlignCenter, self.text())
        # TODO: Switch AlignCenter back to AlignVCenter

        # DRAW ICONS
        self.icon_paint(p, self._icon_path, rect_icon, self._set_icon_color)
        """
        outer_frame = QFrame(self)
        outer_frame.setObjectName("outer_frame")
        outer_frame.setFrameShape(QFrame.Shape.NoFrame)
        outer_frame.setFrameShadow(QFrame.Shadow.Plain)
        outer_frame.setStyleSheet(f"""
            QFrame#outer_frame{{
                border-radius: 8px;
                background: {self.themes['app_color']['main_bg']};
                border: 1px solid black;
            }}
        """)

        inner_frame = QFrame(outer_frame)
        inner_frame.setObjectName("inner_frame")
        inner_frame.setFrameShape(QFrame.Shape.NoFrame)
        inner_frame.setFrameShadow(QFrame.Shadow.Plain)

        file_frame = QFrame(inner_frame)
        file_frame.setObjectName('file_frame')
        file_frame.setFrameShape(QFrame.Shape.NoFrame)
        file_frame.setFrameShadow(QFrame.Shadow.Plain)
        #file_frame.setFixedSize(QSize(15, 15))

        file_logo = QSvgWidget(self._icon_file_path)
        file_logo.setFixedSize(QSize(20, 21))

        file_layout = QVBoxLayout(file_frame)
        file_layout.setContentsMargins(0, 0, 0, 0)
        file_layout.addWidget(file_logo, Qt.AlignmentFlag.AlignCenter, Qt.AlignmentFlag.AlignCenter)

        file_label = QLabel(inner_frame)
        file_label.setObjectName('file_label')
        file_label.setText(self._file_name)
        file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        file_label.setStyleSheet(f"color: {self.themes['app_color']['text_color']}; font-size: {self._font_size}px;")

        remove_bttn = PyPushButton(
            text=None,
            radius=0,
            color=self.themes["app_color"]["main_bg"],
            bg_color=self.themes["app_color"]["main_bg"],
            bg_color_hover=self.themes["app_color"]["main_bg"],
            bg_color_pressed=self.themes["app_color"]["main_bg"],
            font_size=16,
            parent=inner_frame
        )
        remove_bttn.setObjectName("remove_bttn")
        remove_bttn.setIcon(QIcon(self._icon_remove_path))
        remove_bttn.setFixedSize(23, 23)
        remove_bttn.setIconSize(QSize(23, 23))

        inner_layout = QHBoxLayout(inner_frame)
        inner_layout.setSpacing(10)
        inner_layout.setContentsMargins(10, 5, 10, 5)
        inner_layout.addWidget(file_frame)
        inner_layout.addWidget(file_label)
        inner_layout.addWidget(remove_bttn)

        outer_layout = QVBoxLayout(outer_frame)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addWidget(inner_frame)
        outer_frame.setFixedSize(inner_layout.sizeHint().width() + 7, inner_layout.sizeHint().height() + 5)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(outer_frame)
