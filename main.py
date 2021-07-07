import sys
import os

import qrcode_wifi
import qr_result


from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtWidgets

set_class = uic.loadUiType('set.ui')[0]
Qrtest_class = uic.loadUiType("camtest.ui")[0]

wificode ='' 
class MyWindow(QMainWindow, set_class):    
    def __init__(self):
        
        super().__init__()
        self.setupUi(self) 
        self.setWindowTitle("Hoseo Unviersity - IR LAB")

        self.qrcode_btn.clicked.connect(self.btn_connect) 
    
    def btn_connect(self): #이벤트 함수
        global wificode
        wificode = qrcode_wifi.start() 
        print(wificode)      
        if wificode is not None:
            setwindow = Set_Window() 
            widget.addWidget(setwindow) #1
            widget.setCurrentIndex(widget.currentIndex()+1) # 다음화면으로 넘김 > qr내용 출력 화면
        
class Set_Window(QMainWindow, Qrtest_class):        
    def __init__(self):
        global wificode
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Hoseo Unviersity - IR LAB")       
        self.qr_label.setText(str(qr_result.result(wificode)))
        self.qr_btn_yes.clicked.connect(lambda state, button=self.qr_btn_yes: self.btn_connect(state, button))
        self.qr_btn_no.clicked.connect(lambda state, button=self.qr_btn_no: self.btn_connect(state, button))
    
    def btn_connect(self, state, button):
        if button==self.qr_btn_yes:
            qr_result.CreateWifiConfig(ssid, password)
        elif button==self.qr_btn_no:
            print('no버튼 클릭')
            widget.setCurrentIndex(widget.currentIndex()-1) 

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    widget= QtWidgets.QStackedWidget()

    mainwindow = MyWindow() # 첫 화면

    widget.addWidget(mainwindow) #0
    widget.setFixedHeight(480)  
    widget.setFixedWidth(800)   
    widget.show()

    app.exec_()
    