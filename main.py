import sys
import os

import qrcode_wifi

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtWidgets

#리소스 파일 사용시 resource_path()사용해서 절대경로로 변경
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


set_class = uic.loadUiType(resource_path('set.ui'))[0]
Qrtest_class = uic.loadUiType(resource_path("camtest.ui"))[0]


class MyWindow(QMainWindow, set_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Hoseo Unviersity - IR LAB")

        self.qrcode_btn.clicked.connect(self.btn_connect)
    
    def btn_connect(self):
        wificode = qrcode_wifi.start()
        print(wificode)

class Set_Window(QMainWindow, Qrtest_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Hoseo Unviersity - IR LAB")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget= QtWidgets.QStackedWidget()

    mainwindow = MyWindow()
    setwindow = Set_Window()

    widget.addWidget(mainwindow)
    widget.addWidget(setwindow)
    widget.setFixedHeight(480)
    widget.setFixedWidth(800)
    widget.show()

    app.exec_()
    