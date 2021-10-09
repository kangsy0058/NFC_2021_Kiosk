import sys
import os
import subprocess #시스템 종료를 위한 'sh' 실행, 와이파이 연결 확인
import time



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
from PyQt5 import QtCore
from PyQt5.QtCore import *

from gpiozero import LED

led_G = LED(23)
led_R = LED(24)
led_Y = LED(17)
#리소스 파일 사용시 resource_path()사용해서 절대경로로 변경


set_class = uic.loadUiType('/home/pi/nfc_2021_kiosk/set.ui')[0]
Qrtest_class = uic.loadUiType("/home/pi/nfc_2021_kiosk/camtest.ui")[0]
sn_class = uic.loadUiType('/home/pi/nfc_2021_kiosk/SN.ui')[0]
nfc_class = uic.loadUiType('/home/pi/nfc_2021_kiosk/nfc.ui')[0]

wificode ='' # qr 내용 저장할 변수
pn532 =''
group='' # 그룹 코드 저장

class sn_window_thread(QThread): 
    def __init__(self, parent):
        super().__init__(parent)
        self.parent= parent
        self.timer= QTimer(self)
        
    def run(self):
        global group     
        
        #와이파이 연결 확인
        arg= ['iw','wlan0','link']
        fd_popen= subprocess.Popen(arg, stdout=subprocess.PIPE).stdout 
        data= fd_popen.read().strip() 
        
        if (str(data).startswith("b'Connected")): # connected으로 시작 > 와이파이 연결됨 | 바로 nfc통신부터 시작 
            print('와이파이 연결')
            self.parent.wifi = True
            print("wifi에 True대입", self.parent.wifi)
            
            #self.timer.singleShot(2000, self.loading_sg.emit(True))
            #self.loading_sg.emit(True)
            api_result_dic= api_call.group_code(self) # 그룹 등록 여부, 그룹코드 검색. 리턴값: 딕셔너리 형태 (원래 그룹코드, 상세 위치, 건물명, 위도, 경도, 그룹 등록 여부) 
            print("딜레이 완료")
            #호출 완료된 시점에서 로딩이미지 종료되도록 false값을 방출
            #self.loading_sg.emit(False)
            
            if api_result_dic['res']['isuser']:  # 등록된 사용자
                              
                # kiosk s/n, 그룹 코드 UI출력 
                group= str(api_result_dic['res']['wearableSN'])
                self.parent.sn_label.setText('KIOSK S/N:'+ api_call.kiosk_sn()+"\nGROUP CODE:"+group) 
                self.parent.isuser_label.setText('사용자 등록: '+str(api_result_dic['res']['isuser']))
                
                
            else: # 등록되지 않은 사용자
              
                # kiosk s/n, 그룹 코드 UI와 안내문구 출력 
                self.parent.movie.stop()
                self.parent.sn_label.setText('KIOSK S/N:'+ api_call.kiosk_sn())  
                self.parent.isuser_label.setText('**등록된 사용자가 아닙니다. 웹에서 등록해주세요! **')
                
                self.parent.pushButton.setEnabled(False) #다음 버튼 비활성화
                
            
        elif (str(data).startswith("b'Not connected")): # Not connected으로 시작 > 와이파이 연결ㄴㄴ | 와이파이 설정하는 것부터 시작됨
            print('와이파이 연결 안됨')
            self.parent.wifi= False
            
            self.parent.sn_label.setText( 'KIOSK S/N: '+  api_call.kiosk_sn() )
            self.parent.isuser_label.setText('와이파이를 연결하세요')
            self.parent.research.setEnabled(False) # 다시 검색 버튼 비활성화
            
        print("스레드 종료")
        
        
        
#시리얼 넘버 출력 클래스
class sn_window(QMainWindow, sn_class):
    def __init__(self):
        global group
        super().__init__()
        self.setupUi(self)
        
        self.wifi=False
        
        # 버튼 이벤트 연결 
        self.pushButton.clicked.connect(self.btn_connect) # 다음버튼 (NFC통신 화면 전환)
        self.research.clicked.connect(self.research_btn) # 다시 검색
        self.reboot_2.clicked.connect(self.rebootbtn) # 재부팅

        # api 스레드  
        self.t1=sn_window_thread(self)
        self.t1.start()
        
        
        # 로딩이미지 구현 
        self.loading()
        
        
    def loading(self):
        self.movie= QMovie('/home/pi/nfc_2021_kiosk/img/loading.gif',QByteArray(), self) # QMovie객체 생성
                                                                                            # 1번째 인자 파일로 이미지 데이터를 읽음 , QByteArray 바이트 배열을 디코딩하는데 사용.
        self.movie.setCacheMode(QMovie.CacheAll) # 캐시 모드 지원   
        self.sn_label.setMovie(self.movie) # 레이블에 동적이미지 전달
        self.movie.start() # 이미지 실행
        self.isuser_label.setText('')
            
        
    # 버튼 이벤트: 다음버튼    btn_connect(self, state, button)
    def btn_connect(self): # 화면 전환 메소드   
        print()
        #와이파이 연결O > nfc통신 페이지  
        if self.wifi== True: 
            nfcwindow= nfc_window()
            widget.addWidget(nfcwindow) # 첫 화면 index 1번  
            widget.setCurrentIndex(1)  
            
        #와이파이 연결X > MyWindow 연결 페이지      
        else:
            mainwindow = MyWindow()
            widget.addWidget(mainwindow) # 첫 화면 index 1번
            widget.setCurrentIndex(1)  
            
            
    # 버튼 이벤트: 다시 검색     
    def research_btn(self): # 그룹 코드 다시 검색 메소드   
        print('다시 검색 버튼 클릭')  
          
        self.sn_label.setText('')
        self.isuser_label.setText('')
        
        self.sn_label.setMovie(self.movie) # 레이블에 동적이미지 전달
        self.movie.start() # 이미지 실행
        
        self.t1.start()
    
    # 버튼 이벤트: 재부팅       
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

# 웨어러블 태그        
class Thread(QThread):
    
    state_sg= pyqtSignal(int) # 신호 방출> 0==대기 1==pass 2==warning
    
    def __init__(self, parent): #여기서 self는 Thread, parent에는 nfc의 객체가 들어가
        global pn532
        super().__init__(parent)
        self.parent=parent
        
    
        
    def run(self):
    
        while True:
            uid = pn532.read_passive_target(timeout=2)
            print(".", end="")
            
            
            
            self.state_sg.emit(0) # 대기 (0)
            self.parent.user_info_label.setText("") 
            self.parent.state_label.setText("인식 대기중...")
            self.parent.state_label.setFont(QtGui.QFont("굴림", 34, QtGui.QFont.Black))
            

            if uid is None:
                continue
            else: 
                # 값을 검색할 경우 넘길 값 그냥 UID만 넘기면 됨.
                 
                key=[hex(i) for i in uid]
                i= self.search(key)
                if i==-1:
                    #신호 방출> 0==대기 1==pass 2==warning
                    self.state_sg.emit(1)
                    
                    print("Found card with UID:", [hex(i) for i in uid])
                    self.parent.state_label.setText("태그되었습니다.\n"+"".join(key))#"".join(key)
                    self.parent.state_label.setFont(QtGui.QFont("굴림", 20, QtGui.QFont.Black))
                    
                  

                    #체온, 배터리 용량

                    battery= 80
                    
                    f_data= pn532.ntag2xx_read_block(6)
                    f_data2= pn532.ntag2xx_read_block(7)
                    print(f_data + f_data2)
                    f_data= float(f_data.decode('ASCII').replace('n',''))
                    
                    #f_data= 37.8 동영상 촬영용
                    

                    self.parent.user_info_label.setText("체온: "+str(f_data)+"℃\n배터리 용량: "+str(battery)+"%")
                    self.parent.user_info_label.setFont(QtGui.QFont("굴림", 13, QtGui.QFont.Black))

                    if f_data >= 37.5:
                        led_R.on()
                        subprocess.call('aplay /home/pi/nfc_2021_kiosk/mp3/warning.wav',shell=True) 
                    elif f_data < 37.5:
                        print("여기")
                        led_G.on()            
                        subprocess.call('aplay /home/pi/nfc_2021_kiosk/mp3/ok2.wav',shell=True) # 사운드 변경해
                    time.sleep(1)

                    if f_data >= 37.5: 
                        
                        led_R.off()

                    elif f_data <37.5:
                        led_G.off()

                    continue
                    
                
                elif(i>=0): 
                    self.state_sg.emit(2)
                    
                    print("이미 태그하셨습니다.")
                    self.parent.state_label.setText("이미 태그하셨습니다.\n"+"".join(key))
                    self.parent.state_label.setFont(QtGui.QFont("굴림", 20, QtGui.QFont.Black))
                    
                    
                    #체온, 배터리 용량
                    battery= 80
                    f_data= pn532.ntag2xx_read_block(6)
                    f_data2= pn532.ntag2xx_read_block(7)
                    print(f_data + f_data2)
                    f_data= float(f_data.decode('ASCII').replace('n',''))


                    self.parent.user_info_label.setText("체온: "+str(f_data)+"\n배터리 용량: "+str(battery)+"%")
                    self.parent.user_info_label.setFont(QtGui.QFont("굴림", 13, QtGui.QFont.Black))

                    if f_data >= 37.5:
                        led_R.on()
                        self.parant.state_label.setText("체온이 "+str(f_data)+"입니다. 출입을 금지합니다.")
            
                    elif f_data < 37.5:
                        led_Y.on() 
                        
                        subprocess.call('aplay /home/pi/nfc_2021_kiosk/mp3/already.wav',shell=True)                         
                    time.sleep(1)

                    if f_data >= 37.5:
                        led_R.off()
                    else:
                        led_Y.off()
                    continue
                   
                    
            
    def search(self, key):
        i=0;
        # visitor배열 중복 제거해야함 수정해야함 코드 이상해
        self.parent.visitor.append(key)
        
        while(True):
            if(self.parent.visitor[i]==key):
                break
            i+=1
        
        if (i==(len(self.parent.visitor)-1))or(len(self.parent.visitor)==1 and i==0): # 처음 태그하는 경우
            i=-1
            return i 
        else : # 전에 태그 전적이 있는 경우
            return i
        
#재부팅되고 > 프로그램이 여기서 부터 실행. > 와이파이 연결(재부팅 결과)     
class nfc_window(QMainWindow, nfc_class): # nfc통신 (그룹 코드 출력)
    def __init__(self):
        global pn532, group
        super().__init__()
        self.setupUi(self)
        
        # 버튼 이벤트 연결
        self.power_btn.clicked.connect(self.power)
        self.reboot_btn.clicked.connect(self.reboot)
        

        #그룹코드 호출
        #api_result_dic= api_call.group_code(self) 
        self.info_label.setFont(QtGui.QFont("굴림",10)) 
        self.info_label.setText(group)
        
        #동적 이미지 객체 
        self.movie= QMovie('/home/pi/nfc_2021_kiosk/img/nfc-mood.gif',QByteArray(), self) # QMovie객체 생성
                                                                                          # 1번째 인자 파일로 이미지 데이터를 읽음 , QByteArray 바이트 배열을 디코딩하는데 사용.
        self.movie.setCacheMode(QMovie.CacheAll) # 캐시 모드 지원   
        self.nfc_img_label.setMovie(self.movie) # 레이블에 동적이미지 전달
        self.movie.start() # 이미지 실행
       
        #태그 상태 이미지 객체  
        self.pass_img = QPixmap('/home/pi/nfc_2021_kiosk/img/pass.png') 
        self.warning_img = QPixmap('/home/pi/nfc_2021_kiosk/img/warning.png')
        
        # nfc 세팅
        pn532= nfc.nfc_set(self)
        self.visitor= list() # 웨어러블 s/n 저장할 변수
        
        # 태그 스레드 실행 
        t=Thread(self)
        t.state_sg.connect(self.img_load)
        t.start()
        
        
    def img_load(self,state):
        if state==0:
           
            self.nfc_img_label.setMovie(self.movie) # 레이블에 동적이미지 전달
            self.movie.start() # 이미지 실행
            
        elif state==1:
            self.movie.stop()
            
            self.nfc_img_label.setPixmap(self.pass_img)
            
        elif state==2:
            self.movie.stop()
            
            self.nfc_img_label.setPixmap(self.warning_img)
                
    def power(self):
        subprocess.call('sudo shutdown now',shell=True)
        
    def reboot(self):
        subprocess.call('sudo reboot now',shell=True)
 #스레드 한 이유 : 태그 대기상태를 반복문으로 구현하는데 도중에 버튼 클릭 이벤트 같은 gui기능도 같이 작동해야해서
                        
if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    widget= QtWidgets.QStackedWidget()
    
    snwindow=sn_window()
    widget.addWidget(snwindow) #첫 화면 index 0번 
    
    widget.setFixedHeight(480)  
    widget.setFixedWidth(800)  
    widget.showFullScreen()
    app.exec_()
    
    # https://ybworld.tistory.com/39?category=9298563