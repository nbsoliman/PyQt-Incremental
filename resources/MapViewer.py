import sys, os, math
try:
    from ResourceManager import ResourceManager
except:
    from resources.ResourceManager import ResourceManager
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import qdarktheme

class MapViewer(QGraphicsView):
    def __init__(self, bg_filename=None, parent=None):
        super().__init__()
        self.parent = parent
        try:
            self.bg_filename = os.path.join(os.path.dirname(__file__), '..', bg_filename)
        except:
            pass
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setRenderHints(QPainter.RenderHint.Antialiasing)
        self.grid_size = 250  # Size of each grid cell
        self.dimensions = 10000
        self.scene.setSceneRect(0, 0, self.dimensions, self.dimensions)
        self.add_clickable_objects()
        initial_zoom_factor = 0.45
        self.scale(initial_zoom_factor, initial_zoom_factor)
        if self.dimensions % 2 != 0:
            self.centerOn(self.dimensions/2, self.dimensions/2)
        else:
            self.centerOn(self.dimensions/2+self.grid_size/2, self.dimensions/2+self.grid_size/2)
        self.setStyleSheet("QGraphicsView { border: none; }")

        # self.fixed_button = QPushButton("Toggle Grid", self)
        self.fixed_button = QPushButton(self)
        self.fixed_button.setStyleSheet("background: transparent; padding-left: 4px; padding-right: 4px;")
        icon_pixmap = QPixmap(self.parent.resources.resource_path('assets/icons/grid.svg')).scaled(84, 84, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.fixed_button.setIcon(QIcon(icon_pixmap))

        self.fixed_button.clicked.connect(self.toggle_grid)
        QTimer.singleShot(0, self.update_fixed_button_position)
        # self.set_background_image()

    def add_clickable_objects(self):
        visible_range = 1
        space = int(self.dimensions/self.grid_size)
        for x in range(space):
            for y in range(space):
                # Current Buildings
                if x < int(space/2)+visible_range and x > int(space/2)-visible_range and y < int(space/2)+visible_range and y > int(space/2)-visible_range:
                    # self.parent.resources
                    margin = int(self.grid_size/10)
                    widget = QWidget()
                    widget.setStyleSheet('background: transparent')
                    t = QGroupBox(widget)
                    t.setFixedHeight(self.grid_size-margin)
                    t.setFixedWidth(self.grid_size-margin-8)
                    t.setStyleSheet('QGroupBox { border: 3px solid #f7d68a; padding:10px; background: transparent; border-radius: 14px;}')
                    layout = QVBoxLayout()

                    icon_label = QLabel()
                    icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    icon_pixmap = QPixmap(self.parent.resources.resource_path('assets/icons/town-hall.svg')).scaled(84, 84, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    icon_label.setPixmap(icon_pixmap)
                    
                    layout.insertWidget(0, icon_label)
                    label = QLabel(f"Town Hall")
                    label.setStyleSheet('font-size: 32px')
                    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    button = QPushButton('Upgrade')
                    button.setStyleSheet('font-size: 24px; background: #1e1e1e; border: 3px solid #8AB4F7; border-radius: 14px;')
                    button.setCursor(Qt.CursorShape.PointingHandCursor)
                    layout.addWidget(label)
                    layout.addWidget(button)
                    t.setLayout(layout)

                    button.clicked.connect(lambda _, x=x, y=y: self.upgrade_clicked(x, y))

                    proxy_widget = QGraphicsProxyWidget()
                    proxy_widget.setWidget(widget)
                    proxy_widget.setGeometry(QRectF(x * self.grid_size + margin/2, y * self.grid_size + margin/2, self.grid_size-margin, self.grid_size-margin))
                    self.scene.addItem(proxy_widget)
                # No building
                elif x < int(space/2)+(visible_range+1) and x > int(space/2)-(visible_range+1) and y < int(space/2)+(visible_range+1) and y > int(space/2)-(visible_range+1):
                    widget = QWidget()
                    # widget.setStyleSheet('background: red')
                    vbox = QVBoxLayout(widget)
                    icon_label = QLabel()
                    icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    icon_pixmap = QPixmap(self.parent.resources.resource_path('assets/icons/hammer.svg')).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    icon_label.setPixmap(icon_pixmap)
                    vbox.insertWidget(0, icon_label)
                    proxy_widget = QGraphicsProxyWidget()
                    proxy_widget.setWidget(widget)
                    proxy_widget.setGeometry(QRectF(x * self.grid_size+10, y * self.grid_size+10, self.grid_size-20, self.grid_size-20))
                    self.scene.addItem(proxy_widget)
                    icon_label.mouseDoubleClickEvent = lambda event: self.build_pressed()
                # Not Visible
                else:
                    pass
    
    def update_fixed_button_position(self):
        self.fixed_button.move(self.viewport().width() - self.fixed_button.width() -10, 
                               self.viewport().height() - self.fixed_button.height()-10)
        
    def upgrade_clicked(self, x, y):
        self.parent.buildings_layout_stack.setCurrentIndex(0)
        self.parent.buildings_title.setText(f"Town Hall")
        self.parent.buildings_info.setText(f"Plot: [{x}, {y}]")
        self.parent.buildings_upgrade1.setText(f"Increase Level 1 --> 2")

    def build_pressed(self):
        self.parent.buildings_layout_stack.setCurrentIndex(1)
        # self.parent.buildings_title.setText(f"Build New Structure")
        # self.parent.buildings_info.setText(f"Choose from the following:")
        # self.parent.buildings_upgrade1.setText(f"Tier 1 Miner")

    def toggle_grid(self):
        """Toggle grid visibility."""
        if hasattr(self, 'grid_visible') and self.grid_visible:
            for item in self.scene.items():
                if isinstance(item, QGraphicsRectItem) and item.pen().color() == QColor("#818181"):
                    self.scene.removeItem(item)
            self.grid_visible = False
        else:
            for x in range(0, int(self.scene.width()), self.grid_size):
                for y in range(0, int(self.scene.height()), self.grid_size):
                    rect = QRectF(x, y, self.grid_size, self.grid_size)
                    self.scene.addRect(rect, QPen(QColor("#818181")), brush=QBrush(Qt.GlobalColor.transparent))
            self.grid_visible = True

    def resizeEvent(self, event):
        QTimer.singleShot(0, self.update_fixed_button_position)

        if self.dimensions % 2 != 0:
            self.centerOn(self.dimensions/2, self.dimensions/2)
        else:
            self.centerOn(self.dimensions/2+self.grid_size/2, self.dimensions/2+self.grid_size/2)

    def wheelEvent(self, event):
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor

        visible_height = self.viewport().height()
        scene_height = self.scene.sceneRect().height()

        if visible_height > scene_height:
            visible_height = scene_height

        max_zoom_out_scale = scene_height / visible_height
        min_scale = max_zoom_out_scale
        max_scale = 2.0

        current_scale = self.transform().m11()

        if event.angleDelta().y() > 0:  # Zoom in
            self.scale(zoom_in_factor, zoom_in_factor)
        elif event.angleDelta().y() < 0:  # Zoom out
            self.scale(zoom_out_factor, zoom_out_factor)

        # if event.angleDelta().y() > 0 and current_scale * zoom_in_factor <= max_scale:  # Zoom in
        #     self.scale(zoom_in_factor, zoom_in_factor)
        # elif event.angleDelta().y() < 0 and current_scale * zoom_out_factor >= min_scale:  # Zoom out
        #     self.scale(zoom_out_factor, zoom_out_factor)
        
        event.accept()

    def set_background_image(self):
        """Set the background image for the scene."""
        pixmap = QPixmap(self.bg_filename)
        self.scene.setBackgroundBrush(QBrush(pixmap.scaledToHeight(self.scene.sceneRect().height(), Qt.TransformationMode.SmoothTransformation)))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resources = ResourceManager()
        self.resources.create()
        self.setWindowTitle("2D Map Viewer")
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create the main layout
        main_layout = QGridLayout(central_widget)
        main_layout.setColumnStretch(0, 4)
        main_layout.setColumnStretch(1, 1)
        
        self.right_gb = QGroupBox()
        self.right_gb.setStyleSheet('''QGroupBox {
                                background: transparent;
                                font-size: 18px;
                                font-weight: bold;
                                padding: 0px;
                                border-radius: 10px;
                                border: 1px solid #1e1e1e;
                                margin: 0px;
                            }''')
        right_layout = QGridLayout(self.right_gb)
        self.buildings_title = QLabel()
        self.buildings_title.setStyleSheet("font-size: 22px; font-weight: bold")
        self.buildings_info = QLabel("Select a plot")
        self.buildings_upgrade1 = QPushButton("")
        right_layout.addWidget(self.buildings_title, 0, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(self.buildings_info, 1, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(self.buildings_upgrade1, 2, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)

        self.map_viewer = MapViewer(parent=self)

        main_layout.addWidget(self.map_viewer, 0, 0, 1, 1)
        main_layout.addWidget(self.right_gb, 0, 1, 1, 1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())