import sys
import os

import qrcode_wifi
import qr_result

from ver_check import version



import pywifi
from pywifi import *

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtWidgets

#리소스 파일 사용시 resource_path()사용해서 절대경로로 변경

set_class = uic.loadUiType('set.ui')[0]
Qrtest_class = uic.loadUiType("camtest.ui")[0]

wificode ='' # qr 내용 저장할 변수
class MyWindow(QMainWindow, set_class): #set.ui *첫 화면     
    def __init__(self):
        
        super().__init__()
        self.setupUi(self) # 화면 나오게 함
        self.setWindowTitle("Hoseo Unviersity - IR LAB") # 제목 표시줄

        self.qrcode_btn.clicked.connect(self.btn_connect) # 이벤트 연결
    
    def btn_connect(self): #이벤트 함수
        global wificode
        wificode = qrcode_wifi.start() 
        print(wificode) #wificode를 다음 창에 넘겨줘야함       
        print('mywindow의 인덱스', widget.currentIndex())      
        if wificode is not None: #값이 들어오면 다음 화면으로 넘어감
            setwindow = Set_Window() # qr인식 객체 생성
            a=widget.addWidget(setwindow) #index 1번
            print('setwindow 인덱스', a)
            widget.setCurrentIndex(widget.currentIndex()+1)
            
class Set_Window(QMainWindow, Qrtest_class):    # camtest.ui *qr내용 출력됨    
    def __init__(self):
        global wificode
        
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Hoseo Unviersity - IR LAB")       
        self.qr_label.setText(str(qr_result.result(wificode)))
        self.qr_btn_yes.clicked.connect(lambda state, button=self.qr_btn_yes: self.btn_connect(state, button))
        self.qr_btn_no.clicked.connect(lambda state, button=self.qr_btn_no: self.btn_connect(state, button))
    
    def btn_connect(self, state, button):
        if button==self.qr_btn_yes: #확인 이벤트
            qr_result.test() 
            #qr_result.CreateWifiConfig(ssid, password)
        elif button==self.qr_btn_no: #취소 이벤트
            print('no버튼 클릭')
            print(widget.count())
            print(widget.currentIndex())
            widget.removeWidget(widget.widget(1)) # widget stack에 생성된 index 1 위젯 삭제 
            widget.setCurrentIndex(0) 
            # 위젯스택 초기화
            
#재부팅되고 > 프로그램이 여기서 부터 실행되어야 함. 와이파이 연결(재부팅 결과)되어있으면 바로 api통신하고 버전검사 실행
class ver_window(version.ver): #버전 검사하는 클래스 
    def __init__(self): #여기에서 
        super(ver_window, self).__init__()
        version.ver.loading(self)#여기 self도 ver_window 인스턴스인가?
        
        
        
            
if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    widget= QtWidgets.QStackedWidget()
    
    #pywifi모듈 사용 시 wifi연결이 안되어 있으면  
    #widget에 mainwindow객체 추가
    #연결되어 있으면 verwindow객체 추가
    #재부팅 후 와이파이가 연결되어있으면 바로 버전검사 거쳐서 nfc통신 가능하도록!
    wifi= pywifi.PyWiFi()
    interface= wifi.interfaces()[0]
    
    if(interface.status()==const.IFACE_CONNECTED): #연결되었을 경우 > 바로 버전검사로 넘어감
        print('와이파이 연결 되었지롱')
        verwindow= ver_window()
        widget.addWidget(verwindow) # 첫 화면 index 0번    
    else: #연결되지 않았을 경우 > 와이파이 설정하는 것부터 시작됨
        mainwindow = MyWindow()
        widget.addWidget(mainwindow) # 첫 화면 index 0번
        
    widget.setFixedHeight(480)  
    widget.setFixedWidth(800)  
    widget.show()
    app.exec_()
    