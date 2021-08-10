import os
import sys
import subprocess

#kiosk S/N 출력 
def kiosk_sn():
    arg= ["cat", "/proc/cpuinfo"]
    result= subprocess.Popen(arg,stdout=subprocess.PIPE).stdout
    data= result.read().strip()
    end_index= str(data).find("Model")
    data=str(data)[end_index-18:end_index-2] # 시리얼 넘버 16자리 출력 > 성공
    print(data)
    return data
    
#그룹코드 출력
def group_code():
    url= str("http://210.119.104.206:8080/v1/kiosk/sncheck/123456") # 
    response = requests.get(url)     
    '''
            rt: 200
            response: True, 그룹코드, 상세 위치, 건물명, 위도, 경도
            --미조회시--

            rt: 200
            response: False
    '''
    result= response.text
    result= result[result.find('N')+4:result.find(',')-1]
    return result