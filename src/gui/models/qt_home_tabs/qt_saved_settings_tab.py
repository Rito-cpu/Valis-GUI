from src.core.pyqt_core import *
from src.core.json.json_themes import Themes


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

        container_layout = QVBoxLayout(container_frame)
        container_layout.setObjectName('container_layout')
        container_layout.setContentsMargins(5, 5, 5, 5)
        container_layout.setSpacing(5)

        main_layout = QVBoxLayout(self)
        main_layout.setObjectName('main_layout')
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container_frame)

