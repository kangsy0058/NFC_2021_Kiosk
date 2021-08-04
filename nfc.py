#------버전 검사 및 업데이트하는 모듈------
import os
import sys
import requests,json #rest api통신하기 위한 파이썬 api모듈

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtGui

# QPixmap >> 레이블에 이미지를 나타내기 위한 함수!
# 1. QPixmap 객체 생성
# 2. 1번 객체에 이미지 불러옴
# 3. 레이블에 객체를 불러오기

persom_img_class= uic.loadUiType("C:\\Users\\졸비쨔응\\Documents\\nfc_2021_kiosk\\nfc.ui")[0] #라즈베리파이에 테스트 시 절대 경로로 변경하기!

class nfc(QMainWindow, persom_img_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        pixmap= QPixmap() # 1이미지를 가져오기 위한 객체 생성 
        pixmap.load('img\people.png')
        self.nfc_img_label.setPixmap(pixmap) # 3 레이블에 이미지 적용
        
    def group_serch(self): # 그룹코드를 검색하는 메소드 
        
        url= str("http://210.119.104.206:8080/v1/kiosk/sncheck/123456") # 
        response = requests.get(url)     
        '''
            rt: 200
            response: True, 그룹코드, 상세 위치, 건물명, 위도, 경도
            --미조회시--

            rt: 200
            response: False
        '''
        result= response.text
        result= result[result.find('N')+4:result.find(',')-1]
        self.info_label.setFont(QtGui.QFont("굴림",24)) 
        self.info_label.setText("NFC 전자 출입 시스템 그룹 코드-"+result)
       
       
        
       
    
    def ver_serch(self): # 버전 검사 메소드
        pass
    



  