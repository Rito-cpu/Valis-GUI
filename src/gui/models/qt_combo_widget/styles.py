combo_box_template = """
    QComboBox {{
        background: {bg};
        color: {color};
        border: none;
        border-radius: 4px;
        {fsize}
    }}
    QComboBox::drop-down {{
        border-left: 1px solid {color};
    }}
    QComboBox::down-arrow {{
        image: url({path});
        width: 15px;
        height: 15px;
    }}
    QComboBox QAbstractItemView {{
        background-color: lightgray;
        border: none;
        border-radius: 4px;
        selection-color: {bg};
    }}
    QComboBox QAbstractItemView::item {{
        color: {bg};
    }}
"""