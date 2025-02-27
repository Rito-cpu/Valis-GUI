from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.core.keyword_store import *
from src.gui.models import QtExportSampleTable, PyPushButton, PyToggle, QtComboBox
from src.gui.models.qt_spinbox import QtNumEntry


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
        # Create toggle groupbox to make space
        export_sample_table_gb = QGroupBox(self)
        export_sample_table_gb.setObjectName('export_sample_table_gb')
        export_sample_table_gb.setTitle('Export Sample Table')
        export_sample_table_gb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        export_sample_table_gb.setStyleSheet(f"""
            QGroupBox {{
                font-size: 13px;
                background: {self.themes['app_color']['main_bg']};
                border: 1px solid {self.themes['app_color']['text_color']};
                border-radius: 8px;
                margin-top: 9px;
            }}
            QGroupBox::title {{
                color: {self.themes['app_color']['text_color']};
                subcontrol-origin: margin;
                subcontrol-position: top-center;
                padding-left: 7px;
                padding-right: 7px;
            }}
        """)

        table_frame = QFrame(export_sample_table_gb)
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

        export_table_gb_layout = QVBoxLayout(export_sample_table_gb)
        export_table_gb_layout.setObjectName('export_table_gb_layout')
        export_table_gb_layout.setContentsMargins(10, 10, 10, 10)
        export_table_gb_layout.addWidget(table_frame)

        export_options_gb = QGroupBox(self)
        export_options_gb.setObjectName('export_options_gb')
        export_options_gb.setTitle('File Export Options')
        export_options_gb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        export_options_gb.setStyleSheet(f"""
            QGroupBox {{
                font-size: 13px;
                background: {self.themes['app_color']['main_bg']};
                border: 1px solid {self.themes['app_color']['text_color']};
                border-radius: 8px;
                margin-top: 9px;
            }}
            QGroupBox::title {{
                color: {self.themes['app_color']['text_color']};
                subcontrol-origin: margin;
                subcontrol-position: top-center;
                padding-left: 7px;
                padding-right: 7px;
            }}
        """)

        export_options_inner_frame = QFrame(export_options_gb)
        export_options_inner_frame.setObjectName('export_options_inner_frame')
        export_options_inner_frame.setFrameShape(QFrame.Shape.NoFrame)
        export_options_inner_frame.setFrameShadow(QFrame.Shadow.Plain)
        export_options_inner_frame.setStyleSheet(f"""
            QFrame#export_options_inner_frame{{
                background: {self.themes['app_color']['blue_bg']};
                border: none;
                border-radius: 8px;
            }}
        """)

        percentage_frame = QFrame(export_options_inner_frame)
        percentage_frame.setObjectName('percentage_frame')
        percentage_frame.setFrameShape(QFrame.Shape.NoFrame)
        percentage_frame.setFrameShadow(QFrame.Shadow.Raised)

        percentage_label = QLabel(percentage_frame)
        percentage_label.setObjectName('percentage_label')
        percentage_label.setText('Export Size (Percentage):')
        percentage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        percentage_label.setStyleSheet(f'font-size: 12px; color: {self.themes["app_color"]["main_bg"]};')

        percentage_spinbox = QSpinBox(percentage_frame)
        percentage_spinbox.setObjectName('percentage_spinbox')
        percentage_spinbox.setRange(1, 100)
        percentage_spinbox.setValue(25)
        percentage_spinbox.setStyleSheet('background: white; border-color: black; color: black;')
        percentage_spinbox.setFixedHeight(28)

        percentage_layout = QHBoxLayout(percentage_frame)
        percentage_layout.setObjectName('percentage_layout')
        percentage_layout.setContentsMargins(0, 0, 0, 0)
        percentage_layout.setSpacing(15)
        percentage_layout.addWidget(percentage_label, alignment=Qt.AlignmentFlag.AlignLeft)
        percentage_layout.addWidget(percentage_spinbox)

        compression_factor_frame = QFrame(export_options_inner_frame)
        compression_factor_frame.setObjectName('compression_factor_frame')
        compression_factor_frame.setFrameShape(QFrame.Shape.NoFrame)
        compression_factor_frame.setFrameShadow(QFrame.Shadow.Raised)

        compression_factor_label = QLabel(compression_factor_frame)
        compression_factor_label.setObjectName('compression_factor_label')
        compression_factor_label.setText('Compression Factor:')
        compression_factor_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        compression_factor_label.setStyleSheet(f'font-size: 12px; color: {self.themes["app_color"]["main_bg"]};')

        compression_factor_entry = QtNumEntry(parent=compression_factor_frame)
        compression_factor_entry.setObjectName('compression_factor_entry')
        compression_factor_entry.setFixedSize(30, 26)
        compression_factor_entry.setDecimals(2)
        compression_factor_entry.setRange(0, 100)
        compression_factor_entry.setSingleStep(1.0)
        compression_factor_entry.setValue(10)

        compression_factor_layout = QHBoxLayout(compression_factor_frame)
        compression_factor_layout.setObjectName('compression_factor_layout')
        compression_factor_layout.setContentsMargins(0, 0, 0, 0)
        compression_factor_layout.setSpacing(15)
        compression_factor_layout.addWidget(compression_factor_label, alignment=Qt.AlignmentFlag.AlignCenter)
        compression_factor_layout.addWidget(compression_factor_entry)

        channel_frame = QFrame(export_options_inner_frame)
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

        # TODO: add level option (combobox, def=0, precalc values), merge slides (toggle, but only if the images are IF) non-rigid (toggle, default is whatever suer selected when valis was run),
        # dest dir (input to save slides, default can be where they save the registration results)

        export_options_inner_layout = QVBoxLayout(export_options_inner_frame)
        export_options_inner_layout.setObjectName('export_options_inner_layout')
        export_options_inner_layout.setContentsMargins(45, 20, 45, 20)
        export_options_inner_layout.setSpacing(15)
        export_options_inner_layout.addWidget(percentage_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        export_options_inner_layout.addWidget(compression_factor_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        export_options_inner_layout.addWidget(channel_frame, alignment=Qt.AlignmentFlag.AlignCenter)

        export_options_gb_layout = QVBoxLayout(export_options_gb)
        export_options_gb_layout.setObjectName('export_options_gb_layout')
        export_options_gb_layout.setContentsMargins(10, 10, 10, 10)
        export_options_gb_layout.setSpacing(15)
        #export_options_layout.addWidget(percentage_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        #export_options_layout.addWidget(channel_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        export_options_gb_layout.addWidget(export_options_inner_frame)
        export_options_gb.setMinimumWidth(table_frame.sizeHint().width())
        export_options_gb.setMaximumHeight(export_options_gb_layout.sizeHint().height() + 50)

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
        main_layout.addWidget(export_sample_table_gb)
        main_layout.addWidget(export_options_gb)
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
