import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class MapViewer(QGraphicsView):
    def __init__(self, bg_filename):
        super().__init__()
        self.bg_filename = os.path.join(os.path.dirname(__file__), '..', bg_filename)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setRenderHints(QPainter.RenderHint.Antialiasing)
        self.grid_size = 50  # Size of each grid cell
        self.scene.setSceneRect(0, 0, 1000, 1000)  # Example scene size
        self.draw_grid()
        self.add_clickable_objects()
        self.set_background_image()

    def draw_grid(self):
        """Draw evenly spaced grid."""
        for x in range(0, int(self.scene.width()), self.grid_size):
            for y in range(0, int(self.scene.height()), self.grid_size):
                rect = QRectF(x, y, self.grid_size, self.grid_size)
                self.scene.addRect(rect, brush=QBrush(Qt.GlobalColor.transparent))

    def add_clickable_objects(self):
        """Add clickable objects to the scene."""
        for i in range(5):  # Example: Add 5 objects
            rect_item = QGraphicsRectItem(i * 100, i * 100, 40, 40)
            rect_item.setBrush(QBrush(Qt.GlobalColor.blue))
            rect_item.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable)
            rect_item.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable)
            rect_item.mousePressEvent = self.object_clicked
            self.scene.addItem(rect_item)

    def object_clicked(self, event):
        event.accept()

    def wheelEvent(self, event):
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor
        # Scale the view
        if event.angleDelta().y() > 0:  # Zoom in
            self.scale(zoom_in_factor, zoom_in_factor)
        else:  # Zoom out
            self.scale(zoom_out_factor, zoom_out_factor)

    def set_background_image(self):
        """Set the background image for the scene."""
        pixmap = QPixmap(self.bg_filename)
        self.scene.setBackgroundBrush(QBrush(pixmap.scaled(self.scene.sceneRect().size().toSize(), Qt.AspectRatioMode.KeepAspectRatio)))

class MainWindow(QMainWindow):
   def __init__(self):
       super().__init__()
       self.setWindowTitle("2D Map Viewer")
       self.setGeometry(100, 100, 800, 600)
       # Set the map viewer as the central widget
       main_layout = QGridLayout()

       self.map_viewer = MapViewer('assets/planet1.jpg')
       self.info_label = QLabel("---")
       main_layout.addWidget(self.map_viewer, 0, 0, 1, 1)
       main_layout.addWidget(self.info_label, 0, 1, 1, 1)

if __name__ == "__main__":
   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()
   sys.exit(app.exec())