import os
import json

from src.core.pyqt_core import *
from src.core.app_config import APP_ROOT, SCRIPTS_PATH
from src.core.scripts.valis import completion_checker
from src.core.validation.validate_file import is_valid_json_file, is_existing_path
from src.core.json.json_themes import Themes
from src.core.keyword_store import *
from src.gui.models import QtStatusTable
from src.gui.models.qt_message import QtMessage


class QtResultsArea(QWidget):
    def __init__(
            self,
            parent=None
    ):
        super().__init__()

        if parent is not None:
            self.parent = parent

        self._monitoring_thread = None
        self._table_items = None

        themes = Themes()
        self.themes = themes.items

        # Setup ui for widget
        self._setup_widget()

        # Setup Slots/Signals

    def _setup_widget(self):
        self.sample_table = QtStatusTable(parent=self)
        self.sample_table.setObjectName('sample_table')
        self.sample_table.setMinimumWidth(400)
        self.sample_table.reset_table()

        bar_frame = QFrame(self)
        bar_frame.setObjectName('bar_frame')
        bar_frame.setFrameShape(QFrame.Shape.NoFrame)
        bar_frame.setFrameShadow(QFrame.Shadow.Raised)

        sample_bar_frame = QFrame(bar_frame)
        sample_bar_frame.setObjectName('sample_bar_frame')
        sample_bar_frame.setFrameShape(QFrame.Shape.NoFrame)
        sample_bar_frame.setFrameShadow(QFrame.Shadow.Raised)

        sample_bar_title = QLabel(sample_bar_frame)
        sample_bar_title.setObjectName('sample_bar_title')
        sample_bar_title.setText('Overall Sample Progress')
        sample_bar_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sample_bar_title.setStyleSheet(f'font-size: 13px; color: {self.themes["app_color"]["text_color"]};')

        self.sample_prog_bar = QProgressBar(sample_bar_frame)
        self.sample_prog_bar.setObjectName('sample_prog_bar')
        self.sample_prog_bar.setFormat('%p%')
        self.sample_prog_bar.setRange(0, 1)
        self.sample_prog_bar.setValue(0)
        self.sample_prog_bar.setStyleSheet("""
            QProgressBar {{
                border: 1px solid {color1};
                border-radius: 16px;
                text-align: center;
                background-color: {color2};
                color: {c};
                padding: 8px;
            }}
            QProgressBar::chunk {{
                background-color: {color3};
                border-radius: 6px;
            }}""".format(
                color1=self.themes['app_color']['highlight_bg'],
                color2=self.themes['app_color']['blue_bg'],
                color3=self.themes['app_color']['yellow_bg'],
                c=self.themes['app_color']['text_color']
            )
        )

        self.sample_text = QLabel(sample_bar_frame)
        self.sample_text.setObjectName('sample_text')
        self.sample_text.setText("None")
        self.sample_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sample_text.setStyleSheet(f'font-size: 12px; color: {self.themes["app_color"]["text_color"]};')

        sample_bar_layout = QVBoxLayout(sample_bar_frame)
        sample_bar_layout.setObjectName('sample_bar_layout')
        sample_bar_layout.setContentsMargins(0, 0, 0, 0)
        sample_bar_layout.setSpacing(5)
        sample_bar_layout.addWidget(sample_bar_title, alignment=Qt.AlignmentFlag.AlignCenter)
        sample_bar_layout.addWidget(self.sample_prog_bar)
        sample_bar_layout.addWidget(self.sample_text, alignment=Qt.AlignmentFlag.AlignCenter)
        sample_bar_frame.setFixedHeight(sample_bar_layout.sizeHint().height())

        step_bar_frame = QFrame(bar_frame)
        step_bar_frame.setObjectName('overall_bar_frame')
        step_bar_frame.setFrameShape(QFrame.Shape.NoFrame)
        step_bar_frame.setFrameShadow(QFrame.Shadow.Raised)

        step_bar_title = QLabel(step_bar_frame)
        step_bar_title.setObjectName('overall_bar_title')
        step_bar_title.setText('Current Sample Progress')
        step_bar_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        step_bar_title.setStyleSheet(f'font-size: 13px; color: {self.themes["app_color"]["text_color"]};')

        self.step_prog_bar = QProgressBar(step_bar_frame)
        self.step_prog_bar.setObjectName('overall_prog_bar')
        self.step_prog_bar.setFormat('%p%')
        self.step_prog_bar.setRange(0, 1)
        self.step_prog_bar.setValue(0)
        self.step_prog_bar.setStyleSheet("""
            QProgressBar {{
                border: 1px solid {color1};
                border-radius: 16px;
                text-align: center;
                background-color: {color2};
                color: {c};
                padding: 8px;
            }}
            QProgressBar::chunk {{
                background-color: {color3};
                border-radius: 6px;
            }}""".format(
                color1=self.themes['app_color']['highlight_bg'],
                color2=self.themes['app_color']['blue_bg'],
                color3=self.themes['app_color']['yellow_bg'],
                c=self.themes['app_color']['text_color']
            )
        )

        self.step_text = QLabel(step_bar_frame)
        self.step_text.setObjectName("step_text")
        self.step_text.setText("None")
        self.step_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.step_text.setStyleSheet(f'font-size: 12px; color: {self.themes["app_color"]["text_color"]};')

        step_bar_layout = QVBoxLayout(step_bar_frame)
        step_bar_layout.setObjectName('overall_bar_layout')
        step_bar_layout.setContentsMargins(0, 0, 0, 0)
        step_bar_layout.setSpacing(5)
        step_bar_layout.addWidget(step_bar_title, alignment=Qt.AlignmentFlag.AlignCenter)
        step_bar_layout.addWidget(self.step_prog_bar)
        step_bar_layout.addWidget(self.step_text, alignment=Qt.AlignmentFlag.AlignCenter)
        step_bar_frame.setFixedHeight(step_bar_layout.sizeHint().height())

        bar_layout = QVBoxLayout(bar_frame)
        bar_layout.setObjectName('progress_layout')
        bar_layout.setContentsMargins(5, 5, 5, 5)
        bar_layout.setSpacing(15)
        bar_layout.addWidget(sample_bar_frame)
        bar_layout.addWidget(step_bar_frame)
        bar_frame.setFixedHeight(bar_layout.sizeHint().height() + 10)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 60, 0, 70)
        main_layout.setSpacing(15)
        main_layout.addWidget(self.sample_table)
        main_layout.addWidget(bar_frame)

    def create_thread(self):
        self._monitoring_thread = completion_checker.ValisMonitoringThread(
            self.dst_dir,
            self.steps_dict,
            self.sample_list
        )
        self._monitoring_thread.step_num_signal.connect(self.update_step_bar)
        self._monitoring_thread.step_text_signal.connect(self.update_step_text)
        self._monitoring_thread.sample_num_signal.connect(self.update_sample_bar)
        self._monitoring_thread.sample_text_signal.connect(self.update_sample_text)
        self._monitoring_thread.finished.connect(self.finish_bars)
        self._monitoring_thread.start()

    def update_step_bar(self, step_val):
        if step_val == self.steps_max_range:
            self.sample_table.update_sample_status(self.previous_sample, COMPLETE_S)
        self.step_prog_bar.setValue(step_val)

    def update_step_text(self, step_text):
        self.step_text.setText(f"Step: {step_text}")

    def update_sample_bar(self, sample_val):
        self.sample_prog_bar.setValue(sample_val)

    def update_sample_text(self, sample_text):
        if self.previous_sample is None or self.previous_sample != sample_text:
            self.previous_sample = sample_text
            self.sample_table.update_sample_status(sample_text, PROCESSING_S)
        #elif self.previous_sample != sample_text:
        #    self.sample_table.update_sample_status(sample_text, PROCESSING_S)
        #    self.previous_sample = sample_text
        self.sample_text.setText(f"Sample: {sample_text}")

    def finish_bars(self):
        self.sample_prog_bar.setValue(self.sample_max_range)
        self.sample_text.setText("Step: Done")
        self.step_prog_bar.setValue(self.steps_max_range)
        self.step_text.setText("Step: Done")

    def process_terminated(self):
        self._monitoring_thread.finished.disconnect(self.finish_bars)
        self._monitoring_thread.terminate()
        self.sample_table.reset_table()
        self.clear()

        self.sample_text.setText('Sample: Process Canceled')
        self.step_text.setText('Step: Process Canceled')

    def prepare_data(self):
        self.clear()
        self.dst_dir, self.steps_dict, self.sample_list = self.gather_file_data()

        self.step_prog_bar.setRange(0, self.steps_max_range)
        self.step_prog_bar.setValue(1)

        self.sample_prog_bar.setRange(0, self.sample_max_range)
        self.sample_prog_bar.setValue(1)

        self.fill_table()

    def clear(self):
        self.step_prog_bar.setRange(0, 1)
        self.step_prog_bar.setValue(0)
        self.step_text.setText("None")

        self.sample_prog_bar.setRange(0, 1)
        self.sample_prog_bar.setValue(0)
        self.sample_text.setText("None")

        self._monitoring_thread = None
        self._table_items = None
        self.dst_dir = None
        self.steps_dict = None
        self.sample_list = None
        self.previous_sample = None

    def gather_file_data(self):
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
        error_msg.setIcon(QMessageBox.Icon.Warning)
        
        output_dir = os.path.join(APP_ROOT, *["src", "core", "output", "states"])
        if not is_existing_path(output_dir):
            error_msg.setText('Error: output directory not found!')
            error_msg.setDetailedText(f'The directory \"src/core/output/states\" is not found in the project tree. Please create the missing directories to continue.')
            error_msg.exec()
            return

        f = open(os.path.join(output_dir, "user_settings.json"))
        if f:
            reader = json.load(f)["user_selections"]
            do_rigid, do_micro, do_non_rigid = reader["do_rigid"], reader["micro_rigid_registrar_cls"], reader["non_rigid_registrar_cls"]
            dst_dir = reader["dst_dir"]
        else:
            error_msg.setText('Error: Registration settings file not found!')
            error_msg.setDetailedText(f'The file \"user_settings.json\" is not found in the \"src/core/output/states\" directory. The file is required to process samples, please create this file by submitting the registration settings.')
            error_msg.exec()
            return

        f = open(os.path.join(output_dir, "sample.json"))
        if f:
            reader: dict
            reader = json.load(f)
            f.close()
            reader.pop("src_dir", None)
            sample_list = list(reader.keys())
            self._table_items = reader
            self.sample_max_range = len(sample_list)
        else:
            error_msg.setText('Error: Submitted samples file was not found!')
            error_msg.setDetailedText(f'The file \"sample.json\" is not found in the \"src/core/output/states\" directory. The file is required to locate and select samples, please create this file by completing the sample upload process.')
            error_msg.exec()
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

    def fill_table(self):
        if self._table_items:
            self.sample_table.set_data(self._table_items)
