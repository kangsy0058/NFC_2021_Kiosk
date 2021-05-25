import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import *

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

wifi_class = uic.loadUiType(resource_path("wifi.ui"))[0]
wifi_list=["와이파이1","와이파이2","와이파이3"]

class mywifi(QMainWindow,wifi_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.wifi_Recall()
        self.wifi_tableWidget.cellClicked.connect(self.cellClicked_event)
        
        timer=QTimer(self)
        timer.start(10000) #10초에 한번씩 timeout이벤트 발생
        timer.timeout.connect(self.wifi_Recall)
        
        #wifi_list를 wifi_tableWidget으로 다시 전달하는 함수 
    def wifi_Recall(self):
            print("10초지남")
                       
            for i, list in enumerate(wifi_list):
                item = QTableWidgetItem(list)
                self.wifi_tableWidget.setItem(i, 0, item)
                
    def cellClicked_event(self):
             
        text, ok = QInputDialog.getText(self, '비밀번호 입력', 'PW:') 
        if ok:
            if(text=="1234"):
                print("암호일치")
                QMessageBox.about(self, "암호 일치", "연결되었습니다.")
                widget.setCurrentIndex(widget.currentIndex()+1)
            else: 
                QMessageBox.warning(self, "암호 오류", "암호가 일치하지 않습니다.")
        else:
            print("취소")
           
            
            
if __name__ == "__main__":
    app = QApplication(sys.argv) 
    w=mywifi()
    w.show()
    app.exec_()