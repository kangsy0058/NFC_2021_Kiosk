#------버전 검사 및 업데이트하는 모듈------
import os
import sys
import requests,json #rest api통신하기 위한 파이썬 api모듈

import api_call 

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5 import uic

persom_img_class= uic.loadUiType("/home/pi/nfc_2021_kiosk/nfc.ui") [0] 
class nfc(QMainWindow, persom_img_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # kiosk s/n 호출 
        kiosk= api_call.kiosk_sn() 
        
        #그룹코드 호출
        group= api_call.group_code() 
        self.info_label.setFont(QtGui.QFont("굴림",10)) 
        self.info_label.setText(group)
        
        # 동적 이미지 
        self.movie= QMovie('/home/pi/nfc_2021_kiosk/img/nfc-mood.gif',QByteArray(), self) #QMovie객체 생성
        # 1번째 인자 파일로 이미지 데이터를 읽음 , QByteArray 바이트 배열을 디코딩하는데 사용.
        self.movie.setCacheMode(QMovie.CacheAll) # 캐시 모드 지원
        self.nfc_img_label.setMovie(self.movie) # 레이블에 동적이미지 전달
        self.movie.start() # 이미지 실행
    
    
    def nfc_api(self): # api 통신
        pass
    