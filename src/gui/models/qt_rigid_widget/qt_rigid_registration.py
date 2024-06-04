import traceback

from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.core.app_config import DEFAULT_FD, DETECTORS
from src.gui.models.qt_combo_widget import QtComboBox
from src.gui.models.py_toggle import PyToggle
from src.gui.models.qt_message import QtMessage
from .styles import *
from .qt_non_rigid_registration import NonRigidSettings
from .qt_setting_header import SettingHeader


class RigidSettings(QGroupBox):
    non_rigid_signal = pyqtSignal(bool)
    script_failed = pyqtSignal(str)

    def __init__(
            self,
            title: str = 'Rigid Settings',
            detectors: list = ['BRISK', 'KAZE', 'AKAZE', 'ORB'],
            matching_metric: list = ['Euclidean', 'Jaccard (continuous)'],
            similarity_metric: list = ['Euclidean', 'Matches'],
            color: str = 'black',
            bg_color: str = 'lightgray',
            title_size: int = 16,
            border_radius: int = 8,
            margin_top: int = 21,
            font_size: int = 12,
            parent=None
    ):
        super().__init__()

        if parent != None:
            self.setParent(parent)

        themes = Themes()
        self.themes = themes.items

        groupbox_style = groupbox_template.format(
            color=self.themes['app_color']['main_bg'],
            color_two=self.themes['app_color']['text_color'],
            bg_color=self.themes['app_color']['blue_bg'],
            title_size=title_size,
            border_radius=border_radius,
            margin_top=margin_top,
            font_size=font_size
        )
        self.setStyleSheet(groupbox_style)
        self.setTitle(title)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self._detectors = detectors
        self._matching_metric = matching_metric
        self._similarity_metric = similarity_metric
        self._font_size = font_size
        self._parent = parent

        # *** Setup widget UI ***
        self._setup_widget()

        # *** Connect/Create Signals/Slots ***
        self.non_rigid_chbx.stateChanged.connect(self.perform_non_rigid)

    def _setup_widget(self):
        content_widget = QWidget(self)
        content_widget.setObjectName('contents_widget')

        fd_label = QLabel()
        fd_label.setObjectName('fd_label')
        fd_label.setText('Feature Detector')

        fd_header = SettingHeader(
            label_text='Feature Detector',
            tool_msg='This is the setting for the feature detector.',
            parent=content_widget
        )

        self.feature_detector_combo = QtComboBox(
            bg_color=self.themes["app_color"]["dark_one"],
            text_color=self.themes["app_color"]["text_color"],
            parent=content_widget
        )
        self.feature_detector_combo.setObjectName('feature_detector_combo')
        self.feature_detector_combo.addItems(DETECTORS)
        self.feature_detector_combo.setCurrentText(DEFAULT_FD)
        # self.feature_detector_combo.setCurrentIndex(0)
        self.feature_detector_combo.setFixedHeight(30)
        self.feature_detector_combo.setMinimumWidth(120)

        mm_header = SettingHeader(
            label_text='Feature Matching Metric',
            tool_msg='This is the setting for the feature matching metric.',
            parent=content_widget
        )

        self.matching_metric_combo = QtComboBox(
            bg_color=self.themes["app_color"]["dark_one"],
            text_color=self.themes["app_color"]["text_color"],
            parent=content_widget
        )
        self.matching_metric_combo.setObjectName('matching_metric_combo')
        self.matching_metric_combo.addItems(self._matching_metric)
        self.matching_metric_combo.setCurrentIndex(0)
        self.matching_metric_combo.setFixedHeight(30)
        self.matching_metric_combo.setMinimumWidth(150)

        sm_header = SettingHeader(
            label_text='Similarity Metric',
            tool_msg='This is the setting for the similarity metric.',
            parent=content_widget
        )

        self.similarity_metric_combo = QtComboBox(
            bg_color=self.themes["app_color"]["dark_one"],
            text_color=self.themes["app_color"]["text_color"],
            parent=content_widget
        )
        self.similarity_metric_combo.setObjectName('similarity_metric_combo')
        self.similarity_metric_combo.addItems(self._similarity_metric)
        self.similarity_metric_combo.setCurrentIndex(0)
        self.similarity_metric_combo.setFixedHeight(30)
        self.similarity_metric_combo.setMinimumWidth(120)

        is_header = SettingHeader(
            label_text='Allow Image Scaling',
            tool_msg='This is the setting for image scaling.',
            parent=content_widget
        )

        self.image_scaling_chbx = PyToggle(
            width=34,
            height=20,
            ellipse_y=2,
            bg_color = self.themes['app_color']['text_color'],
            circle_color = self.themes['app_color']['yellow_bg'],
            active_color = self.themes['app_color']['main_bg'],
            parent=content_widget
        )
        self.image_scaling_chbx.setObjectName('image_scaling_chbx')
        self.image_scaling_chbx.setChecked(True)

        mmi_header = SettingHeader(
            label_text='Maximize Mutual Information',
            tool_msg='This is the setting for maximize mutual information.',
            parent=content_widget
        )

        self.mutual_information_chbx = PyToggle(
            width=34,
            height=20,
            ellipse_y=2,
            bg_color = self.themes['app_color']['text_color'],
            circle_color = self.themes['app_color']['yellow_bg'],
            active_color = self.themes['app_color']['main_bg'],
            parent=content_widget
        )
        self.mutual_information_chbx.setObjectName('mutual_information_chbx')
        self.mutual_information_chbx.setChecked(False)

        non_rigid_frame = QFrame(content_widget)
        non_rigid_frame.setObjectName('non_rigid_frame')
        non_rigid_frame.setFrameShape(QFrame.Shape.NoFrame)
        non_rigid_frame.setFrameShadow(QFrame.Shadow.Raised)

        non_rigid_label = QLabel(non_rigid_frame)
        non_rigid_label.setObjectName('non_rigid_label')
        non_rigid_label.setText('Perform Non-Rigid Registration')
        non_rigid_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # non_rigid_label.setStyleSheet('')

        self.non_rigid_chbx = PyToggle(
            width=28,
            height=16,
            ellipse_y=2,
            bg_color = self.themes['app_color']['text_color'],
            circle_color = self.themes['app_color']['yellow_bg'],
            active_color = self.themes['app_color']['main_bg'],
            parent=non_rigid_frame
        )
        self.non_rigid_chbx.setObjectName('non_rigid_chbx')
        self.non_rigid_chbx.setText('Perform Non-Rigid Registration')
        self.non_rigid_chbx.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.non_rigid_chbx.setChecked(False)

        non_rigid_layout = QHBoxLayout(non_rigid_frame)
        non_rigid_layout.setContentsMargins(5, 5, 5, 5)
        non_rigid_layout.setSpacing(15)
        non_rigid_layout.addWidget(non_rigid_label)
        non_rigid_layout.addWidget(self.non_rigid_chbx)

        self.non_rigid_widget = NonRigidSettings(parent=content_widget)
        self.non_rigid_widget.hide()

        content_layout = QGridLayout(content_widget)
        content_layout.setContentsMargins(25, 18, 25, 18)
        content_layout.setSpacing(40)
        content_layout.addWidget(fd_header, 0, 0, 1, 1)
        content_layout.addWidget(self.feature_detector_combo, 0, 2, 1, 2)
        content_layout.addWidget(mm_header, 1, 0, 1, 1)
        content_layout.addWidget(self.matching_metric_combo, 1, 2, 1, 2)
        content_layout.addWidget(sm_header, 2, 0, 1, 1)
        content_layout.addWidget(self.similarity_metric_combo, 2, 2, 1, 2)
        content_layout.addWidget(is_header, 3, 0, 1, 1)
        content_layout.addWidget(self.image_scaling_chbx, 3, 2, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(mmi_header, 4, 0, 1, 1)
        content_layout.addWidget(self.mutual_information_chbx, 4, 2, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(non_rigid_frame, 5, 4, 1, 1)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(15)
        main_layout.addWidget(content_widget)

    def perform_non_rigid(self):
        self.non_rigid_signal.emit(self.non_rigid_chbx.isChecked())

    def import_settings(self, dict: dict):
        pass

    def get_feature_detector(self):
        return self.feature_detector_combo.currentText()
    
    def get_matching_metric(self):
        return self.matching_metric_combo.currentText()
    
    def get_similarity_metric(self):
        return self.similarity_metric_combo.currentText()
    
    def get_image_scaling(self):
        return self.image_scaling_chbx.isChecked()
    
    def get_mutual_information(self):
        return self.mutual_information_chbx.isChecked()

    def get_data(self):
        detector_type = self.get_feature_detector()
        matching_metric_type = self.get_matching_metric()
        similarity_metric_type = self.get_similarity_metric()
        do_image_scaling = self.get_image_scaling()
        maximize_mutual_information = self.get_mutual_information()
        use_non_rigid = self.non_rigid_chbx.isChecked()

        data_dict = {
            'detector': detector_type,
            'matching_metric': matching_metric_type,
            'similarity_metric': similarity_metric_type,
            'image_scaling': do_image_scaling,
            'maximize_mi': maximize_mutual_information,
            'use_non_rigid': use_non_rigid
        }

        return data_dict
