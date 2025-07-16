from resources.ResourceManager import ResourceManager
from resources.IdleThread import IdleThread
from resources.UI import *
import qdarktheme
import json, os, sys, traceback
from functools import partial
import pyqtgraph as pg
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

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
        self.idle_thread = IdleThread(self)

        self.setWindowTitle("GUI")
        self.setFixedSize(1600, 900)
        self.setMaximumSize(1600, 900)
        self.game_closed = False

        self.stackedWidget = QStackedWidget(self)
        self.stackedWidget.setCurrentIndex(0)
        self.setStyleSheet(f"""
            QWidget {{
                background: {self.resources.colors["dark-bg"]};
            }}
            QLabel {{
                background: transparent;
                font-size: 14px;
            }}
            QGroupBox#blue-border {{
                border: 2px solid {self.resources.colors["blue"]};
                border-radius: 6px;
            }}
            QGroupBox#orellow-border {{
                background: {self.resources.colors["near-black"]};
                border: 2px solid {self.resources.colors["orellow"]};
                border-radius: 6px;
            }}
            QGroupBox#grey-border {{
                background: {self.resources.colors["near-black"]};
                border: 2px solid {self.resources.colors["light-text"]};
                border-radius: 6px;
            }}
            QPushButton {{
                border: 2px solid {self.resources.colors["blue"]};
                background: {self.resources.colors["blue"]};
                color: {self.resources.colors["dark-bg"]};
                font-weight: bold;
                border-radius: 6px;
            }}
            QPushButton#disabled {{
                border: 2px solid {self.resources.colors["light-text"]};
                background: transparent;
                color: {self.resources.colors["light-text"]};
                font-weight: bold;
                border-radius: 6px;
            }}
            QScrollArea {{
                border: none;
            }}
        """)

        # For Testing Load Straight Into Game:
        self.newGamePressed()
        QTimer.singleShot(100, lambda: self.tabWidget.setCurrentIndex(1))

        # Or Title Screen
        # main_menu_ui(self)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stackedWidget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

    # def resizeevent(self, event):
    #     self.tabWidget.setStyleSheet(f"""
    #         QTabBar::tab:last {{
    #             margin-left: {self.size().width()-(121*4)}px;
    #         }}
    #     """)                

    def info_callback(self, data):
        if data[0] == "update-resource":
            self.resource_labels[data[1]].setText(str(data[2]))
            self.resource_rate_labels[data[1]].setText(f"{str(data[3])}/s")
        if data[0] == "not-enough-of-resource":
            self.resource_groups[data[1]].setStyleSheet(
            f'font-size: 14px; margin-left:10px; background: {self.resources.colors["red"]}')
            QTimer.singleShot(
                500,
                lambda: self.resource_groups[data[1]].setStyleSheet(
                    'font-size: 14px; margin-left:10px; background: transparent'
                )
            )  
    def updateProgressBar(self, index):
        progressBar = self.progressBars[index]
        value = progressBar.value() + 1
        if value > 100:
            value = 0
        progressBar.setValue(value)
    
    def adjust_font_size(self, value):
        font = self.mainWidget.font()
        font.setPointSize(value)
        for widget in self.mainWidget.findChildren((QLabel, QPushButton)):
            print(widget,":",value)
            widget.setFont(font)
        self.font_label.setText(str(value)+"px")

    def adjust_resolution(self):
        current_resolution = self.resolution_select.currentText()
        w = int(current_resolution.split("x")[0])
        h = int(current_resolution.split("x")[1])
        self.setFixedSize(w, h)
        self.setMaximumSize(w, h)
        self.center()

    def toggle_fullscreen(self):
        if self.fullscreen_checkbox.isChecked():
            self.showFullScreen()
        else:
            self.showNormal()
    
    def newGamePressed(self):
        self.resources.create()
        # self.resources.load()
        home_ui(self) # Takes long time due to MapViewer Creation
        self.stackedWidget.setCurrentIndex(1)
        self.center()

        # Start idle loop worker
        self.threadpool = QThreadPool()
        worker = Worker(self.idle_thread.start_loop)
        worker.signals.info.connect(self.info_callback)
        self.threadpool.start(worker)

        # self.planet_widget.toggle_autopan()
    
    def loadGamePressed(self):
        # self.resize(750,550)
        self.center()
        self.resources.load()
        home_ui(self)
        self.stackedWidget.setCurrentIndex(1)
        
        # Start idle loop worker
        self.threadpool = QThreadPool()
        worker = Worker(self.idle_thread.start_loop)
        worker.signals.info.connect(self.info_callback)
        self.threadpool.start(worker)

    def tab_changed(self, index):
        self.current_tab_index = index
        # if index == 0:
        #     self.titleLabel.setText("    Home")
        # if index == 1:
        #     QTimer.singleShot(0, self.centerScrollArea)
        # if index == 2:
        #     self.titleLabel.setText("    Settings")

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def resizeEvent(self, event):
        if hasattr(self, 'overlay_widget'):
            self.overlay_widget.setGeometry((self.width() - 300) // 2,(self.height() - 400) // 2,300,500)
        super().resizeEvent(event)

    def closeEvent(self, a0):
        self.game_closed = True
        return super().closeEvent(a0)

app = QApplication(sys.argv)
app.setStyleSheet(qdarktheme.load_stylesheet())
window = MainUI()
window.show()
sys.exit(app.exec())