groupbox_template = """
    QGroupBox {{
        color: {color};
        background: {bg_color};
        font-size: {title_size}px;
        border: none;
        border-radius: {border_radius}px;
        margin-top: {margin_top}px;
    }}
    QGroupBox:title {{
        color: {color_two};
        subcontrol-origin: margin;
        left: 17px;
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