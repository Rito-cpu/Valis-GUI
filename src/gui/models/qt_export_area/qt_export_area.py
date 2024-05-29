from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.core.keyword_store import *
from src.gui.models import QtExportSampleTable, PyPushButton, PyToggle, QtComboBox


class QtExportArea(QWidget):
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
        self._select_rigid_bttn.clicked.connect(self.select_all_rigid)
        self._select_non_rigid_bttn.clicked.connect(self.select_all_non_rigid)

    def _setup_widget(self):
        table_frame = QFrame(self)
        table_frame.setObjectName('table_frame')
        table_frame.setFrameShape(QFrame.Shape.NoFrame)
        table_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.export_sample_table = QtExportSampleTable(parent=table_frame)
        self.export_sample_table.setObjectName('export_sample_table')
        self.export_sample_table.setMinimumWidth(500)
        # self.export_sample_table.setMaximumWidth(750)
        self.export_sample_table.fill_table(self._sample_data)

        selection_frame = QFrame(table_frame)
        selection_frame.setObjectName('selection_frame')
        selection_frame.setFrameShape(QFrame.Shape.NoFrame)
        selection_frame.setFrameShadow(QFrame.Shadow.Raised)
        selection_frame.setStyleSheet('QFrame#selection_frame{border: none; background: %s; border-radius: 8px;}' % self.themes['app_color']['blue_bg'])

        select_all_label = QLabel(selection_frame)
        select_all_label.setObjectName('select_all_label')
        select_all_label.setText('Select All:')
        select_all_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        select_all_label.setStyleSheet(f'font-size: 12px; color: {self.themes["app_color"]["main_bg"]};')

        self._select_rigid_bttn = PyPushButton(
            text="Rigid",
            radius=8,
            color=self.themes["app_color"]["text_color"],
            bg_color=self.themes["app_color"]["yellow_bg"],
            bg_color_hover=self.themes["app_color"]["highlight_bg"],
            bg_color_pressed=self.themes["app_color"]["highlight_bg"],
            parent=selection_frame
        )
        self._select_rigid_bttn.setObjectName('_select_rigid_bttn')
        self._select_rigid_bttn.setFixedSize(77, 30)

        self._select_non_rigid_bttn = PyPushButton(
            text="Non-Rigid",
            radius=8,
            color=self.themes["app_color"]["text_color"],
            bg_color=self.themes["app_color"]["yellow_bg"],
            bg_color_hover=self.themes["app_color"]["highlight_bg"],
            bg_color_pressed=self.themes["app_color"]["highlight_bg"],
            highlight=self.themes["app_color"]["green_bg"],
            parent=selection_frame
        )
        self._select_non_rigid_bttn.setObjectName('_select_non_rigid_bttn')
        self._select_non_rigid_bttn.setFixedSize(93, 30)

        selection_layout = QGridLayout(selection_frame)
        selection_layout.setObjectName('selection_layout')
        selection_layout.setContentsMargins(10, 10, 10, 10)
        # selection_layout.setSpacing(75)
        selection_layout.addWidget(select_all_label, 0, 0, 1, 1)
        selection_layout.addWidget(self._select_rigid_bttn, 0, 2, 1, 1)
        selection_layout.addWidget(self._select_non_rigid_bttn, 0, 3, 1, 1)

        table_layout = QVBoxLayout(table_frame)
        table_layout.setObjectName('table_layout')
        table_layout.setContentsMargins(0, 0, 0, 0)
        table_layout.setSpacing(10)
        table_layout.addWidget(self.export_sample_table)
        table_layout.addWidget(selection_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        table_frame.setMaximumHeight(table_layout.sizeHint().height() + 10)

        options_frame = QGroupBox(self)
        options_frame.setTitle('Options')
        general_groupbox = """
            QGroupBox {{
                font-size: {_font_size}px;
                background-color: {_bg_color};
                border: none;
                border-radius: {_border_radius}px;
                margin-top: {_top_margin}px;
                color: {_color};
            }}
            QGroupBox:title {{
                subcontrol-origin: margin;
                left: {_left_margin}px;
            }}
        """.format(
            _font_size=14,
            _bg_color=self.themes['app_color']['blue_bg'],
            _border_radius=13,
            _top_margin=23,
            _left_margin=23,
            _color=self.themes['app_color']['text_color']
        )
        options_frame.setStyleSheet(general_groupbox)

        percentage_frame = QFrame(options_frame)
        percentage_frame.setObjectName('percentage_frame')
        percentage_frame.setFrameShape(QFrame.Shape.NoFrame)
        percentage_frame.setFrameShadow(QFrame.Shadow.Raised)

        percentage_label = QLabel(percentage_frame)
        percentage_label.setObjectName('percentage_label')
        percentage_label.setText('Export Size (Percentage):')
        percentage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        percentage_label.setStyleSheet(f'font-size: 12px; color: {self.themes["app_color"]["main_bg"]};')

        self.percentage_combo = QtComboBox(
            bg_color=self.themes["app_color"]["yellow_bg"],
            text_color=self.themes["app_color"]["text_color"],
            parent=percentage_frame
        )
        self.percentage_combo.addItems(['Test One', 'Test Two', 'Test Three'])
        self.percentage_combo.setFixedHeight(30)
        self.percentage_combo.setMinimumWidth(120)

        percentage_layout = QHBoxLayout(percentage_frame)
        percentage_layout.setObjectName('percentage_layout')
        percentage_layout.setContentsMargins(0, 0, 0, 0)
        percentage_layout.setSpacing(15)
        percentage_layout.addWidget(percentage_label, alignment=Qt.AlignmentFlag.AlignLeft)
        percentage_layout.addWidget(self.percentage_combo)

        channel_frame = QFrame(options_frame)
        channel_frame.setObjectName('channel_frame')
        channel_frame.setFrameShape(QFrame.Shape.NoFrame)
        channel_frame.setFrameShadow(QFrame.Shadow.Raised)

        channel_label = QLabel(channel_frame)
        channel_label.setObjectName('channel_label')
        channel_label.setText('Merge Channels:')
        channel_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        channel_label.setStyleSheet(f'font-size: 12px; color: {self.themes["app_color"]["main_bg"]};')

        self._merge_channels_toggle = PyToggle(
            width=34,
            height=20,
            ellipse_y=2,
            bg_color = self.themes['app_color']['text_color'],
            circle_color = self.themes['app_color']['yellow_bg'],
            active_color = self.themes['app_color']['main_bg'],
            parent=channel_frame
        )
        self._merge_channels_toggle.setObjectName('_merge_channels_toggle')
        self._merge_channels_toggle.setChecked(False)

        channel_layout = QHBoxLayout(channel_frame)
        channel_layout.setObjectName('channel_layout')
        channel_layout.setContentsMargins(0, 0, 0, 0)
        channel_layout.setSpacing(15)
        channel_layout.addWidget(channel_label, alignment=Qt.AlignmentFlag.AlignLeft)
        channel_layout.addWidget(self._merge_channels_toggle)

        options_layout = QVBoxLayout(options_frame)
        options_layout.setObjectName('options_layout')
        options_layout.setContentsMargins(45, 20, 45, 20)
        options_layout.setSpacing(15)
        options_layout.addWidget(percentage_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        options_layout.addWidget(channel_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        options_frame.setMinimumWidth(table_frame.sizeHint().width())
        options_frame.setMaximumHeight(options_layout.sizeHint().height() + 50)

        self.bar_frame = QFrame(self)
        self.bar_frame.setObjectName('bar_frame')
        self.bar_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.bar_frame.setFrameShadow(QFrame.Shadow.Raised)

        sample_bar_frame = QFrame(self.bar_frame)
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

        overall_bar_frame = QFrame(self.bar_frame)
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

        bar_layout = QVBoxLayout(self.bar_frame)
        bar_layout.setObjectName('progress_layout')
        bar_layout.setContentsMargins(5, 5, 5, 5)
        bar_layout.setSpacing(15)
        bar_layout.addWidget(sample_bar_frame)
        bar_layout.addWidget(overall_bar_frame)
        self.bar_frame.setFixedHeight(bar_layout.sizeHint().height() + 10)

        self.bar_frame.hide()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(45)
        main_layout.addWidget(table_frame)
        main_layout.addWidget(options_frame)
        main_layout.addWidget(self.bar_frame)
        main_layout.addStretch(1)

    def show_bar_frame(self):
        self.bar_frame.show()

    def hide_bar_frame(self):
        self.bar_frame.hide()

    def select_all_rigid(self):
        self.export_sample_table.select_all(RIGID_KEY)

    def select_all_non_rigid(self):
        self.export_sample_table.select_all(NON_RIGID_KEY)
