from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.gui.models import *
from src.gui.models.qt_spinbox import QtNumEntry


class ClassArgs(QWidget):
    def __init__(
        self,
        args: dict,
        font_size: int = 13,
        parent=None
    ):
        super().__init__()
        if parent is not None:
            self.parent = parent

        self._args = args
        self._arg_labels = []
        self._arg_widgets = []
        self._font_size = font_size

        themes = Themes()
        self.themes = themes.items

        self._setup_widget()

    def _setup_widget(self):
        widget_container = QFrame(self)
        widget_container.setObjectName('widget_container')
        widget_container.setFrameShape(QFrame.Shape.NoFrame)
        widget_container.setFrameShadow(QFrame.Shadow.Raised)
        widget_container.setStyleSheet(f"""
            QFrame#widget_container {{
                background: {self.themes['app_color']['main_bg']};
                border-radius: 8px;
                border: none;
            }}""")

        main_layout = QVBoxLayout(self)
        main_layout.setObjectName('main_layout')
        main_layout.setContentsMargins(0, 0, 0, 0)

        if self._args:
            layout_row = 0
            layout_col = 0

            widget_grid = QGridLayout(widget_container)
            widget_grid.setObjectName('widget_grid')
            widget_grid.setContentsMargins(10, 10, 10, 10)
            for name, value in self._args.items():
                arg_widget = QFrame(widget_container)
                arg_widget.setObjectName('arg_widget')
                arg_widget.setFrameShape(QFrame.Shape.NoFrame)
                arg_widget.setFrameShadow(QFrame.Shadow.Raised)

                arg_label = QLabel(arg_widget)
                arg_label.setObjectName('arg_label')
                arg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                arg_label.setText(name+':')
                arg_label.setStyleSheet(f'font-size: {self._font_size}px; color: {self.themes["app_color"]["text_color"]}')
                self._arg_labels.append(arg_label)

                arg_value = None
                if isinstance(value, bool):
                    arg_value = PyToggle(
                        width=34,
                        height=20,
                        ellipse_y=2,
                        bg_color = self.themes['app_color']['text_color'],
                        circle_color = self.themes['app_color']['yellow_bg'],
                        active_color = self.themes['app_color']['blue_bg'],
                        parent=arg_widget
                    )
                    arg_value.setObjectName('arg_value')
                    arg_value.setChecked(value)
                elif isinstance(value, (float, int)):
                    arg_value = QtNumEntry(
                        font_size=self._font_size,
                        font_color=self.themes['app_color']['text_color'],
                        bg_color=self.themes['app_color']['dark_one'],
                        parent=arg_widget
                    )
                    arg_value.setObjectName('arg_value')
                    arg_value.setRange(0, 1000)
                    arg_value.setDecimals(2)
                    arg_value.setSingleStep(0.25)
                    arg_value.setValue(value)
                    arg_value.setFixedSize(75, 25)
                elif isinstance(value, str):
                    arg_value = QLabel(arg_widget)
                    arg_value.setObjectName('arg_value')
                    arg_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    arg_value.setText('\'' + value + '\'')
                    arg_value.setStyleSheet(f'font-size: {self._font_size}px; color: {self.themes["app_color"]["text_color"]}; font-weight: bold;')
                self._arg_widgets.append(arg_value)
                arg_widget_layout = QHBoxLayout(arg_widget)
                arg_widget_layout.setObjectName('arg_widget_layout')
                arg_widget_layout.setContentsMargins(0, 0, 0, 0)
                arg_widget_layout.setSpacing(5)
                arg_widget_layout.addWidget(arg_label)
                arg_widget.setFixedWidth(arg_label.width() + arg_value.width())
                #arg_widget.setStyleSheet('QFrame#arg_widget{border: 1px solid black;}')
                if arg_value is not None:
                    arg_widget_layout.addWidget(arg_value)

                widget_grid.addWidget(arg_widget, layout_row, layout_col)
                widget_container.setFixedSize(widget_grid.sizeHint().width() + 25, widget_grid.sizeHint().height() + 25)
                if layout_row:
                    layout_col += 1
                    layout_row = 0
                else:
                    layout_row += 1
            main_layout.addWidget(widget_container)
        else:
            empty_label = QLabel(widget_container)
            empty_label.setObjectName('empty_label')
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setText('No Settings')
            empty_label.setStyleSheet(f'font-size: {self._font_size}px; color: {self.themes["app_color"]["text_color"]}')

            label_layout = QVBoxLayout(widget_container)
            label_layout.setObjectName('label_layout')
            label_layout.setContentsMargins(5, 5, 5, 5)
            label_layout.addWidget(empty_label, alignment=Qt.AlignmentFlag.AlignCenter)

            main_layout.addWidget(widget_container)

    def get_data(self):
        data = {}
        for index, widget in enumerate(self._arg_widgets):
            name: str
            name = self._arg_labels[index].text()
            name = name.replace(':', '')

            if isinstance(widget, PyToggle):
                data[name] = widget.isChecked()
            elif isinstance(widget, QtNumEntry):
                data[name] = widget.value()
            elif isinstance(widget, QLabel):
                data[name] = widget.text().strip("'")
        return data