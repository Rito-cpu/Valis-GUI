groupbox_template = """
    QGroupBox {{
        color: {color};
        background: {bg_color};
        font-size: {title_size}px;
        border: none;
        border-radius: {border_radius}px;
    }}
    QLabel {{
        color: {color};
        font-size: {font_size}px;
    }}
    QCheckBox {{
        color: {color};
        font-size: {font_size}px;
    }}
"""

setting_label_template = """
    QLabel {{
        color: {font_color};
        font-size: {size}px;
    }}
"""