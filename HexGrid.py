import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import QtGui
import qdarktheme
import math

class HexWidget(QWidget):
   def __init__(self, label_text, button_text, parent=None):
       super().__init__(parent)
       self.setFixedSize(200, 200)  # Fixed size for each hexagon
       layout = QVBoxLayout(self)
       layout.setContentsMargins(0, 0, 0, 0)
       layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
       # Add label
       label = QLabel(label_text, self)
       label.setAlignment(Qt.AlignmentFlag.AlignCenter)
       layout.addWidget(label)
       # Add button
       button = QPushButton(button_text, self)
       layout.addWidget(button)
   def paintEvent(self, event):
       """Draw the hexagon shape."""
       super().paintEvent(event)
       painter = QtGui.QPainter(self)
       painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
       polygon = QPolygonF(self.hexagon_points())
       painter.setBrush(QtGui.QColor("lightblue"))
       painter.setPen(QtGui.QPen(Qt.GlobalColor.black, 2))
       painter.drawPolygon(polygon)
   @staticmethod
   def hexagon_points():
       """Generate the points for a hexagon."""
       points = []
       for i in range(6):
           angle = math.radians(60 * i)
           x = 50 + 40 * math.cos(angle)  # Center at (50, 50), radius 40
           y = 50 + 40 * math.sin(angle)
           points.append(QPointF(x, y))
       return points

class HexGrid(QWidget):
   def __init__(self, rows, cols, parent=None):
       super().__init__(parent)
       self.setMinimumSize(cols * 110, rows * 110)  # Adjust minimum size
       self.layout = QVBoxLayout(self)
       self.layout.setContentsMargins(0, 0, 0, 0)
       self.grid_widgets(rows, cols)
   def grid_widgets(self, rows, cols):
       for row in range(rows):
           row_layout = QHBoxLayout()
           row_layout.setContentsMargins(0, 0, 0, 0)
           row_layout.setSpacing(5)
           for col in range(cols):
               label_text = f"({row}, {col})"
               button_text = f"Button {row * cols + col}"
               hex_widget = HexWidget(label_text, button_text)
               row_layout.addWidget(hex_widget)
           self.layout.addLayout(row_layout)

class ScrollableHexGrid(QScrollArea):
   def __init__(self, rows, cols, parent=None):
       super().__init__(parent)
       self.setWidgetResizable(True)
       # HexGrid is the scrollable content
       hex_grid = HexGrid(rows, cols)
       self.setWidget(hex_grid)

class MainWindow(QMainWindow):
   def __init__(self):
       super().__init__()
       self.setWindowTitle("Scrollable HexGrid")
       # Create a scrollable hex grid
       scrollable_hexgrid = ScrollableHexGrid(10, 8)
       self.setCentralWidget(scrollable_hexgrid)

if __name__ == "__main__":
   app = QApplication(sys.argv)
   window = MainWindow()
   window.resize(800, 600)
   window.show()
   sys.exit(app.exec())