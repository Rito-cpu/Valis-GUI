from src.core.pyqt_core import *


class HyperlinkLabel(QLabel):
    clicked = pyqtSignal(str)

    def __init__(
        self,
        text: str,
        font_size: int = 11,
        font_color: str = "blue",
        underline: bool = True,
        italicized: bool = True,
        parent=None
    ):
        super().__init__()

        if parent is not None:
            self.parent = parent

        self._text = text
        self._font_size = font_size
        self._font_color = font_color
        self._underline = 'underline' if underline else 'none'
        self._italicized = 'italic' if italicized else 'none'

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"""
            QLabel{{
                background: none;
                border: none;
                color: {self._font_color};
                font-size: {self._font_size}px;
                font-style: {self._italicized};
                text-decoration: {self._underline};
            }}
        """)

    def setHyperLink(self, new_link: str):
        self.setText(f"<a href='{new_link}'>{self._text}</a>")

    def mousePressEvent(self, event):
        self.clicked.emit(self.objectName())
        return super().mousePressEvent(event)
