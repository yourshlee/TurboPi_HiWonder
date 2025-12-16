import time
import HiwonderSDK.ros_robot_controller_sdk as rrc

board = rrc.Board()
board.enable_reception()  # 배터리 데이터 수신 활성화
time.sleep(0.5)  # 데이터 수신 대기

voltage = board.get_battery()  # 전압 값 반환 (단위: mV)
if voltage is not None:
    print(f"{voltage}mV = {voltage/1000.0:.2f}V")
else:
    print("None")
