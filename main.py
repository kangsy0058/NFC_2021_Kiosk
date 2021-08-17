import sys
import os
import subprocess #시스템 종료를 위한 'sh' 실행, 와이파이 연결 확인

import qrcode_wifi
import qr_result
from nfc import nfc

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap

#리소스 파일 사용시 resource_path()사용해서 절대경로로 변경
set_class = uic.loadUiType('/home/pi/nfc_2021_kiosk/set.ui')[0]
Qrtest_class = uic.loadUiType("/home/pi/nfc_2021_kiosk/camtest.ui")[0]


wificode ='' # qr 내용 저장할 변수

#와이파이 QR 입력 클래스 
class MyWindow(QMainWindow, set_class): #set.ui *첫 화면     
    def __init__(self):
        
        super().__init__()
        #화면 세팅
        self.setupUi(self) 
        self.setWindowTitle("Hoseo Unviersity - IR LAB") 
        
        #이벤트 연결
        self.qrcode_btn.clicked.connect(self.btn_connect) # QR버튼 클릭 이벤트
        
        self.power_btn.clicked.connect(self.btn_power)  # shutdown 클릭 이벤트
        self.reboot_btn.clicked.connect(self.btn_reboot)# reboot 클릭 이벤트
    
    def btn_connect(self):
        global wificode #와이파이QR 정보 저장
        
        wificode = qrcode_wifi.start()  # 리턴값: QR 해석
        print(wificode) 
        
        if wificode is not None: # 유효한 값이 들어오면 다음 화면으로 변경 
            setwindow = Set_Window() 
            a=widget.addWidget(setwindow) #index 1번
            print('setwindow 인덱스', a) 
            widget.setCurrentIndex(widget.currentIndex()+1) # setwindow으로 화면 전환

    def btn_power(self):
        subprocess.call('sudo shutdown',shell=True)
    def btn_reboot(self):
        subprocess.call('sudo reboot',shell=True)
        
# 와이파이 정보 화면 출력 및 재부팅        
class Set_Window(QMainWindow, Qrtest_class):    # camtest.ui *qr내용 출력됨    
    def __init__(self):
        global wificode, SSID, PWD
        # 화면 세팅
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Hoseo Unviersity - IR LAB")
        
        # 와이파이 정보 화면 출력함
        SSID, PWD = qr_result.result(wificode)  # 리턴값: ssid, password 
        self.qr_label.setText(str(SSID + PWD ))
        
        # 이벤트 연결
        self.qr_btn_yes.clicked.connect(lambda state, button=self.qr_btn_yes: self.btn_connect(state, button)) # 정보가 일치할 경우 ('확인 버튼 클릭')
        self.qr_btn_no.clicked.connect(lambda state, button=self.qr_btn_no: self.btn_connect(state, button)) # 정보가 일치하지 않을 경우 ('취소 버튼 클릭')
    
    def btn_connect(self, state, button):
        if button==self.qr_btn_yes: #확인 이벤트
             print("실행")
             qr_result.CreateWifiConfig(self, SSID, PWD) # wpa_supplicant.conf에 무선랜 정보 입력 > 재부팅 
             
        elif button==self.qr_btn_no: #취소 이벤트
            print('no버튼 클릭')
            print(widget.count())
            print(widget.currentIndex())
            widget.removeWidget(widget.widget(1)) # widget stack에 생성된 index 1 위젯 삭제 
            widget.setCurrentIndex(0) # 다시 mywindow로 전환 (QR다시 입력)
        
            
#재부팅되고 > 프로그램이 여기서 부터 실행. > 와이파이 연결(재부팅 결과)     
class nfc_window(nfc): # nfc통신 (그룹 코드 출력)
    def __init__(self):
        super(nfc_window, self).__init__()
        
        # 버튼 이벤트 연결
        self.power_btn.clicked.connect(self.power)
        self.reboot_btn.clicked.connect(self.reboot)
        
    def power(self):
        subprocess.call('sudo shutdown',shell=True)
    def reboot(self):
        subprocess.call('sudo reboot',shell=True)
                   
if __name__ == "__main__":
    
    # wifi연결이 안되어 있으면 widget에 mainwindow부터 시작  
    # 연결 되어 있으면 nfc_window부터 시작 
    
    app = QApplication(sys.argv)
    widget= QtWidgets.QStackedWidget()
    
    #와이파이 연결 여부 확인
    arg= ['iw','wlan0','link']
    fd_popen= subprocess.Popen(arg, stdout=subprocess.PIPE).stdout 
    data= fd_popen.read().strip()
    
    if (str(data).startswith("b'Connected")): # connected으로 시작 > 와이파이 연결됨 | 바로 nfc통신부터 시작 
        print('와이파이 연결 되었지롱')
        nfcwindow= nfc_window()
        widget.addWidget(nfcwindow) # 첫 화면 index 0번    
       
    elif (str(data).startswith("b'Not connected")): # Not connected으로 시작 > 와이파이 연결ㄴㄴ | 와이파이 설정하는 것부터 시작됨
        print('와이파이 연결 안됨')
        mainwindow = MyWindow()
        widget.addWidget(mainwindow) # 첫 화면 index 0번
    
    widget.setFixedHeight(480)  
    widget.setFixedWidth(800)  
    widget.showFullScreen()
    app.exec_()