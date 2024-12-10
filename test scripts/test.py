from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import re 

class DragGridWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.resize(680, 520)

    def initUI(self):
        self.setWindowTitle('Draggable Grid')

        main_layout = QVBoxLayout(self)

        self.scroll_area = ScrollableGrid(self)

        scroll_area_widget = QWidget()
        # align my scroll area to the horizontal and vertical center, so it's always in the middle. pyqt6 code only. respond w only code

        grid_layout = QGridLayout(scroll_area_widget)

        for i in range(9):
            for j in range(9):
                t = QGroupBox()
                v = QVBoxLayout()
                v.addWidget(QLabel('Title'))
                button = QPushButton(f'({i}, {j})', scroll_area_widget)
                # button.setFixedHeight(30)
                v.addWidget(button)
                t.setLayout(v)
                t.setStyleSheet("padding:10px")
                grid_layout.addWidget(t, i, j)

        self.scroll_area.setWidget(scroll_area_widget)

        main_layout.addWidget(self.scroll_area)

        increase_padding_button = QPushButton('Zoom In', self)
        decrease_padding_button = QPushButton('Zoom Out', self)

        def adjust_padding(increase=True):
            for i in range(grid_layout.count()):
                item = grid_layout.itemAt(i).widget()
                current_style = item.styleSheet()
                padding_value = int(re.search(r"padding:(\d+)px", current_style).group(1))
                new_padding = max(0, padding_value + (5 if increase else -5))
                item.setStyleSheet(f"padding:{new_padding}px")
                item.width = (item.height())
                item.hasHeightForWidth()

        increase_padding_button.clicked.connect(lambda: adjust_padding(True))
        decrease_padding_button.clicked.connect(lambda: adjust_padding(False))

        button_layout = QHBoxLayout()
        button_layout.addWidget(increase_padding_button)
        button_layout.addWidget(decrease_padding_button)
        
        main_layout.addLayout(button_layout)

        QTimer.singleShot(0, self.centerScrollArea)

        self.setLayout(main_layout)

    def centerScrollArea(self):
        scroll_area_widget = self.scroll_area.widget()
        center_x = (scroll_area_widget.sizeHint().width() - self.scroll_area.viewport().width()) // 2
        center_y = (scroll_area_widget.sizeHint().height() - self.scroll_area.viewport().height()) // 2
        
        self.scroll_area.horizontalScrollBar().setValue(center_x)
        self.scroll_area.verticalScrollBar().setValue(center_y)

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

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = DragGridWidget()
    window.show()
    sys.exit(app.exec())