import sys
import os
import subprocess #시스템 종료를 위한 'sh' 실행, 와이파이 연결 확인

import qrcode_wifi
import qr_result
from nfc import nfc

from ver_check import version

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
#리소스 파일 사용시 resource_path()사용해서 절대경로로 변경

set_class = uic.loadUiType('/home/pi/nfc_2021_kiosk/set.ui')[0]
Qrtest_class = uic.loadUiType("/home/pi/nfc_2021_kiosk/camtest.ui")[0]
#persom_img_class= uic.loadUiType("C:\\Users\\졸비쨔응\\Documents\\nfc_2021_kiosk\\nfc.ui")[0]

wificode ='' # qr 내용 저장할 변수
class MyWindow(QMainWindow, set_class): #set.ui *첫 화면     
    def __init__(self):
        
        super().__init__()
        self.setupUi(self) # 화면 나오게 함
        self.setWindowTitle("Hoseo Unviersity - IR LAB") # 제목 표시줄

        self.qrcode_btn.clicked.connect(self.btn_connect) # 이벤트 연결

        self.power_btn.clicked.connect(self.btn_power)
        self.reboot_btn.clicked.connect(self.btn_reboot)
    
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

    def btn_power(self):
        subprocess.call('sudo shutdown',shell=True)
    def btn_reboot(self):
        subprocess.call('sudo reboot',shell=True)
            
class Set_Window(QMainWindow, Qrtest_class):    # camtest.ui *qr내용 출력됨    
    def __init__(self):
        global wificode, SSID, PWD
        
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Hoseo Unviersity - IR LAB")
        SSID, PWD = qr_result.result(wificode)     
        self.qr_label.setText(str(SSID + PWD ))
        self.qr_btn_yes.clicked.connect(lambda state, button=self.qr_btn_yes: self.btn_connect(state, button))
        self.qr_btn_no.clicked.connect(lambda state, button=self.qr_btn_no: self.btn_connect(state, button))
    
    def btn_connect(self, state, button):
        if button==self.qr_btn_yes: #확인 이벤트
             print("실행")
             qr_result.CreateWifiConfig(SSID, PWD)
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
        version.ver.loading(self) #로딩중 * ota 완료하면 조건에 따라 다시 편집할 예정!
        #self.next_btn.clicked.connect(self.next_page) # *버전 업그레이드 완료 or 최신 버전인 경우 자동으로 다음 페이지로 전환  
        self.next_btn.clicked.connect(self.next_page)
          
    def next_page(self): #
        next= nfc_window()
        widget.addWidget(next)
        widget.setCurrentIndex(widget.currentIndex()+1) # 재부팅 / 초기 무선랜 이미 연결 > index 1번
                
class nfc_window(nfc): #nfc통신 하는 클래스 
    def __init__(self):
        super(nfc_window, self).__init__()
        self.group_serch() #그룹코드 검색
                   
if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    widget= QtWidgets.QStackedWidget()
    
    #wifi연결이 안되어 있으면  
    #widget에 mainwindow객체 추가
    #연결되어 있으면 verwindow객체 추가
    #재부팅 후 와이파이가 연결되어있으면 바로 버전검사 거쳐서 nfc통신 가능하도록!
    
    arg= ['iw','wlan0','link']
    fd_popen= subprocess.Popen(arg, stdout=subprocess.PIPE).stdout #와이파이 연결여부 확인
    data= fd_popen.read().strip()
    
    if (str(data).startswith("b'Connected")): # connected으로 시작 > 와이파이 연결됨 | 바로 버전검사로 넘어감   
        print('와이파이 연결 되었지롱')
        verwindow= ver_window()
        widget.addWidget(verwindow) # 첫 화면 index 0번    
       
    elif (str(data).startswith("b'Not connected")): # Not connected으로 시작 > 와이파이 연결ㄴㄴ | 와이파이 설정하는 것부터 시작됨
        print('와이파이 연결 안됨')
        mainwindow = MyWindow()
        widget.addWidget(mainwindow) # 첫 화면 index 0번
    
    widget.setFixedHeight(480)  
    widget.setFixedWidth(800)  
    widget.showFullScreen()
    app.exec_()
    