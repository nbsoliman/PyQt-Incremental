import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import qdarktheme

class MapViewer(QGraphicsView):
    def __init__(self, bg_filename, parent=None):
        super().__init__()
        self.parent = parent
        self.bg_filename = os.path.join(os.path.dirname(__file__), '..', bg_filename)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setRenderHints(QPainter.RenderHint.Antialiasing)
        self.grid_size = 50  # Size of each grid cell
        self.scene.setSceneRect(0, 0, 1000, 1000)  # Example scene size
        self.draw_grid()
        self.add_clickable_objects()
        # self.set_background_image()

    def draw_grid(self):
        """Draw evenly spaced grid."""
        for x in range(0, int(self.scene.width()), self.grid_size):
            for y in range(0, int(self.scene.height()), self.grid_size):
                rect = QRectF(x, y, self.grid_size, self.grid_size)
                self.scene.addRect(rect, brush=QBrush(Qt.GlobalColor.transparent))

    def add_clickable_objects(self):
        """Add clickable objects to the scene."""
        for i in range(5):  # Example: Add 5 objects
            rect_item = QGraphicsRectItem(i * 100, i * 100, 50, 50)
            rect_item.setBrush(QBrush(Qt.GlobalColor.blue))
            rect_item.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable)
            rect_item.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable)
            rect_item.setData(0, f"Object_{i}")  # Assign a unique ID or name to each object
            rect_item.mousePressEvent = self.object_clicked
            self.scene.addItem(rect_item)

    def object_clicked(self, event):
        item = self.scene.itemAt(event.scenePos(), self.scene.views()[0].transform())
        if item is not None:
            object_name = item.data(0)  # Retrieve the unique ID or name
            if self.parent:  # Ensure that parent is not None
                self.parent.info_label.setText(object_name)
        event.accept()

    def wheelEvent(self, event):
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor
        min_scale = 0.5  # minimum scale factor to prevent too much zoom out

        # Get the current scale of the transform
        current_scale = self.transform().m11()

        if event.angleDelta().y() > 0:  # Zoom in
            self.scale(zoom_in_factor, zoom_in_factor)
        else:  # Zoom out
            if current_scale * zoom_out_factor >= min_scale:
                self.scale(zoom_out_factor, zoom_out_factor)

    def set_background_image(self):
        """Set the background image for the scene."""
        pixmap = QPixmap(self.bg_filename)
        self.scene.setBackgroundBrush(QBrush(pixmap.scaled(self.scene.sceneRect().size().toSize(), Qt.AspectRatioMode.KeepAspectRatio)))

    def setBackground(self):
        palette = QPalette()
        pixmap = QPixmap(self.bg_filename)
        brush = QBrush(pixmap)
        palette.setBrush(QPalette.ColorRole.Window, brush)
        self.setPalette(palette)
        self.setAutoFillBackground(True)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("2D Map Viewer")
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create the main layout
        main_layout = QGridLayout(central_widget)
        self.info_label = QLabel("---")
        self.map_viewer = MapViewer('assets/planet1.jpg', self)
        main_layout.addWidget(self.map_viewer, 0, 0, 1, 1)
        main_layout.addWidget(self.info_label, 0, 1, 1, 1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())