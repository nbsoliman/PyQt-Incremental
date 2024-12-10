import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Overlapping Layouts Example")
        self.setGeometry(100, 100, 800, 600)

        # Main container widget
        container = QWidget()
        self.setCentralWidget(container)

        # Main layout for the entire window
        main_layout = QVBoxLayout()
        container.setLayout(main_layout)

        # Background content (full-window layout)
        background_frame = QFrame()
        background_frame.setStyleSheet("background-color: lightblue;")
        main_layout.addWidget(background_frame)

        # Floating VBox layout on the right
        self.floating_layout_widget = QWidget(self)
        self.floating_layout_widget.setGeometry(self.width() - 200, 0, 200, self.height())
        self.floating_layout_widget.setStyleSheet("background-color: white; border: 1px solid black;")
        floating_layout = QVBoxLayout()
        self.floating_layout_widget.setLayout(floating_layout)

        # Add buttons to the floating layout
        for i in range(5):
            button = QLineEdit(f"Button {i+1}")
            floating_layout.addWidget(button)
        floating_layout.addStretch()

        # Reposition floating widget on resize
        self.resizeEvent = self.on_resize

    def on_resize(self, event):
        self.floating_layout_widget.setGeometry(self.width() - 200, 0, 200, self.height())
        super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())