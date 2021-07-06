import pyzbar.pyzbar as pyzbar
import cv2
import matplotlib.pyplot as plt 
import sys
import os


def start():
    cap = cv2.VideoCapture(0)
    cap.set(3,320)
    cap.set(4,240)

    my_code = None

    while cap.isOpened():
        success, frame=cap.read()
            
        if success:
            for code in pyzbar.decode(frame):
                my_code =code.data.decode('utf-8') 
            cv2.imshow('Camera Window', frame)
                
            key=cv2.waitKey(1)&0xff
            if(key==27):
                break
            if my_code is not None:
                break
            
    cap.release()  
    cv2.destroyAllWindows()
    return my_code