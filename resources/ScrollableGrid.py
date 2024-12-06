from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class ScrollableGrid(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.drag_pos = QPoint()
        self.setWidgetResizable(True)

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