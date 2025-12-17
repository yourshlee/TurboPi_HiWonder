#!/usr/bin/python3
# coding=utf8
"""
배터리 전압 확인 프로그램
"""
import sys
sys.path.append('/home/yourshlee/TurboPi/')
import time
import HiwonderSDK.ros_robot_controller_sdk as rrc

print('배터리 전압 측정 중...')
board = rrc.Board()
board.enable_reception()  # 배터리 데이터 수신 활성화
time.sleep(0.5)  # 데이터 수신 대기

voltage = board.get_battery()  # 전압 값 반환 (단위: mV)
if voltage is not None:
    volt_v = voltage / 1000.0
    print(f'\n현재 배터리 전압: {voltage}mV = {volt_v:.2f}V')

    # 배터리 상태 표시
    if volt_v >= 7.4:
        print('배터리 상태: 🔋 만충 (100%)')
    elif volt_v >= 7.2:
        print('배터리 상태: 🔋 양호 (90%+)')
    elif volt_v >= 7.0:
        print('배터리 상태: ⚠️  보통 (80%+)')
    elif volt_v >= 6.8:
        print('배터리 상태: ⚠️  낮음 (70%+)')
    elif volt_v >= 6.4:
        print('배터리 상태: 🔴 매우 낮음 (60%+) - 충전 권장')
    else:
        print('배터리 상태: 🔴 위험 (60% 미만) - 즉시 충전 필요')
else:
    print('\n전압 측정 실패 (배터리 연결 확인 필요)')
