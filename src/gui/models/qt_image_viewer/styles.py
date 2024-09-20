
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
        font-size: {_font_size}px;
        color: {_color};
        background-color: {_bg};
        border: none;
        border-radius: 9px;
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
    QFrame#{_obj_name} {{
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

right_arrow_template = """
    QFrame#main_frame {{
        background: {_color};
        border: none;
        border-top-right-radius: 9px;
        border-bottom-right-radius: 9px;
        border-top-left-radius: 9px;
        border-bottom-left-radius: 9px;
        color: {text_color};
    }}
"""

left_arrow_template = """
    QFrame#main_frame {{
        background: {_color};
        border: none;
        border-top-right-radius: 9px;
        border-bottom-right-radius: 9px;
        border-top-left-radius: 9px;
        border-bottom-left-radius: 9px;
        color: {text_color};
    }}
"""
