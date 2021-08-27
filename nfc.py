from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5 import uic

#nfc를 위한 모듈
import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.i2c import PN532_I2C


persom_img_class= uic.loadUiType("/home/pi/nfc_2021_kiosk/nfc.ui") [0] 

class nfc():
    
    def nfc_set(self):
        #i2c = busio.I2C(board.SCL, board.SDA)
        #reset_pin = DigitalInOut(board.D6)
        #req_pin = DigitalInOut(board.D12)
        
        pn532 = PN532_I2C(busio.I2C(board.SCL, board.SDA), debug=False, reset=DigitalInOut(board.D6), req=DigitalInOut(board.D12))
        pn532.SAM_configuration()
        print("세팅완료")
        return pn532