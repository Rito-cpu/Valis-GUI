
viewer_template = """
    QWidget#{_obj_name} {{
        border-radius: 8px;
        border: none;
        background: {_bg};
    }}
"""

title_label_template = """
    QLabel {{
        font-size: {_title_size}px;
        color: {_color};
    }}
"""

body_label_template = """
    QLabel {{
        font-size: {_font_size};
        color: {_color};
    }}
"""


tool_bttn_template = """
    QToolButton {{
        background: {_color};
        border: none;
        border-radius: 6px;
    }}
"""

navigation_template = """
    QWidget#{_obj_name} {{
        border: none;
        border-radius: 14px;
        background: {_color};
    }}
"""

graphics_template = """
    QGraphicsView {
        border: 2px solid black;
        background: none;
    }
"""
