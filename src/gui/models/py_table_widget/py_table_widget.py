from src.core.pyqt_core import *
from src.gui.models.py_table_widget.style import style


class PyTableWidget(QTableWidget):
    def __init__(
        self,
        radius = 8,
        color = "#FFF",
        bg_color = "#444",
        selection_color = "#FFF",
        header_horizontal_color = "#333",
        header_vertical_color = "#444",
        bottom_line_color = "#555",
        grid_line_color = "#555",
        scroll_bar_bg_color = "#FFF",
        scroll_bar_btn_color = "#333",
        context_color = "#00ABE8",
        font_size: int = 12,
        enable_header_color: bool = False,
        parent=None
    ):
        super().__init__()
        if parent != None:
            self.setParent(parent)

        if enable_header_color:
            style_template = style.format(
                _radius = radius,
                _color = color,
                _bg_color = bg_color,
                _header_horizontal_color = header_horizontal_color,
                _header_vertical_color = header_vertical_color,
                _selection_color = selection_color,
                _bottom_line_color = bottom_line_color,
                _grid_line_color = grid_line_color,
                _scroll_bar_bg_color = scroll_bar_bg_color,
                _scroll_bar_btn_color = scroll_bar_btn_color,
                _context_color = context_color,
                _header_color = bg_color,
                _font_size = font_size
            )
        else:
            style_template = style.format(
                _radius = radius,
                _color = color,
                _bg_color = bg_color,
                _header_horizontal_color = header_horizontal_color,
                _header_vertical_color = header_vertical_color,
                _selection_color = selection_color,
                _bottom_line_color = bottom_line_color,
                _grid_line_color = grid_line_color,
                _scroll_bar_bg_color = scroll_bar_bg_color,
                _scroll_bar_btn_color = scroll_bar_btn_color,
                _context_color = context_color,
                _header_color = color,
                _font_size = font_size
            )

        self.setStyleSheet(style_template)
