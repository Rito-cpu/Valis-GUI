import os

from src.core.pyqt_core import *
from src.core.app_config import IMG_RSC_PATH
from src.core.json.json_themes import Themes
from src.core.keyword_store import *
from .py_table_widget import PyTableWidget


class QtStatusTable(QWidget):
    def __init__(
            self,
            parent=None
    ) -> None:
        super().__init__()

        if parent != None:
            self.parent = parent

        themes = Themes()
        self.themes = themes.items

        # Setup widget
        self._setup_widget()

        # Setup signals/slots
        self.status_table.clicked.connect(self.on_sample_change)

    def _setup_widget(self):
        self.sample_list = []

        self.pending_icon = QIcon(os.path.join(IMG_RSC_PATH, "downloads/pending_icon.png"))
        self.running_icon = QIcon(os.path.join(IMG_RSC_PATH,  "downloads/running_icon.png"))
        self.complete_icon = QIcon(os.path.join(IMG_RSC_PATH, "downloads/complete_icon.png"))

        self.status_table = PyTableWidget(
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
        self.status_table.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.status_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        #self.status_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.status_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.status_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.status_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.status_table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.status_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.status_table.setHorizontalHeaderLabels(['File', 'Status'])
        self.status_table.setRowCount(0)
        self.status_table.setColumnCount(2)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.addWidget(self.status_table)

    def get_icon(self, status):
        if status == COMPLETE_S:
            icon = self.complete_icon
        elif status == PENDING_S:
            icon = self.pending_icon
        else:
            icon = self.running_icon

        return icon

    def reset_table(self):
        self.sample_list = []
        self.status_table.clear()
        self.status_table.setHorizontalHeaderLabels(['File', 'Status'])
        self.status_table.setRowCount(0)

    def fill_table(self, data):
        self.reset_table()
        # self.status_table.setRowCount(len(data))

        for index, sample in enumerate(data):
            self.sample_list.append(sample.sample_id)

            sample_icon = self.get_icon(sample.status)

            #sample_item = QStandardItem(sample.sample_id)
            #sample_item.setEditable(False)
            #sample_item.setIcon(sample_icon)
            #sample_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            # Create QTableWidgetItem for each column
            sample_item = QTableWidgetItem(sample.sample_id)
            sample_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable)  # Make item selectable and enabled
            sample_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            font = sample_item.font()
            font.setPointSize(12)
            sample_item.setFont(font)
            sample_item.setIcon(sample_icon)

            #status_item = QStandardItem(sample.status)
            #status_item.setEditable(False)
            #status_item.setSelectable(False)
            #status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            status_item = QTableWidgetItem(sample.status)
            status_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)  # Make item selectable and enabled
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            #font = status_item.font()
            #font.setPointSize(12)
            status_item.setFont(font)

            # Get current row count
            row_count = self.status_table.rowCount()
            # Insert new row
            self.status_table.insertRow(row_count)
            # Set items in the row
            self.status_table.setItem(row_count, 0, sample_item)  # Assuming sampleItem goes in column 0
            self.status_table.setItem(row_count, 1, status_item)  # Assuming sampleStatus goes in column 1
            # self.status_table.setRowHeight(row_count, sample_item.sizeHint().height() * 2)

            # self.status_table.insertRow([sample_item, status_item])

    def update_status(self, sample_obj):
        sample_index = self.sample_list.index(sample_obj.sample_id)

        print(f"getting sample {sample_obj.sample_id} status in row {sample_index}. sample list = {self.sample_list}")

        new_icon = self.get_icon(sample_obj.status)

        self.status_table.item(sample_index, 0).setIcon(new_icon)
        self.status_table.item(sample_index, 1).setText(sample_obj.status)

        if sample_obj.status == COMPLETE_S:
            self.status_table.item(sample_index, 0).setEnabled(True)

    def on_sample_change(self):
        indexes = self.status_table.selectionModel().selectedRows()

        if indexes:
            sample_name = self.status_table.item(indexes[0].row(), 0).text()
            # print(f"trying to get {sample_name} complete rigid {list(self.parent.app.project_info.completed_rigid.keys())}")
            sample_obj = self.parent.app.project_info.completed_rigid[sample_name]

            self.parent.app.results_viewer.set_sample(sample_obj)
            self.parent.app.results_viewer.update_img_view()
