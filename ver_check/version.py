import os
import sys

import api_call

from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

version_class = uic.loadUiType("/home/pi/nfc_2021_kiosk/ver_check/Ver_check.ui")[0] # 라즈베리파이에 테스트 시 절대경로로 변경!!
class ver(QMainWindow, version_class):
    def __init__(self): #ui구현 
        super().__init__()
        self.setupUi(self) #여기서 self=>main.py에서 만든 객체? 
        
        kiosk= api_call.kiosk_sn() # kiosk s/n 출력 
        self.info_label2.setText("KIOSK S/N: "+kiosk)
        self.info_label2.setFont(QtGui.QFont("굴림", 10, QtGui.QFont.Black))
         
    def loading(self): #로딩 ui 구현 함수
        #self.center() #위치 설정      
        self.movie= QMovie('ver_check/loading.gif',QByteArray(), self) #QMovie객체 생성
        #1번째 인자 파일로 이미지 데이터를 읽음 , QByteArray 바이트 배열을 디코딩하는데 사용.
        self.movie.setCacheMode(QMovie.CacheAll) #캐시 모드 지원
        self.loading_img.setMovie(self.movie) #레이블에 동적이미지 전달
        self.movie.start() # 이미지 실행
               
    def center(self): # 동적 이미지 위치 설정 함수
        size=self.size() #동적 이미지의 크기를 초기화
        self.move()
    
    