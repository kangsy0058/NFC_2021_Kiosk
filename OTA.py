'''
********** OTA등록 스크립트 ************** 
필수 기능
1. OTA 기기등록
    * 오류 (이미 등록된 기기가 있음/ 등록 오류 등 ) 대안
    * 등록되는 이름은 어떻게 할 건지 > 시리얼 넘버 
    OTA등록까지 완료된 상태에서 배포됨 
    
2. 기기 삭제 

'''
import os
import sys
import subprocess

#시리얼 넘버 출력
arg= ["cat", "/proc/cpuinfo"]
result= subprocess.Popen(arg,stdout=subprocess.PIPE).stdout
data= result.read().strip()
end_index= str(data).find("Model")
data=str(data)[end_index-18:end_index-2] 
print(data)
group="test"
print(group)

#기기 등록                                                                저장되는 이름은 시리얼 넘버, 그룹은 일단 test
re_device='sudo wget -O - "https://dashboard.upswift.io/install_upswift" | sudo sh -s TyVZiyMwitDVvmXt4sSMyQtxktZdpKezYg NFC -n={0} -g={1}'.format(data, group)
arg= re_device.split()

result= subprocess.call(re_device, shell=True)


# 일반 사용자
#sudo wget -O - "https://dashboard.upswift.io/install_upswift" | sudo sh -s TyVZiyMwitDVvmXt4sSMyQtxktZdpKezYg NFC

#루트 사용자
# su -c 'wget -O - "https://dashboard.upswift.io/install_upswift" | sh -s TyVZiyMwitDVvmXt4sSMyQtxktZdpKezYg NFC'
# su -c 'wget -O - "http://dashboard.upswift.io/install_upswift" | sh -s TyVZiyMwitDVvmXt4sSMyQtxktZdpKezYg NFC'
#sudo wget -O - "https://dashboard.upswift.io/install_upswift" | sudo sh -s TyVZiyMwitDVvmXt4sSMyQtxktZdpKezYg NFC -n=hoseo -g=testsudo wget -O - "https://dashboard.upswift.io/install_upswift" | sudo sh -s TyVZiyMwitDVvmXt4sSMyQtxktZdpKezYg NFC -n=hoseo -g=test
