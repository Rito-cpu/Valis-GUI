from src.core.pyqt_core import *
from src.core.image_functions import Functions
from src.core.json.json_themes import Themes
from src.gui.models.qt_clickable_icon import QtMenuIcon


class QtSectionalWidget(QWidget):
    def __init__(
        self,
        section_title: str,
        icon_name: str,
        collapsed_info: str,
        expanded_info,
        title_font: int = 16,
        icon_size: int = 70,
        parent=None
    ):
        super().__init__(parent)

        if parent is not None:
            self.parent = parent

        themes = Themes()
        self.themes = themes.items

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self._section_title = section_title
        self._icon_path = Functions.set_svg_icon(icon_name)
        self._collapsed_info = collapsed_info
        self._expanded_info = expanded_info
        self._title_font = title_font
        self._icon_size = icon_size
        self.is_expanded = False
        self.animation_duration = 200

        self._setup_widget()

        self.sectional_icon.clicked.connect(self.toggle_collapsed)

    def _setup_widget(self):
        outermost_frame = QFrame(self)
        outermost_frame.setObjectName('outermost_frame')
        outermost_frame.setFrameShape(QFrame.Shape.NoFrame)
        outermost_frame.setFrameShadow(QFrame.Shadow.Plain)
        outermost_frame.setStyleSheet(f"""
            QFrame#outermost_frame {{
                border: 1px solid {self.themes['app_color']['blue_bg']};
                border-radius: 6px;
                background: {self.themes['app_color']['main_bg']};
            }}
        """)

        sectional_title = QLabel(outermost_frame)
        sectional_title.setObjectName('sectional_title')
        sectional_title.setText(self._section_title)
        sectional_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sectional_title.setStyleSheet(f'color: {self.themes["app_color"]["blue_bg"]}; font-size: {self._title_font}px; font-weight: bold;')

        self.sectional_icon = QtMenuIcon(
            icon_name=self._icon_path,
            icon_size=self._icon_size,
            set_checkable=True,
            parent=outermost_frame
        )
        self.sectional_icon.setObjectName('sectional_icon')

        self.info_area_stack = QStackedWidget(outermost_frame)
        self.info_area_stack.setObjectName('info_area_stack')

        self.collapsed_text = QTextEdit(self.info_area_stack)
        self.collapsed_text.setObjectName('collapsed_info')
        self.collapsed_text.setMinimumWidth(325)
        self.collapsed_text.setReadOnly(True)
        self.collapsed_text.setText(self._collapsed_info)
        self.collapsed_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.collapsed_text.setStyleSheet(f'border: none; background: {self.themes["app_color"]["main_bg"]};')

        self.expanded_wid = QWidget(self.info_area_stack)
        self.expanded_wid.setFixedHeight(500)

        self.info_area_stack.addWidget(self.collapsed_text)
        self.info_area_stack.addWidget(self.expanded_wid)
        self.info_area_stack.setCurrentIndex(0)
        self.adjust_height_to_content()

        grid_filler = QWidget()
        outermost_frame_layout = QGridLayout(outermost_frame)
        outermost_frame_layout.setObjectName('outermost_frame_layout')
        outermost_frame_layout.setContentsMargins(5, 5, 30, 5)
        outermost_frame_layout.setSpacing(5)
        outermost_frame_layout.addWidget(self.sectional_icon, 0, 0, 3, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        outermost_frame_layout.addWidget(sectional_title, 0, 1, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        outermost_frame_layout.addWidget(self.info_area_stack, 1, 1, 2, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        outermost_frame_layout.addWidget(grid_filler, 2, 3, 1, 1)

        #outermost_frame.setMinimumSize(QSize(int(outermost_frame_layout.sizeHint().width()*1.3), outermost_frame_layout.sizeHint().height()))
        #outermost_frame.setMaximumSize(QSize(int(outermost_frame_layout.sizeHint().width()*2), outermost_frame_layout.sizeHint().height()))
        self.outermost_frame = outermost_frame
        self.collapsed_height = outermost_frame.sizeHint().height()
        self.expanded_height = self.collapsed_height + self.expanded_wid.sizeHint().height()
        #outermost_frame.resize(QSize(int(outermost_frame_layout.sizeHint().width()*1.5), outermost_frame_layout.sizeHint().height()))

        main_layout = QVBoxLayout(self)
        main_layout.setObjectName('main_layout')
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(outermost_frame)

    def toggle_collapsed(self):
        # Set the current index first before starting the animation
        self.is_expanded = not self.is_expanded
        self.info_area_stack.setCurrentWidget(self.expanded_wid if self.is_expanded else self.collapsed_text)
        
        # Recalculate heights if needed for the new state
        self.update_heights()

        # Start the animation
        self.animate_resize()

    def update_heights(self):
        if not self.is_expanded:
            # Adjust collapsed height once
            self.adjust_height_to_content()
        self.expanded_height = self.collapsed_height + self.expanded_wid.sizeHint().height()


    def animate_resize(self):
        # Use the updated collapsed and expanded heights for animation
        start_height = self.collapsed_height if not self.is_expanded else self.expanded_height
        end_height = self.expanded_height if not self.is_expanded else self.collapsed_height

        self.animation = QPropertyAnimation(self.outermost_frame, b"maximumHeight")
        self.animation.setDuration(self.animation_duration)
        self.animation.setStartValue(start_height)
        self.animation.setEndValue(end_height)
        self.animation.start()

    def adjust_height_to_content(self):
        doc_height = self.collapsed_text.document().size().height()
        margin_top = self.collapsed_text.contentsMargins().top()
        margin_bottom = self.collapsed_text.contentsMargins().bottom()

        # Set the height of the collapsed text area only, not the whole stack
        self.collapsed_text.setFixedHeight(doc_height + margin_top + margin_bottom + 4)
        # Allow `info_area_stack` to grow/shrink during animation
        self.info_area_stack.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

    def adjust_height_to_content2(self):
        doc_height = self.collapsed_text.document().size().height()
        margin_top = self.collapsed_text.contentsMargins().top()
        margin_bottom = self.collapsed_text.contentsMargins().bottom()

        self.collapsed_text.setFixedHeight(doc_height + margin_top + margin_bottom + 4)
        self.info_area_stack.setFixedHeight(self.collapsed_text.size().height()+4)
    # TODO: Configure resizing
    #def sizeHint(self):
    #    return QSize(int(self.minimumSize().width()*1.5), self.minimumSize().height())

    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Set custom color, font, or other properties if needed
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        #painter.setBrush(QColor(200, 200, 255))  # Set a background color
        #painter.drawRoundedRect(self.rect(), 10, 10)  # Draw a rounded rectangle as the background

        # Draw text in the center
        #painter.setPen(QColor(50, 50, 50))
        #font = QFont("Arial", 12, QFont.Weight.Bold)
        #painter.setFont(font)
        #painter.drawText(self.rect(), "Custom Widget", alignment=Qt.AlignmentFlag.AlignCenter)
