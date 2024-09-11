from .styles import graphics_template
from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.gui.models.qt_message import QtMessage


class QtGraphicsView(QGraphicsView):
    left_mouse_button_pressed = pyqtSignal(float, float)
    right_mouse_button_pressed = pyqtSignal(float, float)
    left_mouse_button_released = pyqtSignal(float, float)
    right_mouse_button_released = pyqtSignal(float, float)
    left_mouse_button_double_clicked = pyqtSignal(float, float)
    right_mouse_button_double_clicked = pyqtSignal(float, float)
    image_added = pyqtSignal()
    images_removed = pyqtSignal()
    scale_changed = pyqtSignal(float)

    def __init__(
            self,
            default_scale: float = 1.0,
            scale_factor: float = 0.2,
            max_scale: float = 2.0,
            min_scale: float = 0.4,
            parent=None
    ) -> None:
        super().__init__()

        if parent is not None:
            self.parent = parent

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.aspect_ratio_mode = Qt.AspectRatioMode.KeepAspectRatio # KeepAspectRatioByExpanding

        self.graphics_scene = QGraphicsScene(self)
        self.setScene(self.graphics_scene)

        self._pixmap_handle = None
        self.zoom_stack = []
        self.can_zoom = True
        self.can_pan = True
        self._current_scale = default_scale
        self._scale_factor = scale_factor
        self._max_scale_factor = max_scale
        self._min_scale_factor = min_scale

        themes = Themes()
        self.themes = themes.items

        self.setStyleSheet(graphics_template)

    def has_image(self):
        return self._pixmap_handle is not None

    def clear_image(self):
        if self.has_image():
            self.graphics_scene.removeItem(self._pixmap_handle)
            self._pixmap_handle = None
            self.images_removed.emit()

    def pixmap(self):
        if self.has_image():
            return self._pixmap_handle.pixmap()
        return None

    def image(self):
        if self.has_image():
            return self._pixmap_handle.pixmap().toImage()
        return None

    def set_image(self, image):
        buttons = {
            "Ok": QMessageBox.ButtonRole.AcceptRole,
        }

        error_msg = QtMessage(buttons=buttons,
                        color=self.themes["app_color"]["main_bg"],
                        bg_color_one=self.themes["app_color"]["dark_one"],
                        bg_color_two=self.themes["app_color"]["bg_one"],
                        bg_color_hover=self.themes["app_color"]["dark_three"],
                        bg_color_pressed=self.themes["app_color"]["dark_four"])
        error_msg.setIcon(QMessageBox.Icon.Warning)

        if isinstance(image,QPixmap):
            pixmap = image
        elif isinstance(image, QImage):
            pixmap = QPixmap.fromImage(image)
        else:
            error_msg.setText('Image Viewer Received Wrong Image')
            error_msg.setInformativeText('Image Viewer (set_image method) expects a QImage or a QPixmap, but received an image of a different type. ')
            error_msg.exec()
            error_msg.deleteLater()
            return
            # raise RuntimeError("ImageViewer.setImage: Argument must be a QImage or QPixmap.")

        if self.has_image():
            self._pixmap_handle.setPixmap(pixmap)
        else:
            self._pixmap_handle = self.graphics_scene.addPixmap(pixmap)

        self.setSceneRect(QRectF(pixmap.rect()))  # Set scene size to image size.
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

        self.update_viewer()
        # self.resize(pixmap.width(), pixmap.height())
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)

        self.image_added.emit()

    def update_viewer(self):
        if not self.has_image():
            return
        if len(self.zoom_stack) and self.sceneRect().contains(self.zoom_stack[-1]):
            self.fitInView(self.zoom_stack[-1], Qt.AspectRatioMode.IgnoreAspectRatio)  # Show zoomed rect (ignore aspect ratio).
        else:
            self.zoom_stack = []  # Clear the zoom stack (in case we got here because of an invalid zoom).
            self.fitInView(self.sceneRect(), self.aspect_ratio_mode)  # Show entire image (use current aspect ratio mode).

    def resizeEvent(self, event):
        self.update_viewer()
        # self.reset_zoom()
        self.set_scale(self._current_scale)

    def zoom_out(self):
        # Calculate the new scale factor for zooming out
        new_scale = self._current_scale - self._scale_factor

        if new_scale >= self._min_scale_factor:
            self.set_scale(new_scale)

    def zoom_in(self):
        # Increase the scale factor for zooming in
        new_scale = self._current_scale + self._scale_factor

        if new_scale <= self._max_scale_factor:
            self.set_scale(new_scale)

    def set_scale(self, scale_factor):
        # Ensure that the scale factor is within the allowed limits
        scale_factor = max(self._min_scale_factor, min(scale_factor, self._max_scale_factor))

        # Create a new transformation matrix with the specified scale factor
        transform = QTransform()
        transform.scale(scale_factor, scale_factor)

        # Apply the transformation matrix to the view
        self.setTransform(transform)

        # Update the current scale factor
        self._current_scale = scale_factor
        self.scale_changed.emit(self._current_scale)

    def reset_zoom(self):
        self._current_scale = 1.0
        self.set_scale(self._current_scale)

    def mousePressEvent(self, event):
        scene_pos = self.mapToScene(event.pos())

        if event.button() == Qt.MouseButton.LeftButton:
            if self.can_pan:
                self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
            self.left_mouse_button_pressed.emit(scene_pos.x(), scene_pos.y())
        elif event.button() == Qt.MouseButton.RightButton:
            if self.can_zoom:
                self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
            self.right_mouse_button_pressed.emit(scene_pos.x(), scene_pos.y())
        QGraphicsView.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        QGraphicsView.mouseReleaseEvent(self, event)
        scene_pos = self.mapToScene(event.pos())

        if event.button() == Qt.MouseButton.LeftButton:
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
            self.left_mouse_button_released.emit(scene_pos.x(), scene_pos.y())
        elif event.button() == Qt.MouseButton.RightButton:
            if self.can_zoom:
                viewBBox = self.zoom_stack[-1] if len(self.zoom_stack) else self.sceneRect()
                selectionBBox = self.graphics_scene.selectionArea().boundingRect().intersected(viewBBox)
                self.graphics_scene.setSelectionArea(QPainterPath())  # Clear current selection area.
                if selectionBBox.isValid() and (selectionBBox != viewBBox):
                    self.zoom_stack.append(selectionBBox)
                    self.update_viewer()
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
            self.right_mouse_button_released.emit(scene_pos.x(), scene_pos.y())

    def mouseDoubleClickEvent(self, event):
        scene_pos = self.mapToScene(event.pos())

        if event.button() == Qt.MouseButton.LeftButton:
            self.left_mouse_button_double_clicked.emit(scene_pos.x(), scene_pos.y())
        elif event.button() == Qt.MouseButton.RightButton:
            if self.can_zoom:
                self.zoom_stack = []  # Clear zoom stack.
                self.update_viewer()
            self.right_mouse_button_double_clicked.emit(scene_pos.x(), scene_pos.y())
        QGraphicsView.mouseDoubleClickEvent(self, event)
