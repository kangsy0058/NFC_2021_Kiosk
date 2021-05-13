import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtWidgets

main_class = uic.loadUiType("main.ui")[0]
screen2_class = uic.loadUiType("test.ui")[0]


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



if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget= QtWidgets.QStackedWidget()
    mainwindow = MyWindow()
    screen2 = Screen2()
    widget.addWidget(mainwindow)
    widget.addWidget(screen2)
    widget.setFixedHeight(400)
    widget.setFixedWidth(800)
    widget.show()

    app.exec_()
    