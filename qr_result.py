import sys
import os

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


#***리눅스에서 돌리면 주석 제거하기***
# wpa_supplicant.conf파일 수정하는 함수
def CreateWifiConfig(SSID, password):
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
    os.system("sudo reboot now") # 재부팅하는 코드
 
#CreateWifiConfig("Ubiquitous_420", "1234567890") #테스트 코드

'''   
#테스트 파일 
def test():
    print('test 연결 완료')
'''
