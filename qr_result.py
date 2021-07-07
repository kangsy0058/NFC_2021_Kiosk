import sys
import os

def result(wificode): # 매개변수 ssid, group_code
    print("qr_result에서 출력"+wificode)
    print(type(wificode))
    
    s_index= wificode.find('"SSID')
    p_index= wificode.find('"PW')

    print(s_index)
    print(p_index)
   
    r=wificode[s_index:p_index-1] 
    '''
    변수로 받을 경우
    qr_add="SSID:{0}\nGroup code:{1}.format(ssid, group_code)"
    return qr_add    
    '''
    print(r)
    
    return r

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
    os.system("sudo reboot now")
 #테스트 코드
CreateWifiConfig("Ubiquitous_420", "1234567890")

'''    
def test():
    print('test 연결 완료')
'''