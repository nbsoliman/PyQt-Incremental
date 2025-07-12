from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from functools import partial
import json, os, sys, traceback, re, random, math
import pyqtgraph as pg

from resources.Space3D import Planet3DWidget
from resources.ScrollableGrid import ScrollableGrid
from resources.MapViewer import MapViewer
from resources.Space3D import Planet3DWidget

def createMainMenu(parent):
    parent.backdrop_layout = QVBoxLayout()
    parent.backdrop_layout.setContentsMargins(0, 0, 0, 0)
    parent.backdrop_layout.setSpacing(0)

    parent.this_widget = QWidget()
    parent.this_widget.setLayout(parent.backdrop_layout)
    parent.this_widget.setStyleSheet('background: transparent')

    # parent.planet_widget = Planet3DWidget()
    # parent.backdrop_layout.addWidget(parent.planet_widget)
    parent.overlay_widget = create_overlay_layout(parent)

    parent.stackedWidget.addWidget(parent.this_widget)

def create_overlay_layout(parent):
    # Overlay container
    overlay_layout = QVBoxLayout()
    overlay_layout.setContentsMargins(10, 10, 10, 10)
    overlay_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    overlay_frame = QFrame()
    overlay_frame.setStyleSheet("""
        QFrame {
            background-color: rgba(0, 0, 0, 0);  /* Semi-transparent black */
            border-radius: 10px;
        }
    """)
    overlay_frame.setFixedWidth(300)  # Set a fixed width for the overlay

    overlay_content_layout = QVBoxLayout()
    overlay_content_layout.setContentsMargins(10, 10, 10, 10)
    overlay_content_layout.setSpacing(10)

    overlay_label = QLabel("Space Simulator")
    overlay_label.setStyleSheet("color: white; font-size: 32px;")
    overlay_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    new_game_button = QPushButton("New Game")
    new_game_button.setStyleSheet("""
        QPushButton {
            background-color: rgba(255, 255, 255, 10);  /* Semi-transparent white */
            border: 1px solid rgba(255, 255, 255, 80);  /* Light border for the glass effect */
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
            color: white;  /* Text color */
        }
        QPushButton:hover {
            background-color: rgba(155, 155, 255, 20);  /* Slightly brighter on hover */
        }
    """)
    new_game_button.clicked.connect(parent.newGamePressed)

    load_game_button = QPushButton("Load Game")
    load_game_button.setStyleSheet("""
        QPushButton {
            background-color: rgba(255, 255, 255, 10);  /* Semi-transparent white */
            border: 1px solid rgba(255, 255, 255, 80);  /* Light border for the glass effect */
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
            color: white;  /* Text color */
        }
        QPushButton:hover {
            background-color: rgba(155, 155, 255, 20);  /* Slightly brighter on hover */
        }
    """)
    load_game_button.clicked.connect(parent.loadGamePressed)

    settings_button = QPushButton("Settings")
    settings_button.setStyleSheet("""
        QPushButton {
            background-color: rgba(255, 255, 255, 10);  /* Semi-transparent white */
            border: 1px solid rgba(255, 255, 255, 80);  /* Light border for the glass effect */
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
            color: white;  /* Text color */
        }
        QPushButton:hover {
            background-color: rgba(155, 155, 255, 20);  /* Slightly brighter on hover */
        }
    """)

    exit_button = QPushButton("Quit Game")
    exit_button.setStyleSheet("""
        QPushButton {
            background-color: rgba(255, 255, 255, 10);  /* Semi-transparent white */
            border: 1px solid rgba(255, 255, 255, 80);  /* Light border for the glass effect */
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
            color: white;  /* Text color */
        }
        QPushButton:hover {
            background-color: rgba(155, 155, 255, 20);  /* Slightly brighter on hover */
        }
    """)

    overlay_content_layout = QVBoxLayout()
    overlay_content_layout.setContentsMargins(10, 10, 10, 10)
    overlay_content_layout.setSpacing(10)

    overlay_content_layout.addWidget(overlay_label)
    overlay_content_layout.addStretch(1)
    overlay_content_layout.addWidget(new_game_button)
    overlay_content_layout.addWidget(load_game_button)
    overlay_content_layout.addWidget(settings_button)
    overlay_content_layout.addWidget(exit_button)
    overlay_content_layout.addStretch()

    overlay_frame.setLayout(overlay_content_layout)
    overlay_layout.addWidget(overlay_frame)

    overlay_widget = QWidget(parent.this_widget)
    overlay_widget.setLayout(overlay_layout)
    overlay_widget.setGeometry(110, parent.height()-400, 300, 500)  # Initial position
    overlay_widget.show()

    return overlay_widget

def createHomePage(parent):
    home_page = QGridLayout()
    home_page.setContentsMargins(0, 0, 0, 0)
    parent.tabWidget = QTabWidget()
    parent.tabWidget.setStyleSheet(f"""
        QTabWidget::pane {{
            border: 0;
            border-radius: 0px;
            border-top: 1px solid #818181;
            margin: 0px;
            }}
    """)
    parent.map_tab = QWidget()
    parent.buildings_tab = QWidget()
    parent.tab2 = QWidget()
    parent.tab3 = QWidget()
    parent.tab4 = QWidget()
    tabIndex0 = parent.tabWidget.addTab(parent.map_tab, "Galaxy")
    tabIndex1 = parent.tabWidget.addTab(parent.buildings_tab, "Planet")
    tabIndex2 = parent.tabWidget.addTab(parent.tab2, "Research")
    tabIndex3 = parent.tabWidget.addTab(parent.tab3, "Stats")
    tabIndex4 = parent.tabWidget.addTab(parent.tab4, "Settings")
    parent.tabWidget.setTabIcon(tabIndex0, QIcon(parent.resources.resource_path("assets/icons/galaxy.png")))
    parent.tabWidget.setTabIcon(tabIndex1, QIcon(parent.resources.resource_path("assets/icons/planet.png")))
    parent.tabWidget.setTabIcon(tabIndex2, QIcon(parent.resources.resource_path("assets/icons/research.png")))
    parent.tabWidget.setTabIcon(tabIndex3, QIcon(parent.resources.resource_path("assets/icons/stats.png")))
    parent.tabWidget.setTabIcon(tabIndex4, QIcon(parent.resources.resource_path("assets/gear.png")))
    parent.tabWidget.setIconSize(QSize(32, 32))

    parent.map_tab.setLayout(galaxy_map_ui(parent))
    parent.buildings_tab.setLayout(interactive_map_stacked_widget(parent))
    parent.tab2.setLayout(ui2(parent))
    parent.tab3.setLayout(ui3(parent))
    parent.tab4.setLayout(ui_settings(parent))
    parent.tabWidget.currentChanged.connect(parent.tab_changed)

    h = QHBoxLayout()

    def create_resource_group(label_text, label_var, label_rate):
        group_box = QGroupBox(label_text)
        group_box.setStyleSheet('font-size: 14px; margin-left:10px; background: transparent')
        layout = QHBoxLayout()
        
        # resource_label = QLabel(label_text)
        # resource_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # layout.addWidget(resource_label)
        
        label_var.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label_var)
        
        label_rate.setAlignment(Qt.AlignmentFlag.AlignRight)
        label_rate.setStyleSheet(f"color: {parent.resources.colors['light-text']}")
        layout.addWidget(label_rate)
        
        group_box.setLayout(layout)
        return group_box

    parent.resource_labels = {}
    parent.resource_rate_labels = {}

    for resource, amount in parent.resources.data['resources'].items():
        if amount > 0:
            parent.resource_labels[resource] = QLabel(str(amount))
            parent.resource_rate_labels[resource] = QLabel(f"{parent.resources.data['resource_rates'].get(resource, 0)}/s")

    parent.resource_groups = {}

    for resource in parent.resource_labels:
        parent.resource_groups[resource] = create_resource_group(f"{resource.capitalize()}:", parent.resource_labels[resource], parent.resource_rate_labels[resource])
        h.addWidget(parent.resource_groups[resource])

    # home_page.addWidget(resource_bar, 0, 0, 1, 4)
    home_page.addLayout(h, 0, 0, 1, 4)
    home_page.addWidget(parent.tabWidget, 1, 0, 1, 4)
    home_page.setRowStretch(0,0)
    home_page.setRowStretch(1,1)

    home_page_widget = QWidget()
    home_page_widget.setLayout(home_page)
    parent.stackedWidget.addWidget(home_page_widget)

def interactive_map_stacked_widget(parent):
    from collections import OrderedDict

    parent.buildings_view_switch = QStackedWidget(parent)
    pages = OrderedDict([
        ("Map", map_ui),
        ("Base", base_page),
        ("Miner", mining_page),
        ("Housing", housing_page),
        ("Refinery", refinery_page),
        ("Merchant's Guild", merchants_page),
        ("Assembler", assembler_page),
        ("Manufacturer", manufacturer_page),
        ("Smelter", smelter_page),
    ])
    parent.tab_lookup_table = {name: i for i, name in enumerate(pages)}

    for page_func in pages.values():
        layout = page_func(parent)
        widget = QWidget()
        widget.setLayout(layout)
        parent.buildings_view_switch.addWidget(widget)

    interactive_layout = QVBoxLayout()
    interactive_layout.addWidget(parent.buildings_view_switch)
    return interactive_layout

def galaxy_map_ui(parent):
    # Create the main layout
    layout = QVBoxLayout(parent)

    # Create graphics scene and view
    scene_size = 1080
    scene = QGraphicsScene(-scene_size//2, -scene_size//2, scene_size, scene_size)
    view = QGraphicsView(scene)
    # view.setFixedSize(scene_size + 2, scene_size + 2)

    # Add central star
    star_radius = int(scene_size/20)
    star = QGraphicsEllipseItem(-star_radius, -star_radius, star_radius*2, star_radius*2)
    star.setBrush(QBrush(QColor("yellow")))
    scene.addItem(star)

    # Add 8 orbiting planets
    planet_radius = int(scene_size/33)
    orbit_radius = int(scene_size/4)
    for i in range(8):
        angle_deg = i * (360 / 8)
        angle_rad = math.radians(angle_deg)
        x = math.cos(angle_rad) * orbit_radius
        y = math.sin(angle_rad) * orbit_radius

        # Create a clickable button as the planet
        planet_button = QPushButton(f"P{i+1}")
        planet_button.setFixedSize(30, 30)
        proxy = QGraphicsProxyWidget()
        proxy.setWidget(planet_button)
        proxy.setPos(QPointF(x - planet_button.width()/2, y - planet_button.height()/2))
        scene.addItem(proxy)

    # Add the view to the layout
    layout.addWidget(view)
    return layout

def map_ui(parent):
    layout = QGridLayout()
    layout.setColumnStretch(0, 4)
    layout.setColumnStretch(1, 1)

    parent.map_viewer = MapViewer(parent=parent) # Setup takes a few seconds
    
    parent.right_gb = QGroupBox()
    parent.right_gb.setFixedWidth(400)
    parent.right_gb.setStyleSheet('''QGroupBox {
                            background: transparent;
                            font-size: 18px;
                            font-weight: bold;
                            padding: 0px;
                            border-radius: 10px;
                            border: 1px solid #1e1e1e;
                            margin: 0px;
                        }''')

    parent.building_info_right_panel = QStackedWidget(parent.right_gb)
    tmp = QGridLayout(parent.right_gb)
    tmp.addWidget(parent.building_info_right_panel)

    upgrade_layout = QGridLayout()
    parent.buildings_title = QLabel()
    parent.buildings_title.setStyleSheet("font-size: 22px; font-weight: bold")
    parent.buildings_info = QLabel("Select a plot")
    parent.buildings_cost = QLabel("Cost: ")
    parent.buildings_upgrade1 = QPushButton("")
    upgrade_layout.addWidget(parent.buildings_title, 0, 0, 1, 2, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
    upgrade_layout.addWidget(parent.buildings_info, 1, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
    upgrade_layout.addWidget(parent.buildings_cost, 2, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
    upgrade_layout.addWidget(parent.buildings_upgrade1, 3, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
    widget1 = QWidget()
    widget1.setLayout(upgrade_layout)
    parent.building_info_right_panel.addWidget(widget1)

    build_layout = QGridLayout()
    parent.buildings_title2 = QLabel("Build Menu")
    parent.buildings_title2.setStyleSheet("font-size: 22px; font-weight: bold")

    def create_building_widget(name, description, cost, icon_path, row):
        icon_label = QLabel()
        icon_label.setPixmap(QPixmap(icon_path).scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio))

        info_layout = QVBoxLayout()
        name_label = QLabel(name)
        name_label.setStyleSheet("font-size: 14px; font-weight: bold")
        description_label = QLabel(description)
        description_label.setStyleSheet("font-size: 10px; color: #818181")
        description_label.setWordWrap(True)
        info_layout.addWidget(name_label)
        info_layout.addWidget(description_label)

        cost_label = QLabel(f"Cost: {cost}")
        cost_label.setStyleSheet("font-size: 10px; color: #f7d68a")
        buy_button = QPushButton("Buy")
        buy_button.clicked.connect(lambda _, name=name: parent.map_viewer.buy_pressed(name))

        build_layout.addWidget(icon_label, row, 0, 1, 1)
        build_layout.addLayout(info_layout, row, 1, 1, 1)
        build_layout.addWidget(cost_label, row, 2, 1, 1)
        build_layout.addWidget(buy_button, row, 3, 1, 1)

    build_layout.addWidget(parent.buildings_title2, 0, 0, 1, 4, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)

    buildings_data = parent.resources.game_data["buildings"]
    for index, (building_name, building_info) in enumerate(buildings_data.items(), start=1):
        if building_name != "Base":
            icon_path = parent.resources.resource_path(building_info["icon"])
            cost = f"{building_info['build_cost']['gold']} Gold"
            create_building_widget(building_name, building_info["description"], cost, icon_path, index)

    build_layout.setColumnStretch(0, 1)
    build_layout.setColumnStretch(1, 3)
    build_layout.setColumnStretch(2, 3)
    build_layout.setColumnStretch(3, 3)
    build_layout.setRowStretch(0, 1)

    widget2 = QWidget()
    widget2.setLayout(build_layout)
    parent.building_info_right_panel.addWidget(widget2)

    layout.addWidget(parent.map_viewer, 0, 0, 1, 1)
    layout.addWidget(parent.right_gb, 0, 1, 1, 1)
    return layout

def base_page(parent):
    layout = QGridLayout()

    header_label = QLabel("Base Page")
    header_label.setStyleSheet("font-size: 24px;")
    header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    layout.addWidget(header_label, 0, 0, Qt.AlignmentFlag.AlignCenter)

    back_button = QPushButton("Back")
    back_button.clicked.connect(lambda: parent.buildings_view_switch.setCurrentIndex(0))
    layout.addWidget(back_button, 2, 0, Qt.AlignmentFlag.AlignLeft)

    layout.setRowStretch(0, 1)
    layout.setRowStretch(1, 4)

    parent.setLayout(layout)

    return layout

def mining_page(parent):
    layout = QGridLayout()

    header_label = QLabel("Mining Page")
    header_label.setStyleSheet("font-size: 24px;")
    header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    layout.addWidget(header_label, 0, 0, Qt.AlignmentFlag.AlignCenter)

    back_button = QPushButton("Back")
    back_button.clicked.connect(lambda: parent.buildings_view_switch.setCurrentIndex(0))
    layout.addWidget(back_button, 2, 0, Qt.AlignmentFlag.AlignLeft)

    layout.setRowStretch(0, 1)
    layout.setRowStretch(1, 4)

    parent.setLayout(layout)

    return layout

def housing_page(parent):
    layout = QGridLayout()

    header_label = QLabel("Housing Page")
    header_label.setStyleSheet("font-size: 24px;")
    header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    layout.addWidget(header_label, 0, 0, Qt.AlignmentFlag.AlignCenter)

    back_button = QPushButton("Back")
    back_button.clicked.connect(lambda: parent.buildings_view_switch.setCurrentIndex(0))
    layout.addWidget(back_button, 2, 0, Qt.AlignmentFlag.AlignLeft)

    layout.setRowStretch(0, 1)
    layout.setRowStretch(1, 4)

    parent.setLayout(layout)

    return layout

def refinery_page(parent):
    layout = QGridLayout()

    header_label = QLabel("Refinery Page")
    header_label.setStyleSheet("font-size: 24px;")
    header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    layout.addWidget(header_label, 0, 0, Qt.AlignmentFlag.AlignCenter)

    back_button = QPushButton("Back")
    back_button.clicked.connect(lambda: parent.buildings_view_switch.setCurrentIndex(0))
    layout.addWidget(back_button, 2, 0, Qt.AlignmentFlag.AlignLeft)

    layout.setRowStretch(0, 1)
    layout.setRowStretch(1, 4)

    parent.setLayout(layout)

    return layout

def merchants_page(parent):
    layout = QGridLayout()

    header_label = QLabel("Merchants Page")
    header_label.setStyleSheet("font-size: 24px;")
    header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    layout.addWidget(header_label, 0, 0, Qt.AlignmentFlag.AlignCenter)

    back_button = QPushButton("Back")
    back_button.clicked.connect(lambda: parent.buildings_view_switch.setCurrentIndex(0))
    layout.addWidget(back_button, 2, 0, Qt.AlignmentFlag.AlignLeft)

    layout.setRowStretch(0, 1)
    layout.setRowStretch(1, 4)

    parent.setLayout(layout)

    return layout

def assembler_page(parent):
    layout = QGridLayout()

    header_label = QLabel("Assembler Page")
    header_label.setStyleSheet("font-size: 24px;")
    header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    layout.addWidget(header_label, 0, 0, Qt.AlignmentFlag.AlignCenter)

    back_button = QPushButton("Back")
    back_button.clicked.connect(lambda: parent.buildings_view_switch.setCurrentIndex(0))
    layout.addWidget(back_button, 2, 0, Qt.AlignmentFlag.AlignLeft)

    layout.setRowStretch(0, 1)
    layout.setRowStretch(1, 4)

    parent.setLayout(layout)

    return layout

def manufacturer_page(parent):
    layout = QGridLayout()

    header_label = QLabel("Manufacturer Page")
    header_label.setStyleSheet("font-size: 24px;")
    header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    layout.addWidget(header_label, 0, 0, Qt.AlignmentFlag.AlignCenter)

    back_button = QPushButton("Back")
    back_button.clicked.connect(lambda: parent.buildings_view_switch.setCurrentIndex(0))
    layout.addWidget(back_button, 2, 0, Qt.AlignmentFlag.AlignLeft)

    layout.setRowStretch(0, 1)
    layout.setRowStretch(1, 4)

    parent.setLayout(layout)

    return layout

def smelter_page(parent):
    layout = QGridLayout()

    header_label = QLabel("Smelter Page")
    header_label.setStyleSheet("font-size: 24px;")
    header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    layout.addWidget(header_label, 0, 0, Qt.AlignmentFlag.AlignCenter)

    back_button = QPushButton("Back")
    back_button.clicked.connect(lambda: parent.buildings_view_switch.setCurrentIndex(0))
    layout.addWidget(back_button, 2, 0, Qt.AlignmentFlag.AlignLeft)

    layout.setRowStretch(0, 1)
    layout.setRowStretch(1, 4)

    parent.setLayout(layout)

    return layout

def ui2(parent):
    layout = QVBoxLayout()
    
    parent.progressBars = [QProgressBar(parent) for _ in range(5)]

    for index, progressBar in enumerate(parent.progressBars):
        progressBar.setRange(0, 100)
        progressBar.setValue(0)
        layout.addWidget(progressBar)
    
    parent.timers = [QTimer(parent) for _ in range(5)]
    speeds = [50, 200, 300, 400, 500]

    for index, timer in enumerate(parent.timers):
        timer.timeout.connect(partial(parent.updateProgressBar, index))
        timer.start(speeds[index])

    return layout

def ui3(parent):
    layout = QGridLayout()
    parent.graphWidget = pg.PlotWidget()
    parent.graphWidget.setBackground('transparent')
    parent.graphWidget.getAxis('left').setStyle(showValues=False)
    parent.graphWidget.getAxis('bottom').setStyle(showValues=False)
    label = QLabel("People/Gold/Resources over Time")
    label.setStyleSheet("font-size: 32px;")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(label, 0, 0, 1, 2)
    layout.addWidget(parent.graphWidget, 1, 0, 1, 2)
    layout.setRowStretch(0, 1)
    layout.setRowStretch(1, 3)
    
    parent.x = list(range(200))
    parent.y = [random.uniform(0, 50) for _ in range(200)]
    parent.y2 = [random.uniform(25, 75) for _ in range(200)]
    parent.y3 = [random.uniform(50, 100) for _ in range(200)]

    parent.data_line = parent.graphWidget.plot(parent.x, parent.y, pen=pg.mkPen(color='#8AB4F7', width=2), antialias=True)
    parent.data_line2 = parent.graphWidget.plot(parent.x, parent.y2, pen=pg.mkPen(color='#f78af1', width=2), antialias=True)
    parent.data_line3 = parent.graphWidget.plot(parent.x, parent.y3, pen=pg.mkPen(color='#f7c28a', width=2), antialias=True)

    def update_plot_data():
        parent.x = parent.x[1:]
        parent.x.append(parent.x[-1] + 1)

        parent.y = parent.y[1:]
        parent.y.append(random.uniform(0, 50))

        parent.y2 = parent.y2[1:]
        parent.y2.append(random.uniform(25, 75))

        parent.y3 = parent.y3[1:]
        parent.y3.append(random.uniform(50, 100))

        parent.data_line.setData(parent.x, parent.y)
        parent.data_line2.setData(parent.x, parent.y2)
        parent.data_line3.setData(parent.x, parent.y3)

    parent.timer = QTimer()
    parent.timer.setInterval(500)
    parent.timer.timeout.connect(update_plot_data)
    parent.timer.start()
    return layout

def ui_settings(parent):
    layout = QVBoxLayout()

    generalSettings = QGroupBox("General Settings")
    generalLayout = QGridLayout()
    generalSettings.setLayout(generalLayout)
    generalSettings.setStyleSheet("QGroupBox { border: 1px solid #f7918a; padding: 10px; font-size: 18px}")

    generalLayout.addWidget(QLabel('Test Timeout (s):'), 1, 0)
    test_timeout = QSpinBox()
    test_timeout.setRange(1, 3600)
    test_timeout.setValue(60)
    generalLayout.addWidget(test_timeout, 1, 1)

    generalLayout.addWidget(QLabel('Retry Count:'), 1, 2)
    retry_count = QSpinBox()
    retry_count.setRange(0, 10)
    retry_count.setValue(3)
    generalLayout.addWidget(retry_count, 1, 3)

    generalLayout.addWidget(QLabel('Log Level:'), 2, 0)
    log_level = QComboBox()
    log_level.addItems(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    log_level.setCurrentText('INFO')
    generalLayout.addWidget(log_level, 2, 1)

    generalLayout.addWidget(QLabel('Save Logs to File:'), 2, 2)
    save_logs = QCheckBox()
    save_logs.setChecked(True)
    generalLayout.addWidget(save_logs, 2, 3)

    generalLayout.addWidget(QLabel('Output Directory:'), 3, 0)
    parent.output_dir = QLineEdit()
    parent.output_dir.setText(os.getcwd())
    generalLayout.addWidget(parent.output_dir, 3, 1, 1, 1)

    # upload_button = QPushButton('Browse')
    # upload_button.setStyleSheet('padding: 5px;')
    # generalLayout.addWidget(upload_button, 3, 2, 1, 2)
    # upload_button.clicked.connect(parent.browse)
    # layout.addWidget(generalSettings)

    label = QLabel("Adjust Font Size")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    # generalLayout.addWidget(label, 4, 0, 1, 1)

    parent.slider = QSlider(Qt.Orientation.Horizontal)
    parent.slider.setMinimum(12)
    parent.slider.setMaximum(32)
    parent.slider.setValue(18)
    parent.slider.valueChanged.connect(parent.adjust_font_size)
    # generalLayout.addWidget(parent.slider, 4, 1, 1, 2)

    parent.font_label = QLabel("18px")
    # generalLayout.addWidget(parent.font_label, 4, 3, 1, 1)

    displaySettings = QGroupBox("Display Settings")
    displayLayout = QGridLayout()
    displaySettings.setLayout(displayLayout)
    displaySettings.setStyleSheet("QGroupBox { border: 1px solid #f7c28a; padding: 10px; font-size: 18px}")

    displayLayout.addWidget(QLabel('Resolution:'), 1, 0)
    parent.resolution_select = QComboBox()
    resolution_options = ['1080x720', '1280x720', '1366x768', '1600x900', '1920x1080', '2560x1440', '3840x2160']
    parent.resolution_select.addItems(resolution_options)
    parent.resolution_select.setCurrentText('1920x1080')
    parent.resolution_select.currentTextChanged.connect(parent.adjust_resolution)
    displayLayout.addWidget(parent.resolution_select, 1, 1, 1, 2)

    displayLayout.addWidget(QLabel('Fullscreen:'), 2, 0)
    parent.fullscreen_checkbox = QCheckBox()
    parent.fullscreen_checkbox.setChecked(False)
    parent.fullscreen_checkbox.stateChanged.connect(parent.toggle_fullscreen)
    displayLayout.addWidget(parent.fullscreen_checkbox, 2, 1, 1, 2, Qt.AlignmentFlag.AlignLeft)

    layout.addWidget(displaySettings)

    testSettings = QGroupBox("Test Settings")
    testLayout = QGridLayout()
    testSettings.setLayout(testLayout)
    testSettings.setStyleSheet("QGroupBox { border: 1px solid #f6f78a; padding: 10px; font-size: 18px}")

    testLayout.addWidget(QLabel('OneFactory Automatic Upload:'), 1, 0)
    one_factory = QCheckBox()
    one_factory.setChecked(False)
    testLayout.addWidget(one_factory, 1, 1)

    testLayout.addWidget(QLabel('Max Concurrent Tests:'), 1, 2)
    max_concurrent_tests = QSpinBox()
    max_concurrent_tests.setRange(1, 20)
    max_concurrent_tests.setValue(5)
    testLayout.addWidget(max_concurrent_tests, 2, 3)

    testLayout.addWidget(QLabel('Test Priority Level:'), 2, 0)
    test_priority = QComboBox()
    test_priority.addItems(['Low', 'Medium', 'High'])
    test_priority.setCurrentText('Medium')
    testLayout.addWidget(test_priority, 2, 1)

    testLayout.addWidget(QLabel('Save Test Report:'), 2, 2)
    save_test_report = QCheckBox()
    save_test_report.setChecked(True)
    testLayout.addWidget(save_test_report, 1, 3)

    testLayout.addWidget(QLabel('Test Script Path:'), 3, 0)
    test_script_path = QLineEdit()
    test_script_path.setText('/path/to/test/script')
    testLayout.addWidget(test_script_path, 3, 1, 1, 3)

    layout.addWidget(testSettings)

    proxySettings = QGroupBox("Proxy Settings")
    proxyLayout = QGridLayout()
    proxySettings.setLayout(proxyLayout)
    proxySettings.setStyleSheet("QGroupBox { border: 1px solid #8af7b4; padding: 10px; font-size: 18px}")

    proxyLayout.addWidget(QLabel('Use Proxy Server:'), 1, 0)
    use_proxy = QCheckBox()
    use_proxy.setChecked(False)
    proxyLayout.addWidget(use_proxy, 1, 1)

    proxyLayout.addWidget(QLabel('Proxy Server Address:'), 2, 0)
    proxy_address = QLineEdit()
    proxy_address.setText('')
    proxyLayout.addWidget(proxy_address, 2, 1, 1, 3)

    layout.addWidget(proxySettings)

    debugSettings = QGroupBox("Debug Settings")
    debugLayout = QGridLayout()
    debugSettings.setLayout(debugLayout)
    debugSettings.setStyleSheet("QGroupBox { border: 1px solid #c58af7; padding: 10px; font-size: 18px}")

    debugLayout.addWidget(QLabel('Enable Debug Mode:'), 1, 0)
    enable_debug = QCheckBox()
    enable_debug.setChecked(False)
    debugLayout.addWidget(enable_debug, 1, 1)

    layout.addWidget(debugSettings)

    save_settings = QPushButton('Save Settings')
    layout.addWidget(save_settings)
    save_settings.setStyleSheet("background: #8AB4F7; border: 1px solid #8AB4F7; color: #202124")

    return layout

# def galaxy_ui(parent):
#     backdrop_layout = QVBoxLayout()
#     backdrop_layout.setContentsMargins(0, 0, 0, 0)
#     backdrop_layout.setSpacing(0)

#     parent.planet_widget = Planet3DWidget()
#     backdrop_layout.addWidget(parent.planet_widget)
#     return backdrop_layout