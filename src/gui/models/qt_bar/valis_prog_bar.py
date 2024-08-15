from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.core.scripts.valis import completion_checker


class ValisBar(QWidget):
    def __init__(
        self,
        path: str,
        steps_dict: dict,
        sample_list: list,
        parent=None
    ):
        super().__init__()

        if parent is not None:
            self.setParent(parent)

        self._path = path
        self._steps_dict = steps_dict
        self._sample_list = sample_list
        self._range_max = len(steps_dict) + 2

        themes = Themes()
        self.themes = themes.items

        self._setup_widget()

    def _setup_widget(self):
        content_frame = QFrame(self)
        content_frame.setObjectName('content_frame')
        content_frame.setFrameShape(QFrame.Shape.NoFrame)
        content_frame.setFrameShadow(QFrame.Shadow.Plain)

        self.process_progress_bar = QProgressBar(content_frame)
        self.process_progress_bar.setObjectName('process_progress_bar')
        self.process_progress_bar.setTextVisible(True)
        self.process_progress_bar.setRange(0, self._range_max)
        self.process_progress_bar.setValue(0)
        #self.process_progress_bar.setStyleSheet(f"""
        #    QProgressBar{{
        #        background: white
        #    }}""")

        content_layout = QVBoxLayout(content_frame)
        content_layout.setObjectName('content_layout')
        content_layout.setContentsMargins(5, 5, 5, 5)
        content_layout.setSpacing(5)
        content_layout.addWidget(self.process_progress_bar)

        main_layout = QVBoxLayout(self)
        main_layout.setObjectName('main_layout')
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(content_frame)

    def create_thread(self):
        self.my_thread = completion_checker.Thread(
            self._path,
            self._steps_dict,
            self._sample_list
        )
        self.my_thread.dir_change.connect(self.advance)
        self.my_thread.start()

    def advance(self, new_value):
        self.process_progress_bar.setValue(new_value)
