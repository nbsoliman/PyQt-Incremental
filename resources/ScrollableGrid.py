from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys, os
import qdarktheme

class ScrollableGrid(QScrollArea):
    def __init__(self, bg_filename, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.drag_pos = QPoint()
        self.bg_filename = os.path.join(os.path.dirname(__file__), '..', bg_filename)
        # self.bg_filename = bg_filename
        self.setWidgetResizable(True)
        self.setBackground()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if not self.drag_pos.isNull():
            delta = self.drag_pos - event.globalPosition().toPoint()
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() + delta.y())
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + delta.x())
            self.drag_pos = event.globalPosition().toPoint()
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = QPoint()

    def setBackground(self):
        palette = QPalette()
        pixmap = QPixmap(self.bg_filename)
        brush = QBrush(pixmap)
        palette.setBrush(QPalette.ColorRole.Window, brush)
        self.setPalette(palette)
        self.setAutoFillBackground(True)

# # To test:
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Scrollable Grid Test")
#         self.setGeometry(100, 100, 600, 400)
        
#         widget = ScrollableGrid('assets/planet1.jpg', self)
#         # widget.setBackground()

#         content_widget = QWidget()
#         layout = QGridLayout(content_widget)
        
#         for i in range(50):
#             for j in range(50):
#                 label = QLabel(f"Label {i}, {j}")
#                 layout.addWidget(label, i, j)
        
#         widget.setWidget(content_widget)
#         self.setCentralWidget(widget)

# app = QApplication(sys.argv)
# # app.setStyleSheet(qdarktheme.load_stylesheet())
# window = MainWindow()
# window.show()
# sys.exit(app.exec())