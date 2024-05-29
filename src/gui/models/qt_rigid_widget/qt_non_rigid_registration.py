from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.gui.models.qt_combo_widget import *
from .styles import *


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

        if len(non_rigid_methods) == 0:
            non_rigid_methods = [
                'Deep Flow',
                'SimpleElastix',
                'Demons',
                'RAFT',
                'Symmetric Diffeomorphic'
            ]
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

    def _setup_widget(self):
        content_widget = QWidget(self)
        content_widget.setObjectName('content_widget')

        process_method_label = QLabel(content_widget)
        process_method_label.setObjectName('process_method_label')
        process_method_label.setText('Processing Method:')

        self.non_rigid_combo = QtComboBox(
            bg_color=self.themes["app_color"]["dark_one"],
            text_color=self.themes["app_color"]["text_color"],
            parent=content_widget
        )
        self.non_rigid_combo.setObjectName('non_rigid_combo')
        self.non_rigid_combo.addItems(self._non_rigid_methods)
        self.non_rigid_combo.setCurrentIndex(0)
        self.non_rigid_combo.setFixedHeight(30)
        self.non_rigid_combo.setMinimumWidth(120)

        content_layout = QGridLayout(content_widget)
        content_layout.setContentsMargins(25, 18, 25, 18)
        content_layout.addWidget(process_method_label, 0, 0, 1, 1)
        content_layout.addWidget(self.non_rigid_combo, 0, 1, 1, 2)
        content_layout.addWidget(QLabel(''), 0, 3, 1, 1)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(15)
        main_layout.addWidget(content_widget)

    def get_data(self):
        registration_type = self.non_rigid_combo.currentText() if not self.isHidden() else None
        data_dict = {
            'method': registration_type
        }

        return data_dict
