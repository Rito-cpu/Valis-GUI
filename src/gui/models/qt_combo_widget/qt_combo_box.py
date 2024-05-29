import os

from src.core.pyqt_core import *
from src.core.app_config import IMG_RSC_PATH
from .styles import combo_box_template


class QtComboBox(QComboBox):
    def __init__(self,
                bg_color: str = "black",
                text_color: str = "white",
                parent=None):
        super().__init__()

        if parent != None:
            self.setParent(parent)

        arrow_png = "downloads/white_down_arrow.png"
        arrow_path = os.path.abspath(os.path.join(IMG_RSC_PATH, arrow_png))

        combo_box_style = combo_box_template.format(
            bg=bg_color,
            color=text_color,
            path=arrow_path
        )

        self.setStyleSheet(combo_box_style)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
