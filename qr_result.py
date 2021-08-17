import sys
import os

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox

#qr정보 띄우는 함수
def result(wificode): # 매개변수 ssid, group_code
    print("qr_result에서 출력"+wificode)
    a = wificode.split(sep=';P:')
    
    _p_index = a[1]
    s_index = wificode[13:wificode.find(';P')]
    p_index = _p_index[:-4]

    print("SSID : "+s_index)
    print("PW : "+p_index)

    return s_index, p_index


# wpa_supplicant.conf파일에 무선랜 정보 입력함수
def CreateWifiConfig(self, SSID, password): 
    config_lines = [
        '\n',
        'network={',
        '\tssid="{}"'.format(SSID),
        '\tpsk="{}"'.format(password),
        '\tkey_mgmt=WPA-PSK',
        '}'
    ]
    config = '\n'.join(config_lines)
    print(config)

    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "a+") as wifi:
        wifi.write(config)

    print("Wifi config added")
    
    # 재부팅 알림창 띄우기
    reboot_msg= QMessageBox.information(self,'알림', 'Yes를 누르면 재부팅이 시작되어 와이파이에 연결됩니다.', QMessageBox.Yes)
    if (reboot_msg==QMessageBox.Yes):
        os.system("sudo reboot now") # 재부팅하는 코드
  

