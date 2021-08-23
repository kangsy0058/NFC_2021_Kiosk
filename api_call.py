import os
import sys
import ast
from ast import literal_eval
 
from PyQt5.QtWidgets import QMessageBox

import subprocess
import requests,json 

#kiosk S/N 출력 
def kiosk_sn():
    arg= ["cat", "/proc/cpuinfo"]
    result= subprocess.Popen(arg,stdout=subprocess.PIPE).stdout
    data= result.read().strip()
    end_index= str(data).find("Model")
    data=str(data)[end_index-18:end_index-2] # 시리얼 넘버 16자리 출력 > 성공
    print("api_call.py의 kiosk_sn()")
    print(data)
    return data
    
# 그룹코드 출력 : 시리얼넘버를 보내고 그룹코드를 받음
def group_code(self):
    #시리얼 넘버를 보낼 경우 wsn을 앞에 붙여서 보내야함
    sn= "wsn"+str(111123) # kiosk_sn() < 실제 시리얼넘버 값 보낼 경우 이걸로 값 변경하기
    #print("http://210.119.104.206:8080/v1/kiosk/sncheck/"+sn)
    url= str("http://210.119.104.206:8080/v1/kiosk/sncheck/"+sn) 
    response = requests.get(url)     
    '''
            시리얼 넘버 보내면 그룹 코드 받음
            rt: 200
            response: True, 그룹코드, 상세 위치, 건물명, 위도, 경도
            --미조회시--

            rt: 200
            response: False
    '''
    result= response.text # 리턴값 = {"res":{"wearableSN": "123456", "isuser":false/true}}
    f= 'false'
    
    if f in result:
        #result= result.replace('false','False') #json은 boolean= false, true 파이썬 문법과 일치시키기 위해 False, True로 변경 
        print('False가 포함되어 있음') # DB에 일치하는 그룹코드가 없다! 
        res= json.loads(result) 
        print(res)
        return res   
    
    else:
        print('true가 있습니다~')
        res= json.loads(result) # true > True 변경 후 이 명령어를 사용하면 json형식이 아니라서 json객체가 없다고 나옴
        print(res) #{u'res': {u'wearableSN': u'123456', u'isuser': True}}
        return res