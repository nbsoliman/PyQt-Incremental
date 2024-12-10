from resources.ResourceManager import ResourceManager
from resources.ScrollableGrid import ScrollableGrid
from resources.Space3D import Planet3DWidget
import qdarktheme
import json, os, sys, traceback, re, random
from functools import partial
import pyqtgraph as pg
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

colors = {
            "bg": "#272727",
            "bg-darker": "#1e1e1e",
            "light-text": "#818181",
            "red": "#f7918a",
            "orange": "#f7c28a",
            "orellow": "#f7d68a",
            "yellow": "#f6f78a",
            "green": "#8af7b4",
            "blue": "#8AB4F7",
            "purple": "#c58af7",
            "pink": "#f78af1",
        }

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    info = pyqtSignal(object)

class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        self.kwargs['info_callback'] = self.signals.info

    @pyqtSlot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()

class MainUI(QWidget):
    def __init__(self):
        super().__init__()
        self.resources = ResourceManager()
        self.setWindowTitle("GUI")
        self.resize(250,150)
        self.stackedWidget = QStackedWidget(self)
        self.createMainMenu()

        self.stackedWidget.setCurrentIndex(0)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stackedWidget)
        main_layout.setContentsMargins(0, 20, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

    def createMainMenu(self):
        main_menu = QVBoxLayout()
        main_menu.addWidget(QLabel("Main Menu", alignment=Qt.AlignmentFlag.AlignCenter))
        new_game_button = QPushButton("New")
        new_game_button.clicked.connect(self.newGamePressed)
        main_menu.addWidget(new_game_button)
        load_game_button = QPushButton('Load')
        load_game_button.clicked.connect(self.loadGamePressed)
        main_menu.addWidget(load_game_button)

        main_menu_widget = QWidget()
        main_menu_widget.setLayout(main_menu)
        self.stackedWidget.addWidget(main_menu_widget)

    def createHomePage(self):
        home_page = QGridLayout()
        home_page.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget()
        self.tabWidget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 0;
                border-radius: 0px;
                border-top: 1px solid #1e1e1e;
                margin: 0px;
                }}
        """)
        self.galaxy_tab = QWidget()
        self.buildings_tab = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        tabIndex0 = self.tabWidget.addTab(self.galaxy_tab, "Galaxy")
        tabIndex1 = self.tabWidget.addTab(self.buildings_tab, "Buildings")
        tabIndex2 = self.tabWidget.addTab(self.tab2, "Research")
        tabIndex3 = self.tabWidget.addTab(self.tab3, "Graphs")
        tabIndex4 = self.tabWidget.addTab(self.tab4, "Settings")
        self.tabWidget.setTabIcon(tabIndex0, QIcon(self.resources.resource_path("assets/home.png")))
        self.tabWidget.setTabIcon(tabIndex1, QIcon(self.resources.resource_path("assets/home.png")))
        self.tabWidget.setTabIcon(tabIndex2, QIcon(self.resources.resource_path("assets/list-check.png")))
        self.tabWidget.setTabIcon(tabIndex3, QIcon(self.resources.resource_path("assets/graph-up.png")))
        self.tabWidget.setTabIcon(tabIndex3, QIcon(self.resources.resource_path("assets/graph-up.png")))
        self.tabWidget.setTabIcon(tabIndex4, QIcon(self.resources.resource_path("assets/gear.png")))
        self.tabWidget.setIconSize(QSize(32, 32))

        self.galaxy_tab.setLayout(self.galaxy_ui())
        self.buildings_tab.setLayout(self.buildings_ui())
        self.tab2.setLayout(self.ui2())
        self.tab3.setLayout(self.ui3())
        self.tab4.setLayout(self.ui_settings())
        self.tabWidget.currentChanged.connect(self.tab_changed)

        # resource_bar = QGroupBox()
        # resource_bar.setObjectName("b1")
        # resource_bar.setStyleSheet('QWidget#b1 {background-color: #161718; background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #161718, stop:0.5 #1f2022, stop:1 #0e0e0f); font-size: 18px; font-weight: bold; padding: 10px; border-radius: 10px; border: 1px solid #f7d68a; margin: 10px; }')
        
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
            label_rate.setStyleSheet(f"color: {colors['light-text']}")
            layout.addWidget(label_rate)
            
            group_box.setLayout(layout)
            return group_box

        self.people_label = QLabel(str(self.resources.data['resources']['people']))
        self.gold_label = QLabel(str(self.resources.data['resources']['gold']))
        self.wood_label = QLabel(str(self.resources.data['resources']['wood']))
        self.stone_label = QLabel(str(self.resources.data['resources']['stone']))
        
        self.gold_label_rate = QLabel('0/s')
        self.wood_label_rate = QLabel('0/s')
        self.stone_label_rate = QLabel('0/s')
        self.people_label_rate = QLabel('0/s')

        people_group = create_resource_group("People:", self.people_label, self.people_label_rate)
        gold_group = create_resource_group("Gold:", self.gold_label, self.gold_label_rate)
        wood_group = create_resource_group("Wood:", self.wood_label, self.wood_label_rate)
        stone_group = create_resource_group("Stone:", self.stone_label, self.stone_label_rate)

        h.addWidget(people_group)
        h.addWidget(gold_group)
        h.addWidget(wood_group)
        h.addWidget(stone_group)
        # resource_bar.setLayout(h)

        # home_page.addWidget(resource_bar, 0, 0, 1, 4)
        home_page.addLayout(h, 0, 0, 1, 4)
        home_page.addWidget(self.tabWidget, 1, 0, 1, 4)
        home_page.setRowStretch(0,0)
        home_page.setRowStretch(1,1)

        home_page_widget = QWidget()
        home_page_widget.setLayout(home_page)
        self.stackedWidget.addWidget(home_page_widget)

    def galaxy_ui(self):
        backdrop_layout = QVBoxLayout()
        backdrop_layout.setContentsMargins(0, 0, 0, 0)
        backdrop_layout.setSpacing(0)

        self.planet_widget = Planet3DWidget()
        backdrop_layout.addWidget(self.planet_widget)
        return backdrop_layout
        
    def buildings_ui(self):
        buildings_layout = QVBoxLayout()
        buildings_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area = ScrollableGrid(bg_filename=self.resources.resource_path("assets/planet1.jpg"), parent=self)
        scroll_area_widget = QWidget()
        grid_layout = QGridLayout(scroll_area_widget)
        # grid_layout.setSpacing(0)
        grid_layout.setHorizontalSpacing(20)
        grid_layout.setVerticalSpacing(10)

        for i in range(21):
            for j in range(21):
                t = QGroupBox()
                t.setFixedHeight(100)
                t.setFixedWidth(100)
                v = QVBoxLayout()
                building_found = False
                for building, details in self.resources.data['buildings'].items():
                    # print(building,':',details)
                    if details['location']['x'] == i and details['location']['y'] == j:
                        t.setStyleSheet('QWidget#b1 { border: 1px solid #f7d68a; padding:10px; background: #1e1e1e}')
                        label = QLabel(building)
                        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        v.addWidget(label)
                        button = QPushButton(f'Upgrade', scroll_area_widget)
                        v.addWidget(button)
                        building_found = True
                        break
                if not building_found:
                    t.setStyleSheet('QWidget#b1 { border: none; padding:10px;}')
                    button = QPushButton(f'Build', scroll_area_widget)
                    button.setStyleSheet(f"border: none; background: transparent; color: {colors['light-text']}")
                    v.addWidget(button)
                t.setLayout(v)
                grid_layout.addWidget(t, i, j)

        self.scroll_area.setWidget(scroll_area_widget)
        buildings_layout.addWidget(self.scroll_area)
        
        QTimer.singleShot(0, self.centerScrollArea)
        return buildings_layout
    
    def ui2(self):
        layout = QVBoxLayout()
        
        self.progressBars = [QProgressBar(self) for _ in range(5)]

        for index, progressBar in enumerate(self.progressBars):
            progressBar.setRange(0, 100)
            progressBar.setValue(0)
            layout.addWidget(progressBar)
        
        self.timers = [QTimer(self) for _ in range(5)]
        speeds = [50, 200, 300, 400, 500]

        for index, timer in enumerate(self.timers):
            timer.timeout.connect(partial(self.updateProgressBar, index))
            timer.start(speeds[index])

        return layout

    def updateProgressBar(self, index):
        progressBar = self.progressBars[index]
        value = progressBar.value() + 1
        if value > 100:
            value = 0
        progressBar.setValue(value)

    def ui3(self):
        layout = QGridLayout()
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground('#202124')
        self.graphWidget.getAxis('left').setStyle(showValues=False)
        self.graphWidget.getAxis('bottom').setStyle(showValues=False)
        label = QLabel("People/Gold/Resources over Time")
        label.setStyleSheet("font-size: 32px;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label, 0, 0, 1, 2)
        layout.addWidget(self.graphWidget, 1, 0, 1, 2)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 3)
        
        self.x = list(range(200))
        self.y = [random.uniform(0, 50) for _ in range(200)]
        self.y2 = [random.uniform(25, 75) for _ in range(200)]
        self.y3 = [random.uniform(50, 100) for _ in range(200)]

        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pg.mkPen(color='#8AB4F7', width=2), antialias=True)
        self.data_line2 = self.graphWidget.plot(self.x, self.y2, pen=pg.mkPen(color='#f78af1', width=2), antialias=True)
        self.data_line3 = self.graphWidget.plot(self.x, self.y3, pen=pg.mkPen(color='#f7c28a', width=2), antialias=True)

        def update_plot_data():
            self.x = self.x[1:]
            self.x.append(self.x[-1] + 1)

            self.y = self.y[1:]
            self.y.append(random.uniform(0, 50))

            self.y2 = self.y2[1:]
            self.y2.append(random.uniform(25, 75))

            self.y3 = self.y3[1:]
            self.y3.append(random.uniform(50, 100))

            self.data_line.setData(self.x, self.y)
            self.data_line2.setData(self.x, self.y2)
            self.data_line3.setData(self.x, self.y3)

        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(update_plot_data)
        self.timer.start()
        return layout
    
    def ui_settings(self):
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
        self.output_dir = QLineEdit()
        self.output_dir.setText(os.getcwd())
        generalLayout.addWidget(self.output_dir, 3, 1, 1, 1)

        # upload_button = QPushButton('Browse')
        # upload_button.setStyleSheet('padding: 5px;')
        # generalLayout.addWidget(upload_button, 3, 2, 1, 2)
        # upload_button.clicked.connect(self.browse)
        # layout.addWidget(generalSettings)

        label = QLabel("Adjust Font Size")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # generalLayout.addWidget(label, 4, 0, 1, 1)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(12)
        self.slider.setMaximum(32)
        self.slider.setValue(18)
        self.slider.valueChanged.connect(self.adjust_font_size)
        # generalLayout.addWidget(self.slider, 4, 1, 1, 2)

        self.font_label = QLabel("18px")
        # generalLayout.addWidget(self.font_label, 4, 3, 1, 1)

        notificationSettings = QGroupBox("Notification Settings")
        notificationLayout = QGridLayout()
        notificationSettings.setLayout(notificationLayout)
        notificationSettings.setStyleSheet("QGroupBox { border: 1px solid #f7c28a; padding: 10px; font-size: 18px}")

        notificationLayout.addWidget(QLabel('Enable Notifications:'), 1, 2)
        enable_notifications = QCheckBox()
        enable_notifications.setChecked(True)
        notificationLayout.addWidget(enable_notifications, 1, 3)

        notificationLayout.addWidget(QLabel('Recipients:'), 1, 0)
        notification_recipients = QLineEdit()
        notification_recipients.setText('nicholas.soliman@gmail.com')
        notificationLayout.addWidget(notification_recipients, 1, 1)

        layout.addWidget(notificationSettings)

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
    
    def adjust_font_size(self, value):
        font = self.mainWidget.font()
        font.setPointSize(value)
        for widget in self.mainWidget.findChildren((QLabel, QPushButton)):
            print(widget,":",value)
            widget.setFont(font)
        self.font_label.setText(str(value)+"px")

    def centerScrollArea(self):
        scroll_area_widget = self.scroll_area.widget()
        center_x = (scroll_area_widget.sizeHint().width() - self.scroll_area.viewport().width()) // 2
        center_y = (scroll_area_widget.sizeHint().height() - self.scroll_area.viewport().height()) // 2
        
        self.scroll_area.horizontalScrollBar().setValue(center_x)
        self.scroll_area.verticalScrollBar().setValue(center_y)
    
    def newGamePressed(self):
        self.resources.create()
        self.createHomePage()
        self.stackedWidget.setCurrentIndex(1)
        self.resize(750,550)
        self.center()

        # QTimer.singleShot(100, lambda: self.stackedWidget.setCurrentIndex(1))
        # QTimer.singleShot(100, lambda: self.resize(750,550))
        # QTimer.singleShot(150, lambda: self.center())
    
    def loadGamePressed(self):
        self.resize(750,550)
        self.center()
        self.resources.load()
        self.createHomePage()
        self.stackedWidget.setCurrentIndex(1)

    def tab_changed(self, index):
        self.current_tab_index = index
        # if index == 0:
        #     self.titleLabel.setText("    Home")
        # if index == 1:
        #     self.titleLabel.setText("    Tab 1")
        # if index == 2:
        #     self.titleLabel.setText("    Settings")

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

app = QApplication(sys.argv)
app.setStyleSheet(qdarktheme.load_stylesheet())
window = MainUI()
window.show()
sys.exit(app.exec())