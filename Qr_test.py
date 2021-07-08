import pyzbar.pyzbar as pyzbar
import cv2
import matplotlib.pyplot as plt 
import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)   

Qrtest_class = uic.loadUiType(resource_path("camtest.ui"))[0]

cap = cv2.VideoCapture(0)
cap.set(3,320)
cap.set(4,240)
class Ex(QMainWindow,Qrtest_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        my_code = None

        while cap.isOpened():
            success, frame=cap.read()
            
            if success:
                for code in pyzbar.decode(frame):
                    my_code =code.data.decode('utf-8')
                    print(my_code)
                    self.label_2.setText(my_code)                 
                cv2.imshow('Camera Window', frame)
                
                key=cv2.waitKey(1)&0xff
                if(key==27):
                    break
                if my_code is not None:
                    break
            
        cap.release()  
        cv2.destroyAllWindows()
        
window= QApplication(sys.argv) 
w=Ex()
w.show()
window.exec_()