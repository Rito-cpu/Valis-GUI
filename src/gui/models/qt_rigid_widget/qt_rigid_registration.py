from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.core.app_config import DEFAULT_FD, DETECTORS, FMM_LIST, SM_LIST, MATCH_FILTERS
from src.core.keyword_store import *
from src.gui.models.qt_combo_widget import QtComboBox
from src.gui.models.py_toggle import PyToggle
from src.gui.models.qt_message import QtMessage
from .styles import *
from .qt_setting_header import SettingHeader


class RigidSettings(QGroupBox):
    script_failed = pyqtSignal(str)

    def __init__(
            self,
            title: str = 'Rigid Settings',
            detectors: list = ['BRISK', 'KAZE', 'AKAZE', 'ORB'],
            matching_metric: list = ['Euclidean', 'Jaccard (continuous)'],
            sorting_metric: list = ['Euclidean', 'Matches'],
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
        self._sorting_metric = sorting_metric
        self._font_size = font_size
        self._parent = parent

        # *** Setup widget UI ***
        self._setup_widget()

    def _setup_widget(self):
        content_widget = QWidget(self)
        content_widget.setObjectName('contents_widget')

        fd_header = SettingHeader(
            label_text='Feature Detector',
            tool_msg=TOOLTIP_FEATURE_DETECTOR,
            parent=content_widget
        )

        self.feature_detector_combo = QtComboBox(
            bg_color=self.themes["app_color"]["dark_one"],
            text_color=self.themes["app_color"]["text_color"],
            parent=content_widget
        )
        self.feature_detector_combo.setObjectName('feature_detector_combo')
        self.feature_detector_combo.setCursor(Qt.CursorShape.PointingHandCursor)
        self.feature_detector_combo.addItems(DETECTORS)
        self.feature_detector_combo.setCurrentText(DEFAULT_FD)
        self.feature_detector_combo.setFixedHeight(30)
        self.feature_detector_combo.setMinimumWidth(120)
        self.feature_detector_combo.setMaximumWidth(175)

        mm_header = SettingHeader(
            label_text='Feature Matching Metric',
            tool_msg=TOOLTIP_FEATURE_MATCHING_METRIC,
            parent=content_widget
        )

        self.matching_metric_combo = QtComboBox(
            bg_color=self.themes["app_color"]["dark_one"],
            text_color=self.themes["app_color"]["text_color"],
            parent=content_widget
        )
        self.matching_metric_combo.setObjectName('matching_metric_combo')
        self.matching_metric_combo.setCursor(Qt.CursorShape.PointingHandCursor)
        self.matching_metric_combo.addItems(FMM_LIST)
        self.matching_metric_combo.setCurrentIndex(0)
        self.matching_metric_combo.setFixedHeight(30)
        self.matching_metric_combo.setMinimumWidth(120)
        self.matching_metric_combo.setMaximumWidth(175)

        sm_header = SettingHeader(
            label_text='Sorting Metric',
            tool_msg=TOOLTIP_SORTING_METRIC,
            parent=content_widget
        )

        self.sorting_metric_combo = QtComboBox(
            bg_color=self.themes["app_color"]["dark_one"],
            text_color=self.themes["app_color"]["text_color"],
            parent=content_widget
        )
        self.sorting_metric_combo.setObjectName('sorting_metric_combo')
        self.sorting_metric_combo.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sorting_metric_combo.addItems(SM_LIST)
        self.sorting_metric_combo.setCurrentIndex(0)
        self.sorting_metric_combo.setFixedHeight(30)
        self.sorting_metric_combo.setMinimumWidth(120)
        self.sorting_metric_combo.setMaximumWidth(175)

        mf_header = SettingHeader(
            label_text='Match Filter',
            tool_msg='This is the setting for the Match Filter.',
            parent=content_widget
        )

        self.match_filter_combo = QtComboBox(
            bg_color=self.themes["app_color"]["dark_one"],
            text_color=self.themes["app_color"]["text_color"],
            parent=content_widget
        )
        self.match_filter_combo.setObjectName('match_filter_combo')
        self.match_filter_combo.setCursor(Qt.CursorShape.PointingHandCursor)
        self.match_filter_combo.addItems(MATCH_FILTERS)
        self.match_filter_combo.setCurrentIndex(0)
        self.match_filter_combo.setFixedHeight(30)
        self.match_filter_combo.setMinimumWidth(120)
        self.match_filter_combo.setMaximumWidth(175)

        toggle_container = QWidget(content_widget)
        toggle_container.setObjectName('toggle_container')

        is_header = SettingHeader(
            label_text='Allow Image Scaling',
            tool_msg='This is the setting for image scaling.',
            parent=toggle_container
        )

        self.image_scaling_toggle = PyToggle(
            width=34,
            height=20,
            ellipse_y=2,
            bg_color = self.themes['app_color']['text_color'],
            circle_color = self.themes['app_color']['yellow_bg'],
            active_color = self.themes['app_color']['main_bg'],
            parent=toggle_container
        )
        self.image_scaling_toggle.setObjectName('image_scaling_toggle')
        self.image_scaling_toggle.setChecked(True)

        mmi_header = SettingHeader(
            label_text='Maximize Mutual Information',
            tool_msg='This is the setting for maximize mutual information.',
            parent=toggle_container
        )

        self.mutual_information_toggle = PyToggle(
            width=34,
            height=20,
            ellipse_y=2,
            bg_color = self.themes['app_color']['text_color'],
            circle_color = self.themes['app_color']['yellow_bg'],
            active_color = self.themes['app_color']['main_bg'],
            parent=toggle_container
        )
        self.mutual_information_toggle.setObjectName('mutual_information_toggle')
        self.mutual_information_toggle.setChecked(False)

        rmr_header = SettingHeader(
            label_text='Rigid Micro-Registration',
            tool_msg=TOOLTIP_MICRO_RIGID_REG,
            parent=toggle_container
        )

        self.rmr_toggle = PyToggle(
            width=34,
            height=20,
            ellipse_y=2,
            bg_color = self.themes['app_color']['text_color'],
            circle_color = self.themes['app_color']['yellow_bg'],
            active_color = self.themes['app_color']['main_bg'],
            parent=toggle_container
        )
        self.rmr_toggle.setObjectName('rmr_toggle')
        self.rmr_toggle.setChecked(False)

        crop_header = SettingHeader(
            label_text='Crop to ROI',
            tool_msg='This is the setting for Crop to ROI.',
            parent=toggle_container
        )

        self.crop_toggle = PyToggle(
            width=34,
            height=20,
            ellipse_y=2,
            bg_color = self.themes['app_color']['text_color'],
            circle_color = self.themes['app_color']['yellow_bg'],
            active_color = self.themes['app_color']['main_bg'],
            parent=toggle_container
        )
        self.crop_toggle.setObjectName('crop_toggle')
        self.crop_toggle.setChecked(True)

        reflections_header = SettingHeader(
            label_text='Check for Reflections',
            tool_msg='This is the setting Check for Reflections.',
            parent=toggle_container
        )

        self.reflections_toggle = PyToggle(
            width=34,
            height=20,
            ellipse_y=2,
            bg_color = self.themes['app_color']['text_color'],
            circle_color = self.themes['app_color']['yellow_bg'],
            active_color = self.themes['app_color']['main_bg'],
            parent=toggle_container
        )
        self.reflections_toggle.setObjectName('reflections_toggle')
        self.reflections_toggle.setChecked(False)

        toggle_layout = QGridLayout(toggle_container)
        toggle_layout.setObjectName('toggle_layout')
        toggle_layout.setContentsMargins(0, 0, 0, 0)
        toggle_layout.setSpacing(25)
        toggle_layout.addWidget(is_header, 0, 0 , 1, 1)
        toggle_layout.addWidget(self.image_scaling_toggle, 0, 2, 1, 2)
        toggle_layout.addWidget(mmi_header, 1, 0, 1, 1)
        toggle_layout.addWidget(self.mutual_information_toggle, 1, 2, 1, 2)
        toggle_layout.addWidget(rmr_header, 2, 0, 1, 1)
        toggle_layout.addWidget(self.rmr_toggle, 2, 2, 1, 2)
        toggle_layout.addWidget(crop_header, 0, 4, 1, 1)
        toggle_layout.addWidget(self.crop_toggle, 0, 6, 1, 2)
        toggle_layout.addWidget(reflections_header, 1, 4, 1, 1)
        toggle_layout.addWidget(self.reflections_toggle, 1, 6, 1, 2)

        content_layout = QGridLayout(content_widget)
        content_layout.setContentsMargins(25, 18, 25, 18)
        content_layout.setSpacing(25)
        content_layout.addWidget(fd_header, 0, 0, 1, 1)
        content_layout.addWidget(self.feature_detector_combo, 0, 2, 1, 1)
        content_layout.addWidget(mm_header, 1, 0, 1, 1)
        content_layout.addWidget(self.matching_metric_combo, 1, 2, 1, 1)
        content_layout.addWidget(sm_header, 2, 0, 1, 1)
        content_layout.addWidget(self.sorting_metric_combo, 2, 2, 1, 1)
        content_layout.addWidget(mf_header, 3, 0, 1, 1)
        content_layout.addWidget(self.match_filter_combo, 3, 2, 1, 1)
        content_layout.addWidget(toggle_container, 4, 0, 1, 4)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(15)
        main_layout.addWidget(content_widget)

    def get_feature_detector(self):
        return self.feature_detector_combo.currentText()
    
    def get_matching_metric(self):
        return self.matching_metric_combo.currentText()
    
    def get_sorting_metric(self):
        return self.sorting_metric_combo.currentText()
    
    def get_match_filter(self):
        return self.match_filter_combo.currentText()

    def get_image_scaling(self):
        return self.image_scaling_toggle.isChecked()
    
    def get_maximize_mutual_information(self):
        return self.mutual_information_toggle.isChecked()
    
    def get_rigid_micro_registration(self):
        return self.rmr_toggle.isChecked()
    
    def get_crop_to_roi(self):
        return self.crop_toggle.isChecked()
    
    def get_check_for_reflections(self):
        return self.reflections_toggle.isChecked()

    def get_data(self):
        detector_type = self.get_feature_detector()
        matching_metric_type = self.get_matching_metric()
        sorting_metric_type = self.get_sorting_metric()
        match_filter = self.get_match_filter()
        do_image_scaling = self.get_image_scaling()
        do_maximize_mutual_information = self.get_maximize_mutual_information()
        do_rigid_micro_registration = self.get_rigid_micro_registration()
        do_crop_to_roi = self.get_crop_to_roi()
        do_check_for_reflections = self.get_check_for_reflections()

        data_dict = {
            FEATURE_DETECTOR_CLS: detector_type,
            SORTING_METRIC: sorting_metric_type,
            MATCH_FILTER_METHOD: match_filter,
            FEATURE_MATCHING_METRIC: matching_metric_type,
            TRANSFORMER_CLS: do_image_scaling,
            AFFINE_OPTIMIZER_CLS: do_maximize_mutual_information,
            MICRO_RIGID_REGISTRAR_CLS: do_rigid_micro_registration,
            CROP_FOR_RIGID_REG: do_crop_to_roi,
            CHECK_FOR_REFLECTIONS: do_check_for_reflections
        }

        return data_dict
