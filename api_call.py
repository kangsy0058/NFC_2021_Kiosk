import os
import sys

import subprocess
import requests,json 

#kiosk S/N 출력 
def kiosk_sn():
    arg= ["cat", "/proc/cpuinfo"]
    result= subprocess.Popen(arg,stdout=subprocess.PIPE).stdout
    data= result.read().strip()
    end_index= str(data).find("Model")
    data=str(data)[end_index-18:end_index-2] # 시리얼 넘버 16자리 출력 > 성공
    print(data)
    return data
    
# 그룹코드 출력 : 시리얼넘버를 보내고 그룹코드를 받음
def group_code():
    #시리얼 넘버를 보낼 경우 wsn을 앞에 붙여서 보내야함
    sn= "wsn"+str(12345) # kiosk_sn() < 실제 시리얼넘버 값 보낼 경우 이걸로 값 변경하기
    print("http://210.119.104.206:8080/v1/kiosk/sncheck/"+sn)
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
    result= response.text
    print(result) # 결과값 {{"wearableSN": "123456", "isuser":false}} DB에 없으면 isuser false값 나옴
    result= result[result.find('N')+4:result.find(',')-1]
    return result
