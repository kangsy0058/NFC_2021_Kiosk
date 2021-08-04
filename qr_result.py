import sys
import os

#qr정보 띄우는 함수
def result(wificode): # 매개변수 ssid, group_code
    print("qr_result에서 출력"+wificode)
    print(type(wificode))
    a= wificode.split(sep=';')
    del a[2:]
    
    print(a)
    '''
    s_index= wificode.find('S')
    p_index= wificode.find('')

    print(s_index)
    print(p_index)
   
    r=wificode[s_index:p_index-1] 
    '''
    '''
    변수로 받을 경우
    qr_add="SSID:{0}\nGroup code:{1}.format(ssid, group_code)"
    return qr_add    
    '''
    
    
    return a
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

  
#테스트 파일 
def test():
    print('test 연결 완료 | 재부팅 테스트 시 main,  qr_result문서에서 주석 표시 지우기')
