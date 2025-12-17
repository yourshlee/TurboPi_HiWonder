#!/usr/bin/python3
# coding=utf8
"""
메카넘 휠 모터 캘리브레이션 프로그램

각 모터를 개별적으로 테스트하여 방향과 배선을 확인합니다.
"""

import sys
sys.path.append('/home/yourshlee/TurboPi/')
import time
import HiwonderSDK.ros_robot_controller_sdk as rrc

def test_motor(board, motor_id, duty):
    """
    특정 모터를 테스트합니다.

    Args:
        board: ros_robot_controller_sdk.Board 객체
        motor_id: 모터 번호 (1-4)
        duty: 모터 duty (-100 ~ 100)
    """
    print(f"\n모터 {motor_id}을(를) duty={duty}로 회전시킵니다...")
    print("(2초 동안 회전합니다)")

    # 모터 회전
    board.set_motor_duty([[motor_id, duty]])
    time.sleep(2)

    # 정지
    board.set_motor_duty([[motor_id, 0]])
    time.sleep(0.5)

def main():
    print("=" * 60)
    print("메카넘 휠 모터 캘리브레이션 프로그램")
    print("=" * 60)
    print()
    print("로봇을 들어올려서 바퀴가 바닥에 닿지 않도록 해주세요.")
    print("또는 바퀴가 자유롭게 회전할 수 있도록 배치해주세요.")
    print()

    input("준비되었으면 Enter를 누르세요...")

    # Board 초기화
    board = rrc.Board()
    time.sleep(0.5)

    print("\n" + "=" * 60)
    print("모터 배치 (위에서 본 모습)")
    print("=" * 60)
    print()
    print("     모터1 (왼쪽 앞)        모터2 (오른쪽 앞)")
    print("            ↖                    ↗")
    print("              \\                /")
    print("                \\            /")
    print("                  [ 로봇 ]")
    print("                /            \\")
    print("              /                \\")
    print("            ↙                    ↘")
    print("     모터3 (왼쪽 뒤)        모터4 (오른쪽 뒤)")
    print()
    print("=" * 60)
    print()

    # 각 모터 테스트 결과 저장
    results = {}

    for motor_id in range(1, 5):
        print("\n" + "=" * 60)
        print(f"모터 {motor_id} 테스트")
        print("=" * 60)

        # 위치 확인
        motor_positions = {
            1: "왼쪽 앞",
            2: "오른쪽 앞",
            3: "왼쪽 뒤",
            4: "오른쪽 뒤"
        }
        print(f"\n모터 {motor_id}의 예상 위치: {motor_positions[motor_id]}")

        # 정방향 테스트 (duty = +50)
        test_motor(board, motor_id, 50)

        print("\n바퀴가 어떻게 회전했나요?")
        print("1. 시계 방향 (CW)")
        print("2. 반시계 방향 (CCW)")
        print("3. 회전 안함")
        forward_direction = input("선택 (1-3): ").strip()

        # 역방향 테스트 (duty = -50)
        test_motor(board, motor_id, -50)

        print("\n바퀴가 어떻게 회전했나요?")
        print("1. 시계 방향 (CW)")
        print("2. 반시계 방향 (CCW)")
        print("3. 회전 안함")
        backward_direction = input("선택 (1-3): ").strip()

        # 결과 저장
        results[motor_id] = {
            'forward': forward_direction,
            'backward': backward_direction
        }

        print(f"\n모터 {motor_id} 테스트 완료")

    # 모든 모터 정지
    board.set_motor_duty([[1, 0], [2, 0], [3, 0], [4, 0]])

    # 결과 출력
    print("\n" + "=" * 60)
    print("테스트 결과")
    print("=" * 60)

    direction_map = {
        '1': 'CW (시계방향)',
        '2': 'CCW (반시계방향)',
        '3': '회전안함'
    }

    for motor_id in range(1, 5):
        forward = results[motor_id]['forward']
        backward = results[motor_id]['backward']
        print(f"\n모터 {motor_id} ({motor_positions[motor_id]}):")
        print(f"  duty=+50 : {direction_map.get(forward, '알수없음')}")
        print(f"  duty=-50 : {direction_map.get(backward, '알수없음')}")

        # 방향 일관성 체크
        if forward == '1' and backward == '2':
            print("  ✓ 정상 (방향이 올바름)")
        elif forward == '2' and backward == '1':
            print("  ✓ 정상 (방향이 올바름)")
        elif forward == backward:
            print("  ✗ 문제: duty 부호를 바꿔도 같은 방향으로 회전")
        elif forward == '3' or backward == '3':
            print("  ✗ 문제: 모터가 회전하지 않음 (배선 또는 전원 문제)")
        else:
            print("  ? 확인 필요")

    print("\n" + "=" * 60)
    print("캘리브레이션 권장 사항")
    print("=" * 60)

    # 메카넘 휠의 정상 패턴
    # 전진할 때: 모든 바퀴가 앞으로 굴러가야 함
    # 왼쪽 바퀴(1,3): duty가 양수일 때 바퀴 표면이 앞으로 (CCW)
    # 오른쪽 바퀴(2,4): duty가 양수일 때 바퀴 표면이 앞으로 (CW)

    print("\n정상 동작 패턴 (전진을 위한 회전 방향):")
    print("- 왼쪽 바퀴 (모터1, 모터3): duty가 양수일 때 반시계(CCW) 회전")
    print("- 오른쪽 바퀴 (모터2, 모터4): duty가 양수일 때 시계(CW) 회전")
    print()

    # 문제 진단
    issues = []
    for motor_id in [1, 3]:  # 왼쪽 바퀴
        forward = results[motor_id]['forward']
        if forward == '1':  # CW when positive duty
            issues.append(f"모터{motor_id}: 방향 반전 필요 (현재 CW, 필요 CCW)")

    for motor_id in [2, 4]:  # 오른쪽 바퀴
        forward = results[motor_id]['forward']
        if forward == '2':  # CCW when positive duty
            issues.append(f"모터{motor_id}: 방향 반전 필요 (현재 CCW, 필요 CW)")

    if issues:
        print("발견된 문제:")
        for issue in issues:
            print(f"  - {issue}")
        print()
        print("해결 방법:")
        print("  1. 하드웨어: 해당 모터의 +/- 배선을 바꿔 연결")
        print("  2. 소프트웨어: mecanum.py 파일에서 해당 모터의 부호 반전")
    else:
        print("✓ 모든 모터가 올바른 방향으로 회전합니다!")

    print("\n" + "=" * 60)

    # 결과를 파일로 저장
    with open('/home/yourshlee/TurboPi/motor_calibration_result.txt', 'w') as f:
        f.write("메카넘 휠 모터 캘리브레이션 결과\n")
        f.write("=" * 60 + "\n\n")
        for motor_id in range(1, 5):
            forward = results[motor_id]['forward']
            backward = results[motor_id]['backward']
            f.write(f"모터 {motor_id} ({motor_positions[motor_id]}):\n")
            f.write(f"  duty=+50 : {direction_map.get(forward, '알수없음')}\n")
            f.write(f"  duty=-50 : {direction_map.get(backward, '알수없음')}\n\n")

        if issues:
            f.write("\n발견된 문제:\n")
            for issue in issues:
                f.write(f"  - {issue}\n")
        else:
            f.write("\n✓ 모든 모터가 올바른 방향으로 회전합니다!\n")

    print("\n결과가 'motor_calibration_result.txt' 파일에 저장되었습니다.")
    print()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n프로그램이 중단되었습니다.")
        # 모든 모터 정지
        board = rrc.Board()
        board.set_motor_duty([[1, 0], [2, 0], [3, 0], [4, 0]])
    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()
