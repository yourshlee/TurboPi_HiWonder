#!/usr/bin/python3
# coding=utf8
"""
TurboPi 하드웨어 단위 테스트 메뉴 프로그램

모든 하드웨어 컴포넌트를 개별적으로 테스트할 수 있는 메뉴 시스템
"""

import sys
sys.path.append('/home/yourshlee/TurboPi/')
import time
import os
import subprocess
import HiwonderSDK.ros_robot_controller_sdk as rrc
import HiwonderSDK.mecanum as mecanum
import HiwonderSDK.Sonar as Sonar

# 전역 객체
board = None
car = None
sonar = None

def clear_screen():
    """화면 지우기"""
    os.system('clear')

def print_header():
    """헤더 출력"""
    print("=" * 70)
    print(" " * 20 + "TurboPi 단위 테스트 메뉴")
    print("=" * 70)

def print_status():
    """기기 현재 상태 출력"""
    global board

    print("\n" + "=" * 70)
    print("기기 상태")
    print("=" * 70)

    # 배터리 전압
    try:
        if board is None:
            board = rrc.Board()
            board.enable_reception()
            time.sleep(0.5)

        voltage = board.get_battery()
        if voltage is not None:
            volt_v = voltage / 1000.0
            print(f"배터리 전압: {voltage}mV = {volt_v:.2f}V", end="")

            if volt_v >= 7.4:
                print(" [🔋 만충 100%]")
            elif volt_v >= 7.2:
                print(" [🔋 양호 90%+]")
            elif volt_v >= 7.0:
                print(" [⚠️  보통 80%+]")
            elif volt_v >= 6.8:
                print(" [⚠️  낮음 70%+]")
            elif volt_v >= 6.4:
                print(" [🔴 매우낮음 60%+]")
            else:
                print(" [🔴 위험 60%미만]")
        else:
            print("배터리 전압: 측정 실패")
    except Exception as e:
        print(f"배터리 전압: 오류 ({e})")

    # TurboPi 서버 상태
    try:
        result = subprocess.run(['pgrep', '-f', 'TurboPi.py'],
                              capture_output=True, text=True)
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            print(f"TurboPi 서버: 실행 중 (PID: {', '.join(pids)})")
        else:
            print("TurboPi 서버: 중지됨")
    except:
        print("TurboPi 서버: 상태 확인 실패")

    # 영상 스트리밍 포트
    try:
        result = subprocess.run(['sudo', 'ss', '-tlnp'],
                              capture_output=True, text=True)
        if ':8080' in result.stdout:
            print("영상 스트리밍: http://192.168.0.11:8080/")
        else:
            print("영상 스트리밍: 비활성화")

        if ':9030' in result.stdout:
            print("RPC API 서버: http://192.168.0.11:9030/")
        else:
            print("RPC API 서버: 비활성화")
    except:
        print("포트 상태: 확인 실패")

    # 카메라 장치
    try:
        result = subprocess.run(['v4l2-ctl', '--list-devices'],
                              capture_output=True, text=True)
        if 'icspring' in result.stdout:
            print("카메라: 연결됨 (/dev/video0)")
        else:
            print("카메라: 연결 안됨")
    except:
        print("카메라: 상태 확인 실패")

    print("=" * 70)

def test_servo():
    """서보 모터 테스트"""
    global board

    clear_screen()
    print_header()
    print("\n서보 모터 테스트")
    print("-" * 70)

    if board is None:
        board = rrc.Board()

    while True:
        print("\n1. 서보1 (팬, 좌우) - 왼쪽")
        print("2. 서보1 (팬, 좌우) - 중앙")
        print("3. 서보1 (팬, 좌우) - 오른쪽")
        print("4. 서보2 (틸트, 상하) - 위")
        print("5. 서보2 (틸트, 상하) - 중앙")
        print("6. 서보2 (틸트, 상하) - 아래")
        print("7. 원점 복귀 (servo1=1185, servo2=1500)")
        print("0. 메인 메뉴로 돌아가기")

        choice = input("\n선택: ").strip()

        if choice == '1':
            print("서보1을 왼쪽으로...")
            board.pwm_servo_set_position(1, [[1, 1000]])
        elif choice == '2':
            print("서보1을 중앙으로...")
            board.pwm_servo_set_position(1, [[1, 1500]])
        elif choice == '3':
            print("서보1을 오른쪽으로...")
            board.pwm_servo_set_position(1, [[1, 2000]])
        elif choice == '4':
            print("서보2를 위로...")
            board.pwm_servo_set_position(1, [[2, 1000]])
        elif choice == '5':
            print("서보2를 중앙으로...")
            board.pwm_servo_set_position(1, [[2, 1500]])
        elif choice == '6':
            print("서보2를 아래로...")
            board.pwm_servo_set_position(1, [[2, 2000]])
        elif choice == '7':
            print("원점 복귀...")
            board.pwm_servo_set_position(1, [[1, 1185], [2, 1500]])
        elif choice == '0':
            break
        else:
            print("잘못된 선택입니다.")

        time.sleep(0.5)

def test_motors():
    """DC 모터 테스트"""
    global board, car

    clear_screen()
    print_header()
    print("\nDC 모터 테스트 (메카넘 휠)")
    print("-" * 70)
    print("주의: 로봇을 들어올리거나 안전한 곳에 배치하세요!")
    print("-" * 70)

    if board is None:
        board = rrc.Board()
    if car is None:
        car = mecanum.MecanumChassis()

    speed = 30

    while True:
        print("\n1. 전진 (2초)")
        print("2. 후진 (2초)")
        print("3. 좌측 이동 (2초)")
        print("4. 우측 이동 (2초)")
        print("5. 좌회전 (2초)")
        print("6. 우회전 (2초)")
        print("7. 개별 모터 테스트")
        print("8. 속도 조절 (현재: {})".format(speed))
        print("9. 정지")
        print("0. 메인 메뉴로 돌아가기")

        choice = input("\n선택: ").strip()

        if choice == '1':
            print("전진 중...")
            car.set_velocity(speed, 90, 0)
            time.sleep(2)
            car.set_velocity(0, 90, 0)
        elif choice == '2':
            print("후진 중...")
            car.set_velocity(speed, 270, 0)
            time.sleep(2)
            car.set_velocity(0, 90, 0)
        elif choice == '3':
            print("좌측 이동 중...")
            car.set_velocity(speed, 180, 0)
            time.sleep(2)
            car.set_velocity(0, 90, 0)
        elif choice == '4':
            print("우측 이동 중...")
            car.set_velocity(speed, 0, 0)
            time.sleep(2)
            car.set_velocity(0, 90, 0)
        elif choice == '5':
            print("좌회전 중...")
            car.set_velocity(0, 90, -1)
            time.sleep(2)
            car.set_velocity(0, 90, 0)
        elif choice == '6':
            print("우회전 중...")
            car.set_velocity(0, 90, 1)
            time.sleep(2)
            car.set_velocity(0, 90, 0)
        elif choice == '7':
            test_individual_motors()
        elif choice == '8':
            new_speed = input("새 속도 입력 (0-100): ").strip()
            try:
                speed = int(new_speed)
                if speed < 0 or speed > 100:
                    print("속도는 0-100 사이여야 합니다.")
                    speed = 30
                else:
                    print(f"속도가 {speed}로 설정되었습니다.")
            except:
                print("잘못된 입력입니다.")
        elif choice == '9':
            print("모터 정지...")
            car.set_velocity(0, 90, 0)
        elif choice == '0':
            car.set_velocity(0, 90, 0)
            break
        else:
            print("잘못된 선택입니다.")

def test_individual_motors():
    """개별 모터 테스트"""
    global board

    print("\n개별 모터 테스트")
    print("모터 배치: 1(왼쪽앞) 2(오른쪽앞) 3(왼쪽뒤) 4(오른쪽뒤)")

    motor_id = input("모터 번호 (1-4): ").strip()
    duty = input("Duty (-100 ~ 100): ").strip()

    try:
        motor_id = int(motor_id)
        duty = int(duty)

        if 1 <= motor_id <= 4 and -100 <= duty <= 100:
            print(f"모터 {motor_id}을(를) duty={duty}로 회전 (2초)...")
            board.set_motor_duty([[motor_id, duty]])
            time.sleep(2)
            board.set_motor_duty([[motor_id, 0]])
            print("정지")
        else:
            print("잘못된 범위입니다.")
    except:
        print("잘못된 입력입니다.")

def test_buzzer():
    """부저 테스트"""
    global board

    clear_screen()
    print_header()
    print("\n부저 테스트")
    print("-" * 70)

    if board is None:
        board = rrc.Board()

    while True:
        print("\n1. 도 (261 Hz)")
        print("2. 레 (293 Hz)")
        print("3. 미 (329 Hz)")
        print("4. 파 (349 Hz)")
        print("5. 솔 (392 Hz)")
        print("6. 라 (440 Hz)")
        print("7. 시 (493 Hz)")
        print("8. 사용자 정의 주파수")
        print("0. 메인 메뉴로 돌아가기")

        choice = input("\n선택: ").strip()

        frequencies = {
            '1': 261,
            '2': 293,
            '3': 329,
            '4': 349,
            '5': 392,
            '6': 440,
            '7': 493
        }

        if choice in frequencies:
            freq = frequencies[choice]
            print(f"{freq}Hz 소리 재생 (1초)...")
            board.set_buzzer(freq, 0.5)
            time.sleep(1)
        elif choice == '8':
            freq = input("주파수 입력 (Hz): ").strip()
            try:
                freq = int(freq)
                duration = input("지속 시간 (초): ").strip()
                duration = float(duration)
                print(f"{freq}Hz 소리 재생 ({duration}초)...")
                board.set_buzzer(freq, duration)
                time.sleep(duration + 0.5)
            except:
                print("잘못된 입력입니다.")
        elif choice == '0':
            break
        else:
            print("잘못된 선택입니다.")

def test_rgb_led():
    """RGB LED 테스트"""
    global board

    clear_screen()
    print_header()
    print("\n RGB LED 테스트 (초음파 센서)")
    print("-" * 70)

    if board is None:
        board = rrc.Board()

    global sonar
    if sonar is None:
        sonar = Sonar.Sonar()
        sonar.setRGBMode(0)

    while True:
        print("\n1. 빨강 (Red)")
        print("2. 녹색 (Green)")
        print("3. 파랑 (Blue)")
        print("4. 노랑 (Yellow)")
        print("5. 자홍 (Magenta)")
        print("6. 청록 (Cyan)")
        print("7. 흰색 (White)")
        print("8. 끄기 (Off)")
        print("9. 사용자 정의 RGB")
        print("0. 메인 메뉴로 돌아가기")

        choice = input("\n선택: ").strip()

        colors = {
            '1': (255, 0, 0),    # Red
            '2': (0, 255, 0),    # Green
            '3': (0, 0, 255),    # Blue
            '4': (255, 255, 0),  # Yellow
            '5': (255, 0, 255),  # Magenta
            '6': (0, 255, 255),  # Cyan
            '7': (255, 255, 255),# White
            '8': (0, 0, 0)       # Off
        }

        if choice in colors:
            color = colors[choice]
            print(f"LED를 RGB{color}로 설정...")
            sonar.setPixelColor(0, color)
            sonar.setPixelColor(1, color)
        elif choice == '9':
            try:
                r = int(input("R (0-255): ").strip())
                g = int(input("G (0-255): ").strip())
                b = int(input("B (0-255): ").strip())
                if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                    print(f"LED를 RGB({r},{g},{b})로 설정...")
                    sonar.setPixelColor(0, (r, g, b))
                    sonar.setPixelColor(1, (r, g, b))
                else:
                    print("0-255 범위로 입력하세요.")
            except:
                print("잘못된 입력입니다.")
        elif choice == '0':
            sonar.setPixelColor(0, (0, 0, 0))
            sonar.setPixelColor(1, (0, 0, 0))
            break
        else:
            print("잘못된 선택입니다.")

def test_ultrasonic():
    """초음파 센서 테스트"""
    global sonar

    clear_screen()
    print_header()
    print("\n초음파 센서 테스트")
    print("-" * 70)

    if sonar is None:
        sonar = Sonar.Sonar()

    print("\n거리 측정 중... (Ctrl+C로 중지)")
    print("-" * 70)

    try:
        while True:
            distance = sonar.getDistance() / 10.0  # mm to cm
            print(f"\r거리: {distance:.1f} cm    ", end='', flush=True)
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("\n\n측정 중지")

    input("\nEnter를 눌러 메인 메뉴로...")

def test_line_sensor():
    """라인 센서 테스트"""
    clear_screen()
    print_header()
    print("\n라인 센서 테스트")
    print("-" * 70)

    try:
        from HiwonderSDK.FourInfrared import FourInfrared
        sensor = FourInfrared()

        print("\n센서 값 읽기 중... (Ctrl+C로 중지)")
        print("센서 배치: [1] [2] [3] [4]")
        print("-" * 70)

        while True:
            data = sensor.readData()
            print(f"\r센서 값: {data}    ", end='', flush=True)
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\n\n측정 중지")
    except Exception as e:
        print(f"\n오류: {e}")

    input("\nEnter를 눌러 메인 메뉴로...")

def test_camera():
    """카메라 테스트"""
    clear_screen()
    print_header()
    print("\n카메라 테스트")
    print("-" * 70)

    print("\n1. 카메라 열기 테스트")
    print("2. 스냅샷 저장")
    print("3. 영상 스트리밍 서버 확인")
    print("0. 메인 메뉴로 돌아가기")

    choice = input("\n선택: ").strip()

    if choice == '1':
        try:
            import cv2
            print("\n카메라 열기 시도...")
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                print("✓ 카메라 열림 성공")
                ret, frame = cap.read()
                if ret:
                    print(f"✓ 프레임 읽기 성공: {frame.shape}")
                else:
                    print("✗ 프레임 읽기 실패")
                cap.release()
            else:
                print("✗ 카메라 열기 실패")
        except Exception as e:
            print(f"오류: {e}")
        input("\nEnter를 눌러 계속...")

    elif choice == '2':
        try:
            print("\n스냅샷 저장 중...")
            result = subprocess.run(
                ['curl', '-s', 'http://192.168.0.11:8080/?action=snapshot',
                 '-o', '/tmp/snapshot.jpg'],
                capture_output=True, timeout=5
            )
            if result.returncode == 0:
                print("✓ 스냅샷 저장됨: /tmp/snapshot.jpg")
            else:
                print("✗ 스냅샷 저장 실패")
        except Exception as e:
            print(f"오류: {e}")
        input("\nEnter를 눌러 계속...")

    elif choice == '3':
        print("\n영상 스트리밍 서버 상태:")
        try:
            result = subprocess.run(['sudo', 'ss', '-tlnp'],
                                  capture_output=True, text=True)
            if ':8080' in result.stdout:
                print("✓ 서버 실행 중: http://192.168.0.11:8080/")
            else:
                print("✗ 서버 중지됨")
        except:
            print("✗ 상태 확인 실패")
        input("\nEnter를 눌러 계속...")

def run_motor_calibration():
    """모터 캘리브레이션 실행"""
    clear_screen()
    print_header()
    print("\n모터 캘리브레이션 프로그램 실행")
    print("-" * 70)
    print("\n별도 프로그램으로 실행합니다...")
    input("\nEnter를 눌러 시작...")

    try:
        subprocess.run(['python3', '/home/yourshlee/TurboPi/motor_calibration.py'])
    except KeyboardInterrupt:
        print("\n캘리브레이션 중단됨")
    except Exception as e:
        print(f"오류: {e}")

    input("\nEnter를 눌러 메인 메뉴로...")

def main_menu():
    """메인 메뉴"""
    while True:
        clear_screen()
        print_header()
        print_status()

        print("\n메인 메뉴")
        print("-" * 70)
        print("1. 서보 모터 테스트")
        print("2. DC 모터 테스트 (메카넘 휠)")
        print("3. 부저 테스트")
        print("4. RGB LED 테스트")
        print("5. 초음파 센서 테스트")
        print("6. 라인 센서 테스트")
        print("7. 카메라 테스트")
        print("8. 모터 캘리브레이션")
        print("9. 기기 상태 새로고침")
        print("0. 종료")
        print("-" * 70)

        choice = input("\n선택: ").strip()

        if choice == '1':
            test_servo()
        elif choice == '2':
            test_motors()
        elif choice == '3':
            test_buzzer()
        elif choice == '4':
            test_rgb_led()
        elif choice == '5':
            test_ultrasonic()
        elif choice == '6':
            test_line_sensor()
        elif choice == '7':
            test_camera()
        elif choice == '8':
            run_motor_calibration()
        elif choice == '9':
            continue
        elif choice == '0':
            print("\n프로그램을 종료합니다.")
            # 모든 모터 정지
            if board is not None:
                board.set_motor_duty([[1, 0], [2, 0], [3, 0], [4, 0]])
            if car is not None:
                car.set_velocity(0, 90, 0)
            if sonar is not None:
                sonar.setPixelColor(0, (0, 0, 0))
                sonar.setPixelColor(1, (0, 0, 0))
            break
        else:
            print("\n잘못된 선택입니다.")
            time.sleep(1)

if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n프로그램이 중단되었습니다.")
        # 모든 모터 정지
        if board is not None:
            board.set_motor_duty([[1, 0], [2, 0], [3, 0], [4, 0]])
    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()
