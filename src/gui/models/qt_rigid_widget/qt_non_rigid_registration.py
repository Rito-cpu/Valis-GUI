from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.core.app_config import NONRIGID_REGISTRARS
from src.core.keyword_store import *
from src.gui.models.qt_combo_widget import *
from src.gui.models.py_toggle import PyToggle
from .styles import *
from .qt_setting_header import SettingHeader


class NonRigidSettings(QGroupBox):
    def __init__(
            self,
            non_rigid_methods: list = [],
            title: str = 'Non-Rigid Registration',
            title_size: int = 16,
            font_size: int = 12,
            margin_top: int = 21,
            border_radius: int = 8,
            color: str = 'black',
            bg_color: str = 'lightgray',
            parent = None
    ):
        super().__init__()

        if parent != None:
            self.setParent(parent)

        self.setTitle(title)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self._non_rigid_methods = non_rigid_methods

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

        self._setup_widget()

        self.non_rigid_chbx.checkStateChanged.connect(self.toggle_settings)

    def _setup_widget(self):
        content_widget = QWidget(self)
        content_widget.setObjectName('content_widget')

        non_rigid_header = SettingHeader(
            label_text='Non-Rigid Registration',
            tool_msg=TOOLTIP_NON_RIGID_REG,
            parent=content_widget
        )

        self.non_rigid_combo = QtComboBox(
            bg_color=self.themes["app_color"]["dark_one"],
            text_color=self.themes["app_color"]["text_color"],
            parent=content_widget
        )
        self.non_rigid_combo.setObjectName('non_rigid_combo')
        self.non_rigid_combo.addItems(NONRIGID_REGISTRARS)
        self.non_rigid_combo.setCurrentIndex(0)
        self.non_rigid_combo.setFixedHeight(30)
        self.non_rigid_combo.setMinimumWidth(120)

        non_rigid_frame = QFrame(content_widget)
        non_rigid_frame.setObjectName('non_rigid_frame')
        non_rigid_frame.setFrameShape(QFrame.Shape.NoFrame)
        non_rigid_frame.setFrameShadow(QFrame.Shadow.Raised)
        # non_rigid_frame.setStyleSheet('QFrame#non_rigid_frame {background: white; border-radius: 8px;}')

        non_rigid_label = QLabel(non_rigid_frame)
        non_rigid_label.setObjectName('non_rigid_label')
        non_rigid_label.setText('Perform Non-Rigid Registration')
        non_rigid_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

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
        # self.non_rigid_chbx.setText('Perform Non-Rigid Registration')
        self.non_rigid_chbx.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.non_rigid_chbx.setChecked(False)

        non_rigid_layout = QHBoxLayout(non_rigid_frame)
        non_rigid_layout.setContentsMargins(5, 5, 5, 5)
        non_rigid_layout.setSpacing(10)
        non_rigid_layout.addWidget(non_rigid_label)
        non_rigid_layout.addWidget(self.non_rigid_chbx)

        non_rigid_frame.setFixedWidth(non_rigid_layout.sizeHint().width() + 5)

        content_layout = QGridLayout(content_widget)
        content_layout.setContentsMargins(25, 18, 25, 18)
        content_layout.addWidget(non_rigid_frame, 0, 1, 1, 1)
        content_layout.addWidget(non_rigid_header, 1, 0, 1, 1)
        content_layout.addWidget(self.non_rigid_combo, 1, 1, 1, 1)
        content_layout.addWidget(QLabel(''), 0, 3, 1, 1)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(15)
        main_layout.addWidget(content_widget)

    def toggle_settings(self, state):
        if state == Qt.CheckState.Checked:
            self.non_rigid_combo.setEnabled(True)
        else:
            self.non_rigid_combo.setEnabled(False)

    def get_data(self):
        if not self.non_rigid_chbx.isChecked():
            registration_method = None
        else:
            registration_method = self.non_rigid_combo.currentText()

        data_dict = {
            NON_RIGID_REGISTRAR_CLS: registration_method
        }

        return data_dict
    
    def get_default_data(self):
        if not self.non_rigid_chbx.isChecked():
            registration_method = None
        else:
            registration_method = NONRIGID_REGISTRARS[0]

        data_dict = {
            NON_RIGID_REGISTRAR_CLS: registration_method
        }

        return data_dict
