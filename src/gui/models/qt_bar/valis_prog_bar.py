import os
import json
from src.core.pyqt_core import *
from src.core.app_config import APP_ROOT, SCRIPTS_PATH
from src.core.json.json_themes import Themes
from src.core.scripts.valis import completion_checker
from src.core.validation import is_valid_json_file, is_existing_path


class ValisBar(QWidget):
    def __init__(
        self,
        path: str = None,
        steps_dict: dict = None,
        sample_list: list = None,
        parent=None
    ):
        super().__init__()

        if parent is not None:
            self.setParent(parent)

        #self._path = path
        #self._steps_dict = steps_dict
        #self._sample_list = sample_list
        #self._range_max = len(steps_dict) + 2

        themes = Themes()
        self.themes = themes.items

        self.dst_dir, self.steps_dict, self.sample_list = self.gather_file_data()

        self._setup_widget()

    def _setup_widget(self):
        content_frame = QFrame(self)
        content_frame.setObjectName('content_frame')
        content_frame.setFrameShape(QFrame.Shape.NoFrame)
        content_frame.setFrameShadow(QFrame.Shadow.Plain)

        self.process_progress_bar = QProgressBar(content_frame)
        self.process_progress_bar.setObjectName('process_progress_bar')
        self.process_progress_bar.setTextVisible(True)
        self.process_progress_bar.setRange(0, self.steps_max_range)
        self.process_progress_bar.setValue(1)
        self.step_text = QLabel(content_frame)
        self.step_text.setText('None')

        self.sample_bar = QProgressBar(content_frame)
        self.sample_bar.setObjectName('sample_bar')
        self.sample_bar.setTextVisible(True)
        self.sample_bar.setRange(0, self.sample_max_range)
        self.sample_bar.setValue(1)

        self.sample_text = QLabel(content_frame)
        self.sample_text.setText('None')

        content_layout = QVBoxLayout(content_frame)
        content_layout.setObjectName('content_layout')
        content_layout.setContentsMargins(5, 5, 5, 5)
        content_layout.setSpacing(5)
        content_layout.addWidget(self.process_progress_bar)
        content_layout.addWidget(self.step_text, alignment=Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.sample_bar)
        content_layout.addWidget(self.sample_text, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout = QVBoxLayout(self)
        main_layout.setObjectName('main_layout')
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(content_frame)

    def create_thread(self):
        self.my_thread = completion_checker.ValisMonitoringThread(
            self.dst_dir,
            self.steps_dict,
            self.sample_list
        )
        self.my_thread.step_num_signal.connect(self.update_step_bar)
        self.my_thread.step_text_signal.connect(self.update_step_text)
        self.my_thread.sample_num_signal.connect(self.update_sample_bar)
        self.my_thread.sample_text_signal.connect(self.update_sample_text)
        self.my_thread.start()

    def update_step_bar(self, step_val):
        self.process_progress_bar.setValue(step_val)

    def update_step_text(self, step_text):
        self.step_text.setText(f"Step: {step_text}")

    def update_sample_bar(self, sample_val):
        self.sample_bar.setValue(sample_val)

    def update_sample_text(self, sample_text):
        self.sample_text.setText(f"Sample: {sample_text}")

    def gather_file_data(self):
        output_dir = os.path.join(APP_ROOT, *["src", "core", "output", "states"])
        if not is_existing_path(output_dir):
            print("Error: output_dir not defined!")
            return

        f = open(os.path.join(output_dir, "user_settings.json"))
        if f:
            reader = json.load(f)["user_selections"]
            do_rigid, do_micro, do_non_rigid = reader["do_rigid"], reader["micro_rigid_registrar_cls"], reader["non_rigid_registrar_cls"]
            dst_dir = reader["dst_dir"]
        else:
            # TODO: Create error box message
            print("Error: user_settings.json not found!")
            return

        f = open(os.path.join(output_dir, "sample.json"))
        if f:
            reader = json.load(f)
            sample_list = list(reader.keys())
            f.close()
            if sample_list[0] == "src_dir":
                sample_list = sample_list[1:]
            self.sample_max_range = len(sample_list)
        else:
            print("Error: sample.json not found!")
            return

        del reader

        # create a dictionary of steps to be passed into the progress bar. This will determine how many steps
        # are given to the progress bar on initialization.
        steps_dict = {
            "rigid": do_rigid, 
            "micro_rigid": do_micro,
            "non_rigid": do_non_rigid
        }

        for key in list(steps_dict.keys()):
            if steps_dict[key] is False or steps_dict[key] is None:
                del steps_dict[key]

        self.steps_max_range = len(steps_dict) + 2

        return dst_dir, steps_dict, sample_list
