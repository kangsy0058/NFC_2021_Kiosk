import sys
import os
import wifi
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


main_class = uic.loadUiType(resource_path("main.ui"))[0]
screen2_class = uic.loadUiType(resource_path("test.ui"))[0]
wifi_class = uic.loadUiType(resource_path("wifi.ui"))[0]

wifi_list=["와이파이1","와이파이2","와이파이3"]

class MyWindow(QMainWindow, main_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Hoseo Unviersity - IR LAB")

        self.top_label.setText("체온측정 Kiosk")

        self.check_btn.clicked.connect(self.check_clicked_btn)

        self.num_btn_1.clicked.connect(lambda state, button=self.num_btn_1 : self.num_clicked_btn(state,button))
        self.num_btn_2.clicked.connect(lambda state, button=self.num_btn_2 : self.num_clicked_btn(state,button))
        self.num_btn_3.clicked.connect(lambda state, button=self.num_btn_3 : self.num_clicked_btn(state,button))
        self.num_btn_4.clicked.connect(lambda state, button=self.num_btn_4 : self.num_clicked_btn(state,button))
        self.num_btn_5.clicked.connect(lambda state, button=self.num_btn_5 : self.num_clicked_btn(state,button))
        self.num_btn_6.clicked.connect(lambda state, button=self.num_btn_6 : self.num_clicked_btn(state,button))
        self.num_btn_7.clicked.connect(lambda state, button=self.num_btn_7 : self.num_clicked_btn(state,button))
        self.num_btn_8.clicked.connect(lambda state, button=self.num_btn_8 : self.num_clicked_btn(state,button))
        self.num_btn_9.clicked.connect(lambda state, button=self.num_btn_9 : self.num_clicked_btn(state,button))
        self.num_btn_0.clicked.connect(lambda state, button=self.num_btn_0 : self.num_clicked_btn(state,button))

        self.del_btn.clicked.connect(self.del_clicked_btn)
        
    def num_clicked_btn(self, state, button):
        exist_line_text = self.code_Edit.text()
        now_num_text = button.text()
        self.code_Edit.setText(exist_line_text+now_num_text)
    
    def del_clicked_btn(self):
        exist_line_text = self.code_Edit.text()
        self.code_Edit.setText(exist_line_text[:-1])

    def check_clicked_btn(self):
        G_code = self.code_Edit.text()
        if G_code == "123123":
            widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            self.notice_label.setStyleSheet("Color : red")
            self.notice_label.setText("다시 입력하세요")
            
class Screen2(QMainWindow, screen2_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
class wifi(QMainWindow, wifi_class):
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
             
        text, ok = QInputDialog.getText(self, '네트워크 암호 입력', 'PW:') 
        if ok:
            if(text=="1234"):
                print("암호일치")
                QMessageBox.about(self, "암호 일치", "연결되었습니다.")
                widget.setCurrentIndex(widget.currentIndex()+1)
            else: 
                QMessageBox.warning(self, "암호 오류", "암호가 일치하지 않습니다.")
        else:
            print("취소")
            #취소를 눌러도 화면이 꺼지지 않도록
            


if __name__ == "__main__":
    app = QApplication(sys.argv) # 프로그램 실행
    widget= QtWidgets.QStackedWidget() # Qtwidgets모듈의 Qstackedwidget클래스 
    wifi=wifi()
    mainwindow = MyWindow()
    screen2 = Screen2()
    widget.addWidget(wifi)
    widget.addWidget(mainwindow) # 위젯 추가 > mainwindow창
    widget.addWidget(screen2) # 위젯 추가  > screen창
    widget.setFixedHeight(400) # 사이즈 조절
    widget.setFixedWidth(800)
    widget.show() #화면에 보여지도록

    app.exec_() #이벤트 루프
    