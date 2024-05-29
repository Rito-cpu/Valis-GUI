from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.core.keyword_store import *
from .py_table_widget import PyTableWidget
from .qt_transform_item import TableTransformItem
from .qt_export_table_item import ExportTableItem


class QtExportSampleTable(QWidget):
    def __init__(
            self,
            parent=None
    ):
        super().__init__()

        if parent is not None:
            self.parent = parent

        themes = Themes()
        self.themes = themes.items

        self._sample_col = 0
        self._tform_col = 1

        # Setup widget
        self._setup_widget()

        # Setup signals/slots

    def _setup_widget(self):
        self.sample_table = PyTableWidget(
            radius = 4,
            color = self.themes["app_color"]["text_color"],
            selection_color = self.themes["app_color"]["yellow_bg"],
            bg_color = self.themes["app_color"]["main_bg"],
            header_horizontal_color = self.themes["app_color"]["blue_bg"],
            header_vertical_color = self.themes["app_color"]["blue_bg"],
            bottom_line_color = self.themes["app_color"]["bg_one"],
            grid_line_color = self.themes["app_color"]["bg_one"],
            scroll_bar_bg_color = self.themes["app_color"]["bg_one"],
            scroll_bar_btn_color = self.themes["app_color"]["dark_four"],
            context_color = self.themes["app_color"]["context_color"],
            font_size=13,
            enable_header_color=True,
            parent=self
        )
        self.sample_table.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.sample_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        #self.sample_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.sample_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.sample_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.sample_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.sample_table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.sample_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.sample_table.setHorizontalHeaderLabels(['Sample', 'Transform'])
        self.sample_table.setRowCount(0)
        self.sample_table.setColumnCount(2)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.addWidget(self.sample_table)

    def add_sample(self, sample_obj):
        sample_item = ExportTableItem(sample_obj.sample_id,  sample_obj)
        tform_radio_btns = TableTransformItem(sample_obj)
        self.sample_table.insertRow(self.sample_table.rowCount())

        self.sample_table.setCellWidget(self.sample_table.rowCount()-1, self._sample_col, sample_item)
        self.sample_table.setCellWidget(self.sample_table.rowCount()-1, self._tform_col, tform_radio_btns)

        self.sample_table.resizeColumnsToContents()
        self.sample_table.resizeRowsToContents()

    def fill_table(self, data):
        self.reset_table()
        # do_non_rigid = data[0].proj_obj.do_non_rigid
        # for d in data:
        #     if (do_non_rigid and d.non_rigid_complete) or (do_non_rigid == False and d.rigid_complete):
        #         self.add_sample(d)
        for d in data:
            self.add_sample(d)

    def reset_table(self):
        self.sample_table.clear()
        self.sample_table.setHorizontalHeaderLabels(['Sample', 'Transform'])
        self.sample_table.setRowCount(0)

    def update_sample_dict(self, sample_obj_dict):
        for row_index in range(self.sample_table.rowCount()):
            sample_cell = self.sample_table.cellWidget(row_index, self._sample_col)

            sample_obj = sample_obj_dict[sample_cell.text()]
            sample_obj.to_export = sample_cell.isChecked()

            tform_item = self.sample_table.cellWidget(row_index, self._tform_col)
            sample_obj.export_non_rigid = tform_item.is_non_rigid()
            # print(sample_obj.sample_id, "export:", sample_obj.to_export, "non-rigid:", sample_obj.export_non_rigid)

            # .to_align = sample_row.checkState() == Qt.CheckState.Checked
            # if self.all_rigid_radio_btn.isChecked():
                # tform_radio.rigid_rbtn.setChecked(True)
            # else:
                # tform_radio.non_rigid_rbtn.setChecked(True)

    def select_all(self, key):
        if key == RIGID_KEY:
            for row in range(self.sample_table.rowCount()):
                item: TableTransformItem
                item = self.sample_table.cellWidget(row, self._tform_col)
                item.set_rigid()
        else:
            for row in range(self.sample_table.rowCount()):
                item: TableTransformItem
                item = self.sample_table.cellWidget(row, self._tform_col)
                item.set_non_rigid()
