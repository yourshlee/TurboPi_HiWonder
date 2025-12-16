# TurboPi 작업 이력

## 2025-12-16 (월) - 초기 설정

### 작업 환경
- **하드웨어**: Raspberry Pi 5
- **OS**: Linux 6.12.47+rpt-rpi-2712
- **Python**: 3.13.5
- **작업 디렉토리**: `/home/yourshlee/TurboPi`

### 완료된 작업

#### 1. Git 저장소 설정
- 원본 저장소 Fork: `Hiwonder/TurboPi` → `yourshlee/TurboPi_HiWonder`
- 원격 저장소 설정 완료
  - **origin**: `git@github.com:yourshlee/TurboPi_HiWonder.git` (SSH)
  - **upstream**: `https://github.com/Hiwonder/TurboPi.git`
- Git 사용자 설정
  - Name: yourshlee
  - Email: yourshlee@gmail.com
- SSH 키 설정 완료 (Raspberry Pi 5)

#### 2. 개발 환경 구성
**설치된 패키지:**
- numpy 2.2.4
- opencv 4.10.0
- PyYAML (python3-yaml 6.0.2)
- json-rpc 1.15.0 (RPC 서버용)
- pandas 2.3.3 (데이터 처리용)
- pyzbar 0.1.9 (QR 코드 인식용)
- werkzeug, pillow, smbus2, gpiod, pyserial (기존 설치)

**미설치 패키지:**
- mediapipe (Python 3.13 + ARM64 아키텍처 미지원)
  - 영향받는 기능: FaceTracking, GestureRecognition
  - 해결방안: Python 3.11/3.12 가상환경 필요 (추후 작업)
  - 임시 해결: RPCServer.py에 조건부 import 추가로 나머지 기능 사용 가능

#### 3. 코드 수정
**경로 수정 작업:**
- 변경 내용: `/home/pi/TurboPi` → `/home/yourshlee/TurboPi`
- 수정된 파일: 23개
  - TurboPi.py (메인 프로그램)
  - yaml_handle.py (설정 파일 경로)
  - Functions/*.py (11개 기능 모듈)
  - HiwonderSDK/*.py (4개 SDK 파일)
  - MecanumControl/*.py (5개 메카넘 제어 데모)
  - CameraCalibration/CalibrationConfig.py
  - RPCServer.py

#### 4. 하드웨어 테스트
- 테스트 스크립트: `HiwonderSDK/hardware_test.py`
- 결과: **성공**
  - PWM 서보 모터 (2개) 정상 작동
  - DC 모터 (4개) 정상 작동

#### 5. Git 커밋 및 푸시
- 커밋: "초기 설정: 경로를 /home/pi에서 /home/yourshlee로 변경"
- GitHub 푸시 완료: https://github.com/yourshlee/TurboPi_HiWonder

#### 6. 메인 프로그램 테스트
**TurboPi.py 실행 테스트:**
- RPC 서버 정상 작동 확인 (Port 9030)
- MJPG 비디오 스트리밍 서버 정상 작동 확인 (Port 8080)
- 라즈베리파이 IP: 192.168.0.11

**접속 URL:**
- 비디오 스트림: http://192.168.0.11:8080/
- 스냅샷: http://192.168.0.11:8080/?action=snapshot
- RPC API: http://192.168.0.11:9030/

**테스트 결과:**
- ✅ RPC 서버 응답 정상 (JSON-RPC 2.0)
- ✅ 프로세스 정상 실행
- ✅ 포트 바인딩 정상

### 사용 가능한 기능
현재 테스트 가능한 기능들 (mediapipe 불필요):
- ✅ ColorTracking (색상 추적)
- ✅ ColorDetect (색상 감지)
- ✅ LineFollower (라인 따라가기)
- ✅ Avoidance (장애물 회피)
- ✅ QuickMark (QR 코드 인식)
- ✅ RemoteControl (원격 제어)
- ✅ 메카넘 휠 제어 (전방향 이동)
- ❌ FaceTracking (얼굴 추적) - mediapipe 필요
- ❌ GestureRecognition (손동작 인식) - mediapipe 필요

#### 7. 하드웨어 부품 점검 (체계적 테스트)
**전원 설정:**
- USB-C 전원 사용 (개발/테스트용)
- 측정 전압: 4.54~4.55V (안정적)
- 실제 주행은 7.4V 배터리 권장

**테스트 결과:**

| 부품 | 상태 | 테스트 내용 |
|------|------|------------|
| PWM 서보 (2개) | ✅ 정상 | 카메라 팬틸트 상하좌우 작동 확인 |
| DC 모터 (4개) | ✅ 정상 | 메카넘 휠 4개 정방향/역방향 회전 |
| 부저 (Buzzer) | ✅ 정상 | 여러 주파수 소리 출력 |
| RGB LED | ✅ 정상 | 초음파 센서 7색 LED 표시 |
| 초음파 센서 | ✅ 정상 | 거리 측정 (약 5.4m) |
| 라인 센서 (4채널) | ✅ 정상 | 검은색/흰색 감지 |
| USB 카메라 | ⏸️ 보류 | 프로세스 충돌, Camera.py 수정 필요 |

**코드 수정:**
- Camera.py: VideoCapture(-1) → VideoCapture(0) 명시적 디바이스 지정
- TurboPi.py: cam.camera_open() 추가로 시작 시 카메라 자동 열기

**발견 사항:**
- icspring USB 카메라 확인 (/dev/video0, /dev/video1)
- 모든 하드웨어 정상 조립 및 연결 확인
- USB-C 전원으로 센서/서보 정상 작동

### 다음 단계
1. ~~메인 프로그램 실행 테스트 (`python3 TurboPi.py`)~~ ✅ 완료
2. ~~하드웨어 부품 점검~~ ✅ 완료
3. 카메라 영상 스트리밍 문제 해결
4. 기본 AI 기능 테스트 (ColorTracking, LineFollower 등)
5. 메카넘 휠 주행 테스트
6. Python 3.11 가상환경 구성 (mediapipe 설치용)

### 참고사항
- 부품 목록: 첨부 이미지 참조
- TurboPi 하드웨어: HiWonder사 AI Vision Robot Car
- 공식 문서: https://docs.hiwonder.com/projects/TurboPi/en/standard/

---

## 2025-12-17 (화) - 서보 모터 조정 및 전압 측정 개선

### 작업 내용

#### 1. 서보 케이블 교체 및 방향 수정
**문제 발견:**
- 초기 테스트에서 servo1(팬)과 servo2(틸트)의 케이블이 반대로 연결됨
- servo1 명령 → 상하 움직임 (틸트)
- servo2 명령 → 좌우 움직임 (팬)

**해결 방법:**
1. 하드웨어 수정: 서보 케이블 교체 (servo1 ↔ servo2 포트)
2. 소프트웨어 수정: 방향 반전 로직 추가
   - 파일: `HiwonderSDK/ros_robot_controller_sdk.py:354-365`
   - 수정 내용:
     ```python
     # Servo1, Servo2 방향 반전 (케이블 연결로 인한 방향 반대 문제 해결)
     if servo_id == 1:
         value = 3000 - value
     if servo_id == 2:
         value = 3000 - value
     ```
   - 효과: 모든 AI 기능에서 일관된 방향으로 작동

**테스트 결과:**
- ✅ servo1 (팬, 좌우): 1000=왼쪽, 2000=오른쪽, 1500=중앙
- ✅ servo2 (틸트, 상하): 1000=위, 2000=아래, 1500=중앙

#### 2. 서보 영점 조정
**카메라 팬(servo1) 조정:**
- 초기값: 1500 (중앙)
- 문제: 카메라가 정면을 향하지 않음
- 조정 과정:
  1. 1500 → 1430 (70 왼쪽)
  2. 1430 → 1290 (140 추가 왼쪽)
  3. 1290 → 1185 (105 추가 왼쪽)
- **최종값: 1185** (카메라 정면 향함)

**카메라 틸트(servo2) 조정:**
- 값: 1500 (중앙 위치 유지)

**저장 위치:**
- `servo_config.yaml`:
  ```yaml
  servo1: 1185
  servo2: 1500
  ```

#### 3. 배터리 전압 측정 문제 해결
**문제:**
- `print_voltage.py` 실행 시 전압값이 `None`으로 표시됨
- 배터리(7.4V) 연결 상태인데도 측정 실패

**원인 분석:**
- `board.get_battery()` 함수는 큐(queue) 기반 데이터 수신 방식
- `board.enable_reception()`을 호출하지 않으면 보드에서 전송하는 배터리 데이터를 수신하지 못함
- 코드 위치: `HiwonderSDK/ros_robot_controller_sdk.py:178-190`

**해결:**
- `print_voltage.py` 수정:
  ```python
  board = rrc.Board()
  board.enable_reception()  # 배터리 데이터 수신 활성화
  time.sleep(0.5)  # 데이터 수신 대기
  voltage = board.get_battery()
  ```

**측정 결과:**
- 배터리 전압: **6.98~7.04V** (정상 범위)
- 7.4V 만충 기준 약 95% 수준

#### 4. 추가 발견 사항
**서보 동작 특성:**
- 작은 변화량(70~100) 명령은 서보 데드존(Dead Zone)에 걸려서 무시됨
- 큰 변화량(500 이상) 명령만 확실히 동작
- 안정된 위치에서 큰 변화를 줄 때 가장 확실한 동작 보장

**전압 측정 범위:**
- TurboPi.py는 배터리 전압 범위를 `5.0V < voltage < 8.5V`로 필터링
- USB-C 전원(4.5~4.6V)은 이 범위를 벗어나 `None`으로 표시됨 (정상 동작)

### Git 커밋
- 커밋 메시지: "서보 모터 방향 수정 및 영점 조정 완료"
- 수정 파일:
  - `HiwonderSDK/ros_robot_controller_sdk.py` (servo 방향 반전)
  - `servo_config.yaml` (servo1 = 1185)
  - `print_voltage.py` (enable_reception 추가)
  - `Camera.py`, `HiwonderSDK/FourInfrared.py` (기존 수정 유지)
- GitHub 푸시 완료

### 다음 단계
1. 메카넘 휠 기본 주행 테스트 (전진/후진/좌우/회전)
2. RPC API 원격 제어 테스트
3. ColorTracking (색상 추적) 기능 테스트
4. LineFollower (라인 따라가기) 기능 테스트
5. Avoidance (장애물 회피) 기능 테스트

---

## 작업 메모
- 라즈베리파이 5에서 작업 진행 중
- 매일 작업 종료 시 GitHub 업데이트 예정
- 일 단위 작업 내용 요약 및 메모 진행
