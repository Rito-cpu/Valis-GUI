import os

from src.core.pyqt_core import *
from src.gui.models import *
from src.gui.models.qt_line_button import QtButtonLineEdit
from .immuno_folder_widget import ImmunoFolderView

IHC_TYPE = 'ImmunoHistoChemistry'
CYCIF_TYPE = 'ImmunoFluorescence'


class QtImmunoWidget(QWidget):
    def __init__(
            self,
            text_color: str = 'black',
            blue_color: str = 'blue',
            yellow_color: str = 'yellow',
            highlight_color: str = 'yellow',
            parent=None
        ):
        super().__init__()

        if parent != None:
            self.setParent(parent)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self._text_color = text_color
        self._blue_color = blue_color
        self._yellow_color = yellow_color
        self._highlight_color = highlight_color

        self.setup_widget()

        # *** Slots/Signals ***
        self.image_dir_entry.entry_changed.connect(self.update_table)
        self.ihc_toggle.toggled.connect(self.check_ihc_state)
        self.cycif_toggle.toggled.connect(self.check_cycif_state)

    def setup_widget(self):
        entry_frame = QFrame(self)
        entry_frame.setObjectName('entry_frame')
        entry_frame.setFrameShape(QFrame.Shape.NoFrame)
        entry_frame.setFrameShadow(QFrame.Shadow.Raised)
        entry_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.image_dir_entry = QtButtonLineEdit(
            title="Slide Directory",
            title_color=self._text_color,
            color_three=self._blue_color,
            top_margin=18,
            parent=entry_frame
        )
        self.image_dir_entry.setObjectName(u'image_dir_entry')
        self.image_dir_entry.setMinimumWidth(350)

        #self.register_dir_bttn = PyPushButton(
        #    text="Register",
        #    radius=8,
        #    color='white',
        #    bg_color=self._yellow_color,
        #    bg_color_hover=self._highlight_color,
        #    bg_color_pressed=self._highlight_color,
        #    parent=entry_frame
        #)
        #self.register_dir_bttn.setObjectName(u"register_dir_bttn")
        #self.register_dir_bttn.setFixedSize(85, 31)

        #bttn_layout = QVBoxLayout()
        #bttn_layout.setContentsMargins(0, 22, 0, 0)
        #bttn_layout.addWidget(self.register_dir_bttn)

        entry_layout = QHBoxLayout(entry_frame)
        entry_layout.setContentsMargins(50, 0, 50, 0)
        # entry_layout.setSpacing(5)
        entry_layout.addWidget(self.image_dir_entry)
        #entry_layout.addLayout(bttn_layout)

        upper_area = QFrame(self)
        upper_area.setObjectName('upper_area')
        upper_area.setFrameShape(QFrame.Shape.NoFrame)
        upper_area.setFrameShadow(QFrame.Shadow.Raised)
        upper_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        options_frame = QFrame(upper_area)
        options_frame.setObjectName('options_frame')
        options_frame.setFrameShape(QFrame.Shape.NoFrame)
        options_frame.setFrameShadow(QFrame.Shadow.Raised)
        options_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        image_type_frame = QWidget(options_frame)
        image_type_frame.setObjectName('image_type_frame')
        image_type_frame.setStyleSheet('QWidget#image_type_frame{background: lightgray; border-radius: 12px;}')

        image_type_label = QLabel(image_type_frame)
        image_type_label.setObjectName('image_type_label')
        image_type_label.setText('Image Type')
        image_type_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_type_label.setStyleSheet('font-size: 13px; font-weight: bold;')

        # **** IHC Frame ****
        ihc_frame = QFrame(image_type_frame)
        ihc_frame.setObjectName('ihc_frame')
        ihc_frame.setFrameShape(QFrame.Shape.NoFrame)
        ihc_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.ihc_toggle = PyToggle(
                width=28,
                height=16,
                ellipse_y=2,
                bg_color = self._text_color,
                circle_color = self._yellow_color,
                active_color = self._blue_color,
                parent=ihc_frame
        )
        self.ihc_toggle.setObjectName(u"ihc_toggle")
        self.ihc_toggle.setChecked(True)
        self.ihc_toggle.setCursor(Qt.CursorShape.PointingHandCursor)

        ihc_title = QLabel(ihc_frame)
        ihc_title.setObjectName('ihc_title')
        ihc_title.setText(IHC_TYPE)
        ihc_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ihc_title.setStyleSheet('font-size: 13px;')

        ihc_layout = QGridLayout(ihc_frame)
        ihc_layout.setObjectName('ihc_layout')
        ihc_layout.setContentsMargins(0, 0, 0, 0)
        ihc_layout.setSpacing(10)
        ihc_layout.addWidget(ihc_title, 0, 0, 1, 1,)
        ihc_layout.addWidget(self.ihc_toggle, 0, 1, 1, 1)
        ihc_frame.setMinimumWidth(ihc_layout.sizeHint().width())
        ihc_frame.setMaximumWidth(int(ihc_layout.sizeHint().width() * 1.5))

        # **** Cycif Frame ****
        cycif_frame = QFrame(image_type_frame)
        cycif_frame.setObjectName('cycif_frame')
        cycif_frame.setFrameShape(QFrame.Shape.NoFrame)
        cycif_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.cycif_toggle = PyToggle(
                width=28,
                height=16,
                ellipse_y=2,
                bg_color = self._text_color,
                circle_color = self._yellow_color,
                active_color = self._blue_color,
                parent=cycif_frame
            )
        self.cycif_toggle.setObjectName(u"cycif_toggle")
        self.cycif_toggle.setChecked(False)
        self.cycif_toggle.setCursor(Qt.CursorShape.PointingHandCursor)

        cycif_label = QLabel(cycif_frame)
        cycif_label.setObjectName('cycif_label')
        cycif_label.setText(CYCIF_TYPE)
        cycif_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        cycif_label.setStyleSheet('font-size: 13px;')

        cycif_layout = QGridLayout(cycif_frame)
        cycif_layout.setObjectName('cycif_layout')
        cycif_layout.setContentsMargins(0, 0, 0, 0)
        cycif_layout.setSpacing(10)
        cycif_layout.addWidget(cycif_label, 0, 0, 1, 1)
        cycif_layout.addWidget(self.cycif_toggle, 0, 1, 1, 1)
        cycif_frame.setMinimumWidth(cycif_layout.sizeHint().width())
        cycif_frame.setMaximumWidth(int(cycif_layout.sizeHint().width() * 1.5))

        image_type_layout = QGridLayout(image_type_frame)
        image_type_layout.setObjectName('image_type_layout')
        image_type_layout.setContentsMargins(20, 20, 20, 20)
        image_type_layout.setHorizontalSpacing(30)
        image_type_layout.addWidget(image_type_label, 0, 0, 1, 2)
        image_type_layout.addWidget(ihc_frame, 1, 0, 1, 1)
        image_type_layout.addWidget(cycif_frame, 1, 1, 1, 1)
        image_type_frame.setMinimumWidth(image_type_layout.sizeHint().width())

        # **** Sorted Images Interaction ****
        sorted_frame = QFrame(options_frame)
        sorted_frame.setObjectName('sorted_frame')
        sorted_frame.setFrameShape(QFrame.Shape.NoFrame)
        sorted_frame.setFrameShadow(QFrame.Shadow.Raised)

        sorted_label = QLabel(sorted_frame)
        sorted_label.setObjectName('sorted_label')
        sorted_label.setText('Already Sorted')
        sorted_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sorted_label.setStyleSheet('font-size: 13px;')

        self.is_sorted_chbx = PyToggle(
            width=28,
            height=16,
            ellipse_y=2,
            bg_color = self._text_color,
            circle_color = self._yellow_color,
            active_color = self._blue_color,
            parent=sorted_frame
        )
        self.is_sorted_chbx.setObjectName('is_sorted_chbx')
        self.is_sorted_chbx.setChecked(False)

        sorted_layout = QGridLayout(sorted_frame)
        sorted_layout.setObjectName('sorted_layout')
        sorted_layout.setContentsMargins(0, 0, 0, 0)
        sorted_layout.setSpacing(10)
        sorted_layout.addWidget(sorted_label, 0, 0, 1, 1)
        sorted_layout.addWidget(self.is_sorted_chbx, 0, 1, 1, 1)
        sorted_frame.setFixedWidth(sorted_layout.sizeHint().width())

        options_layout = QVBoxLayout(options_frame)
        options_layout.setContentsMargins(0, 3, 0, 3)
        options_layout.addWidget(image_type_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        options_layout.addWidget(sorted_frame, alignment=Qt.AlignmentFlag.AlignCenter)

        # Unhide if image type is needed
        image_type_frame.hide()

        upper_area_layout = QVBoxLayout(upper_area)
        upper_area_layout.setObjectName('upper_area_layout')
        upper_area_layout.setContentsMargins(0, 0, 0, 0)
        upper_area_layout.setSpacing(15)
        upper_area_layout.addWidget(entry_frame)
        upper_area_layout.addWidget(options_frame)
        upper_area.setFixedHeight(upper_area_layout.sizeHint().height() + 10)

        # **** Table view ****
        folder_view_container = QFrame(self)
        folder_view_container.setObjectName('folder_view_container')
        folder_view_container.setFrameShape(QFrame.Shape.NoFrame)
        folder_view_container.setFrameShadow(QFrame.Shadow.Raised)

        self.image_folder_view = ImmunoFolderView(parent=folder_view_container)

        folder_view_layout = QVBoxLayout(folder_view_container)
        folder_view_layout.setObjectName('folder_view_layout')
        folder_view_layout.setContentsMargins(65, 0, 65, 25)
        folder_view_layout.addWidget(self.image_folder_view)

        # **** Finalize ****
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(55)
        main_layout.addWidget(upper_area)
        main_layout.addWidget(folder_view_container)

    def check_ihc_state(self):
        if self.ihc_toggle.isChecked():
            self.cycif_toggle.setChecked(False)
        else:
            self.cycif_toggle.setChecked(True)

    def check_cycif_state(self):
        if self.cycif_toggle.isChecked():
            self.ihc_toggle.setChecked(False)
        else:
            self.ihc_toggle.setChecked(True)

    def set_text(self, text: str):
        self.image_dir_entry.set_text(text)

    def update_table(self):
        directory = self.image_dir_entry.text()
        self.image_folder_view.populate_table(directory)

    def is_empty(self):
        empty_entry_check = self.image_dir_entry.text() == ''

        subdir_names, subdir_included = self.image_folder_view.get_table_data()
        empty_table_check = len(subdir_names) == 0 and len(subdir_included) == 0

        if empty_entry_check and empty_table_check:
            return True
        return False

    def is_valid_path(self):
        return os.path.exists(self.image_dir_entry.text())

    def has_all_toggled(self):
        # All toggle buttons are in the unchecked position
        _, subdir_included = self.image_folder_view.get_table_data()

        all_false = all(not state for state in subdir_included)

        return all_false

    def is_valid_data(self):
        '''
            Checks if the data we have is legitimate for valis process to move forward.
        '''
        # Insert script here? To check for specific files and slides?
        empty_data = self.is_empty()
        valid_path = self.is_valid_path()

        if empty_data or not valid_path:
            return False
        return True

    def get_data(self):
        slide_parent_dir = self.image_dir_entry.text()
        subdir_names, subdir_included = self.image_folder_view.get_table_data()
        image_type = self.ihc_toggle

        filtered_names = [name for index, name in enumerate(subdir_names) if subdir_included[index]]

        data_dict = {
            'parent_dir': slide_parent_dir,
            'slide_dirs': filtered_names,
            'already_sorted': self.is_sorted_chbx.isChecked()
        }

        return data_dict
