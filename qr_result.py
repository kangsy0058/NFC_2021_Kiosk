import sys
import os

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox

#qr정보 띄우는 함수
def result(wificode): # 매개변수 ssid, group_code
    '''
    wificode 출력 유형    
        1. 비밀번호 없을 경우= "WIFI:T:nopass;S:PASCUCCI_5G;P:;H:;"
        2. 비밀번호가 있을 경우=  "WIFI:T:WPA;S:SSID;P:PWD;H:;"
    '''
    a = wificode.split(sep=';P:') 
    print("a출력 : "+str(a))
    
    
    _p_index = a[1]
    psd_index = wificode[7:wificode.find(';')]
    print("psd_index : " + psd_index)
    s_index = '초기값'
    p_index = '초기값'
    
    if psd_index == "nopass":
        s_index = wificode[16:wificode.find(';P:')]
        p_index = ''
    elif psd_index == "WPA":
        s_index = wificode[13:wificode.find(';P:')]
        p_index = _p_index[:-4]
    
    print("SSID : "+s_index)
    print("PW : "+p_index)
    
    return s_index, p_index


# wpa_supplicant.conf파일에 무선랜 정보 입력함수
def CreateWifiConfig(self, SSID, password): 
    if password is '':
        config_lines = [
            '\n',
            'network={',
            '\tssid="{}"'.format(SSID),
            '\tkey_mgmt=NONE',
            '}'
        ]
    else :
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
  

