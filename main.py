import sys
import os
import subprocess #시스템 종료를 위한 'sh' 실행, 와이파이 연결 확인

import qrcode_wifi
import qr_result
from nfc import nfc

import api_call
from api_call import *

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui
from PyQt5.QtCore import *

#리소스 파일 사용시 resource_path()사용해서 절대경로로 변경

set_class = uic.loadUiType('/home/pi/nfc_2021_kiosk/set.ui')[0]
Qrtest_class = uic.loadUiType("/home/pi/nfc_2021_kiosk/camtest.ui")[0]
sn_class = uic.loadUiType('/home/pi/nfc_2021_kiosk/SN.ui')[0]
nfc_class = uic.loadUiType('/home/pi/nfc_2021_kiosk/nfc.ui')[0]

wificode ='' # qr 내용 저장할 변수
pn532 =''
#시리얼 넘버 출력 클래스
class sn_window(QMainWindow, sn_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
                
        #와이파이 연결 확인
        arg= ['iw','wlan0','link']
        fd_popen= subprocess.Popen(arg, stdout=subprocess.PIPE).stdout 
        data= fd_popen.read().strip()
        wifi = False 
        
        if (str(data).startswith("b'Connected")): # connected으로 시작 > 와이파이 연결됨 | 바로 nfc통신부터 시작 
            print('와이파이 연결')
            wifi = True
            api_result_dic= api_call.group_code(self) # 등록된 사용자인지 그룹코드 검색. 리턴값: 딕셔너리 형태
            
            if api_result_dic['res']['isuser']:  # 등록된 사용자              
                #시리얼 넘버 및 상세 정보 출력
                self.sn_label.setText('KIOSK S/N:'+ str(api_result_dic['res']['wearableSN'])) 
                 
                self.isuser_label.setText('사용자 등록: '+str(api_result_dic['res']['isuser']))
                
                
            else: # 등록되지 않은 사용자
                # 시리얼 넘버와 안내문구 출력
                self.sn_label.setText('KIOSK S/N:'+ str(api_result_dic['res']['wearableSN']))
                #self.sn_label.setText('KIOSK S/N:'+ api_call.kiosk_sn())
                self.isuser_label.setText('**등록된 사용자가 아닙니다. 웹에서 등록해주세요! **')
                self.pushButton.setEnabled(False) #다음 버튼 비활성화
                
            
        elif (str(data).startswith("b'Not connected")): # Not connected으로 시작 > 와이파이 연결ㄴㄴ | 와이파이 설정하는 것부터 시작됨
            print('와이파이 연결 안됨')
            self.sn_label.setText( 'KIOSK S/N: '+  api_call.kiosk_sn() )
            self.isuser_label.setText('와이파이를 연결하세요')
            self.research.setEnabled(False) # 다시 검색 버튼 비활성화
            
        
        # 버튼 이벤트 연결 (기능: 화면 전환)
        self.pushButton.clicked.connect(lambda state, button= wifi: self.btn_connect(state, button))       
            # 종료, 재부팅
        self.research.clicked.connect(self.research_btn)
        self.reboot_2.clicked.connect(self.rebootbtn)
    
    # 버튼 이벤트 1    
    def btn_connect(self, state, button): # 화면 전환 메소드   
         
        #와이파이 연결O > nfc통신 페이지  
        if button== True: 
              
            nfcwindow= nfc_window()
            widget.addWidget(nfcwindow) # 첫 화면 index 1번  
            widget.setCurrentIndex(1)  
            
        #와이파이 연결X > MyWindow 연결 페이지      
        else:
            mainwindow = MyWindow()
            widget.addWidget(mainwindow) # 첫 화면 index 1번
            widget.setCurrentIndex(1)  
            
    # 버튼 이벤트 2     
    def research_btn(self): # 그룹 코드 다시 검색 메소드   
        print('다시 검색')    
        api_result_dic= api_call.group_code(self)
        if (api_result_dic['res']['isuser'] ): # 등록된 사용자
            self.sn_label.setText('KIOSK S/N:'+ str(api_result_dic['res']['wearableSN'])) 
            self.isuser_label.setText('사용자 등록: '+str(api_result_dic['res']['isuser']))
        else: # 등록되지 않은 사용자 
            self.sn_label.setText('KIOSK S/N:'+ str(api_result_dic['res']['wearableSN']))
            self.isuser_label.setText('** 등록된 사용자가 아닙니다. 웹에서 등록해주세요! **')
            
    # 버튼 이벤트 3       
    def rebootbtn(self):  # 재시작 버튼 메소드   
        subprocess.call('sudo reboot now',shell=True)
            
#와이파이 QR 입력 클래스 
class MyWindow(QMainWindow, set_class): #set.ui 
    def __init__(self):
        
        super().__init__()
        #화면 세팅
        self.setupUi(self) 
        
        
        #이벤트 연결
        self.qrcode_btn.clicked.connect(self.btn_connect) # QR시작 버튼 이벤트
        
        self.power_btn.clicked.connect(self.btn_power)  # shutdown 클릭 이벤트
        self.reboot_btn.clicked.connect(self.btn_reboot)# reboot 클릭 이벤트
    
    def btn_connect(self):
        global wificode #와이파이QR 정보 저장
        
        wificode = qrcode_wifi.start()  # 리턴값: QR 해석
        print(wificode) 
        
        if wificode is not None: # 유효한 값이 들어오면 다음 화면으로 변경 
            setwindow = Set_Window() 
            a=widget.addWidget(setwindow) #index 2번
            print('setwindow 인덱스', a) 
            widget.setCurrentIndex(widget.currentIndex()+1) # setwindow으로 화면 전환

    def btn_power(self):
        subprocess.call('sudo shutdown now',shell=True)
    def btn_reboot(self):
        subprocess.call('sudo reboot now',shell=True)
        
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
        self.qr_label.setText(str(SSID))
        self.qr_label_2.setText(str(PWD))
        
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
            widget.removeWidget(widget.widget(2)) # widget stack에 생성된 index2 위젯 삭제 
            widget.setCurrentIndex(1) # 다시 mywindow로 전환 (QR다시 입력)

# 웨어러블 태그 클래스        
class Thread(QThread):
    def __init__(self, parent):
        global pn532
        super().__init__(parent)
        self.parent=parent
         
    def run(self):
        print("웨어러블 기기를 태그해주세요")
        while True:
        # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=1)
            print(".", end="")
                
            # Try again if no card is available.
            if uid is None:
                continue
            else: 
                print("Found card with UID:", [hex(i) for i in uid])
                subprocess.call('aplay /home/pi/nfc_2021_kiosk/mp3/ok2.wav',shell=True)
                break
            
                    
#재부팅되고 > 프로그램이 여기서 부터 실행. > 와이파이 연결(재부팅 결과)     
class nfc_window(QMainWindow, nfc_class): # nfc통신 (그룹 코드 출력)
    def __init__(self):
        global pn532
        super().__init__()
        self.setupUi(self)
        
        # 버튼 이벤트 연결
        self.power_btn.clicked.connect(self.power)
        self.reboot_btn.clicked.connect(self.reboot)
            
        #그룹코드 호출
        api_result_dic= api_call.group_code(self) 
        self.info_label.setFont(QtGui.QFont("굴림",10)) 
        self.info_label.setText(api_result_dic['res']['wearableSN'])
        
        # 동적 이미지 
        self.movie= QMovie('/home/pi/nfc_2021_kiosk/img/nfc-mood.gif',QByteArray(), self) # QMovie객체 생성
                                                                                          # 1번째 인자 파일로 이미지 데이터를 읽음 , QByteArray 바이트 배열을 디코딩하는데 사용.
        self.movie.setCacheMode(QMovie.CacheAll) # 캐시 모드 지원   
        self.nfc_img_label.setMovie(self.movie) # 레이블에 동적이미지 전달
        self.movie.start() # 이미지 실행
        
        #nfc 세팅
        pn532= nfc.nfc_set(self)
        
        # 태그 스레드 실행
        t=Thread(self)
        t.start()
                
    def power(self):
        subprocess.call('sudo shutdown now',shell=True)
    def reboot(self):
        subprocess.call('sudo reboot now',shell=True)
 
                        
if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    widget= QtWidgets.QStackedWidget()
    
    snwindow=sn_window()
    widget.addWidget(snwindow) #첫 화면 index 0번 
    
    widget.setFixedHeight(480)  
    widget.setFixedWidth(800)  
    widget.showFullScreen()
    app.exec_()
    
    # https://ybworld.tistory.com/39?category=929856