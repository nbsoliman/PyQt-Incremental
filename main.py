from resources.ResourceManager import ResourceManager
from resources.UI.MainUI import *
import qdarktheme
import json, os, sys, traceback, re, random
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
        self.setWindowTitle("GUI")
        self.setFixedSize(1080, 720)
        self.setMaximumSize(1080, 720)
        self.stackedWidget = QStackedWidget(self)
        self.stackedWidget.setCurrentIndex(0)

        # For Testing Load Straight Into Game:
        self.newGamePressed()
        QTimer.singleShot(100, lambda: self.tabWidget.setCurrentIndex(1))

        # Or Title Screen
        # createMainMenu(self)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stackedWidget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

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

    def centerScrollArea(self):
        scroll_area_widget = self.scroll_area.widget()
        center_x = (scroll_area_widget.sizeHint().width() - self.scroll_area.viewport().width()) // 2
        center_y = (scroll_area_widget.sizeHint().height() - self.scroll_area.viewport().height()) // 2
        
        self.scroll_area.horizontalScrollBar().setValue(center_x)
        self.scroll_area.verticalScrollBar().setValue(center_y)
    
    def newGamePressed(self):
        self.resources.create()
        # self.resources.load()
        createHomePage(self) # Takes long time due to MapViewer Creation
        self.stackedWidget.setCurrentIndex(1)
        self.center()
        self.planet_widget.toggle_autopan()
    
    def loadGamePressed(self):
        # self.resize(750,550)
        self.center()
        self.resources.load()
        self.createHomePage()
        self.stackedWidget.setCurrentIndex(1)

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

app = QApplication(sys.argv)
app.setStyleSheet(qdarktheme.load_stylesheet())
window = MainUI()
window.show()
sys.exit(app.exec())