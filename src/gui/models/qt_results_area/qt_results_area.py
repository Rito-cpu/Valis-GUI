from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.core.keyword_store import *
from src.gui.models import QtExportSampleTable, PyPushButton, PyToggle, QtComboBox, QtStatusTable


class QtResultsArea(QWidget):
    def __init__(
            self,
            sample_data,
            parent=None
    ):
        super().__init__()

        if parent is not None:
            self.parent = parent

        self._sample_data = sample_data

        themes = Themes()
        self.themes = themes.items

        # Setup ui for widget
        self._setup_widget()

        # Setup Slots/Signals

    def _setup_widget(self):
        self.sample_table = QtStatusTable(parent=self)
        self.sample_table.setObjectName('sample_table')
        self.sample_table.setMinimumWidth(400)
        self.sample_table.fill_table(self._sample_data)

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
        sample_bar_title.setText('Current Sample')
        sample_bar_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sample_bar_title.setStyleSheet('font-size: 12px;')

        self.sample_prog_bar = QProgressBar(sample_bar_frame)
        self.sample_prog_bar.setObjectName('sample_prog_bar')
        self.sample_prog_bar.setFormat('%p%')
        self.sample_prog_bar.setRange(0, 100)
        self.sample_prog_bar.setValue(50)
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

        sample_bar_layout = QVBoxLayout(sample_bar_frame)
        sample_bar_layout.setObjectName('sample_bar_layout')
        sample_bar_layout.setContentsMargins(0, 0, 0, 0)
        sample_bar_layout.setSpacing(5)
        sample_bar_layout.addWidget(sample_bar_title, alignment=Qt.AlignmentFlag.AlignCenter)
        sample_bar_layout.addWidget(self.sample_prog_bar)
        sample_bar_frame.setFixedHeight(sample_bar_layout.sizeHint().height())

        overall_bar_frame = QFrame(bar_frame)
        overall_bar_frame.setObjectName('overall_bar_frame')
        overall_bar_frame.setFrameShape(QFrame.Shape.NoFrame)
        overall_bar_frame.setFrameShadow(QFrame.Shadow.Raised)

        overall_bar_title = QLabel(overall_bar_frame)
        overall_bar_title.setObjectName('overall_bar_title')
        overall_bar_title.setText('Overall Samples')
        overall_bar_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        overall_bar_title.setStyleSheet('font-size: 12px;')

        self.overall_prog_bar = QProgressBar(overall_bar_frame)
        self.overall_prog_bar.setObjectName('overall_prog_bar')
        self.overall_prog_bar.setFormat('%p%')
        self.overall_prog_bar.setRange(0, 3)
        self.overall_prog_bar.setValue(2)
        self.overall_prog_bar.setStyleSheet("""
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

        overall_bar_layout = QVBoxLayout(overall_bar_frame)
        overall_bar_layout.setObjectName('overall_bar_layout')
        overall_bar_layout.setContentsMargins(0, 0, 0, 0)
        overall_bar_layout.setSpacing(5)
        overall_bar_layout.addWidget(overall_bar_title, alignment=Qt.AlignmentFlag.AlignCenter)
        overall_bar_layout.addWidget(self.overall_prog_bar)
        overall_bar_frame.setFixedHeight(overall_bar_layout.sizeHint().height())

        bar_layout = QVBoxLayout(bar_frame)
        bar_layout.setObjectName('progress_layout')
        bar_layout.setContentsMargins(5, 5, 5, 5)
        bar_layout.setSpacing(15)
        bar_layout.addWidget(sample_bar_frame)
        bar_layout.addWidget(overall_bar_frame)
        bar_frame.setFixedHeight(bar_layout.sizeHint().height() + 10)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 60, 0, 70)
        main_layout.setSpacing(15)
        main_layout.addWidget(self.sample_table)
        main_layout.addWidget(bar_frame)

    def fill_table(self, table_data):
        if table_data:
            self.sample_table.fill_table(table_data)
