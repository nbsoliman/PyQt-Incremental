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
        self.selected_coords_queue = [(0,0), (0,0)] # used to find prev coord
        self.current_selected_coords = (0,0)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setRenderHints(QPainter.RenderHint.Antialiasing)
        self.grid_size = 250  # Size of each grid cell
        self.margin = int(self.grid_size / 10)
        self.dimensions = 10000
        self.scene.setSceneRect(0, 0, self.dimensions, self.dimensions)
        self.load_clickable_objects_from_save()
        initial_zoom_factor = 0.45
        self.scale(initial_zoom_factor, initial_zoom_factor)
        if self.dimensions % 2 != 0:
            self.centerOn(self.dimensions/2, self.dimensions/2)
        else:
            self.centerOn(self.dimensions/2+self.grid_size/2, self.dimensions/2+self.grid_size/2)

        self.highlighted_item = None
        self.highlight_selected_item(0, 0)
        self.setStyleSheet("QGraphicsView { border: none; }")

        # self.fixed_button = QPushButton("Toggle Grid", self)
        self.fixed_button = QPushButton(self)
        self.fixed_button.setStyleSheet("background: transparent; padding-left: 4px; padding-right: 4px;")
        icon_pixmap = QPixmap(self.parent.resources.resource_path('assets/icons/grid.svg')).scaled(84, 84, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.fixed_button.setIcon(QIcon(icon_pixmap))

        self.fixed_button.clicked.connect(self.toggle_grid)
        QTimer.singleShot(0, self.update_fixed_button_position)
        # self.set_background_image()

    def load_clickable_objects_from_save(self):
        space = int(self.dimensions / self.grid_size)
        building_locations = {}

        for name, info in self.parent.resources.data["buildings"].items():
            x = info["location"]["x"]
            y = info["location"]["y"]
            icon = info["icon"]
            translated_coordinates = self.coordinate_translator(x, y)
            building_locations[translated_coordinates] = (name, icon)

        for x in range(space):
            for y in range(space):
                building_data = building_locations.get((x, y))
                if building_data:
                    building_name, icon = building_data
                    self.create_building(x, y, building_name, icon)
                else:
                    self.create_empty_space(x, y)

    def create_building(self, x, y, building_name, icon):
        self.clear_area(x, y)

        widget = QWidget()
        widget.setStyleSheet('background: transparent')
        t = QGroupBox(widget)
        t.setFixedHeight(self.grid_size - self.margin)
        t.setFixedWidth(self.grid_size - self.margin)
        t.setStyleSheet('QGroupBox { border: 3px solid #f7d68a; padding:10px; background: transparent; border-radius: 14px;}')
        layout = QVBoxLayout()

        icon_label = QLabel()
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_pixmap = QPixmap(self.parent.resources.resource_path(icon)).scaled(84, 84, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        icon_label.setPixmap(icon_pixmap)

        layout.insertWidget(0, icon_label)
        label = QLabel(building_name)
        label.setStyleSheet('font-size: 24px')
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button = QPushButton('Upgrade')
        button.setStyleSheet('font-size: 18px; background: #1e1e1e; border: 3px solid #8AB4F7; border-radius: 14px;')
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(label)
        layout.addWidget(button)
        t.setLayout(layout)

        button.clicked.connect(lambda _, x=x, y=y: self.upgrade_clicked(x, y))

        proxy_widget = QGraphicsProxyWidget()
        proxy_widget.setWidget(widget)
        proxy_widget.setGeometry(QRectF(x * self.grid_size + self.margin / 2,
                                        y * self.grid_size + self.margin / 2,
                                        self.grid_size - self.margin,
                                        self.grid_size - self.margin))
        self.scene.addItem(proxy_widget)

    def create_empty_space(self, x, y):
        self.clear_area(x, y)

        widget = QWidget()
        vbox = QVBoxLayout(widget)
        icon_label = QLabel()
        icon_label.setStyleSheet("background: #1e1e1e")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_pixmap = QPixmap(self.parent.resources.resource_path('assets/icons/hammer.svg')).scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        icon_label.setPixmap(icon_pixmap)
        vbox.insertWidget(0, icon_label)

        proxy_widget = QGraphicsProxyWidget()
        proxy_widget.setWidget(widget)
        proxy_widget.setGeometry(QRectF(x * self.grid_size + self.margin * 3, y * self.grid_size + self.margin * 3, self.grid_size - self.margin * 6, self.grid_size - self.margin * 6))
        self.scene.addItem(proxy_widget)

        icon_label.mousePressEvent = lambda _, x=x, y=y: self.build_pressed(x, y)

    def coordinate_translator(self, x, y, reverse=False):
        space = int(self.dimensions / self.grid_size)
        center = int(space / 2)
        if not reverse:
            new_x = x + center
            new_y = center - y
        else:
            new_x = x - center
            new_y = center - y
        return new_x, new_y

    def is_in_visible_range(self, x, y):
        visible_range = 2
        space = int(self.dimensions / self.grid_size)
        center = int(space / 2)
        return center - visible_range < x < center + visible_range and center - visible_range < y < center + visible_range

    def update_fixed_button_position(self):
        self.fixed_button.move(self.viewport().width() - self.fixed_button.width() -10, 
                               self.viewport().height() - self.fixed_button.height()-10)
        
    def clear_area(self, x, y):
        rect = QRectF(
            x * self.grid_size + self.margin / 2, 
            y * self.grid_size + self.margin / 2, 
            self.grid_size - self.margin, 
            self.grid_size - self.margin
        )
        items_to_remove = self.scene.items(rect)
        for item in items_to_remove:
            self.scene.removeItem(item)
    
    def highlight_selected_item(self, x, y):
        x, y = self.coordinate_translator(self.current_selected_coords[0], self.current_selected_coords[1])

        if self.highlighted_item is not None:
            if self.highlighted_item.scene() is self.scene:
                self.scene.removeItem(self.highlighted_item)
            self.highlighted_item = None

        widget = QWidget()
        widget.setStyleSheet('background: transparent')

        t = QGroupBox(widget)
        t.setFixedHeight(self.grid_size - self.margin)
        t.setFixedWidth(self.grid_size - self.margin)
        t.setStyleSheet('QGroupBox { border: 3px solid #8AB4F7; padding: 10px; background: transparent; border-radius: 14px;}')

        proxy_widget = QGraphicsProxyWidget()
        proxy_widget.setWidget(widget)
        proxy_widget.setGeometry(QRectF(
            x * self.grid_size + self.margin / 2,
            y * self.grid_size + self.margin / 2,
            self.grid_size - self.margin,
            self.grid_size - self.margin
        ))

        self.highlighted_item = proxy_widget
        self.scene.addItem(proxy_widget)

    def upgrade_clicked(self, x, y):
        self.current_selected_coords = self.coordinate_translator(x, y, True)
        if self.parent.buildings_layout_stack.currentIndex != 0:
            self.parent.buildings_layout_stack.setCurrentIndex(0)
            self.parent.buildings_title.setText(f"Town Hall")
            self.parent.buildings_info.setText(f"Plot: [{x}, {y}]")
            self.parent.buildings_upgrade1.setText(f"Increase Level 1 --> 2")
        self.highlight_selected_item(x, y)

    def build_pressed(self, x, y):
        self.current_selected_coords = self.coordinate_translator(x, y, True)
        if self.parent.buildings_layout_stack.currentIndex != 1:
            self.parent.buildings_layout_stack.setCurrentIndex(1)
        self.highlight_selected_item(x, y)

    def buy_pressed(self, name):
        x, y = self.coordinate_translator(self.current_selected_coords[0], self.current_selected_coords[1])
        self.create_building(x, y, name, 'assets/icons/town-hall.svg')
        self.parent.buildings_layout_stack.setCurrentIndex(0)
    
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

        min_scale = visible_height / scene_height
        current_scale = self.transform().m11()

        if event.angleDelta().y() > 0 and current_scale < 0.75:
            self.scale(zoom_in_factor, zoom_in_factor)
        elif event.angleDelta().y() < 0 and current_scale > 0.35:
            self.scale(zoom_out_factor, zoom_out_factor)

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