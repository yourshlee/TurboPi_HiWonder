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

## 2025-12-18 (수) - 하드웨어 점검 및 테스트 도구 개발

### 작업 내용

#### 1. 하드웨어 전체 점검
**서보 모터 점검:**
- 모든 부품 정상 작동 확인
- 서보 케이블 연결 확인 및 방향 수정 완료
- servo1 (팬): 1185, servo2 (틸트): 1500

**메카넘 휠 주행 테스트:**
- 전진/후진 테스트 완료 ✓
- 좌우 이동 테스트 시도 (방향 이상 발견)
- 회전 테스트 시도 (혼란스러운 동작 발견)
- 원인: 모터 배선 또는 방향 설정 문제로 추정

#### 2. 배터리 전압 모니터링
**전압 변화 추이:**
- 작업 시작: 7.50V (만충)
- 1시간 후: 7.29V
- 2시간 후: 7.13V
- 3시간 후: 6.84V
- 작업 종료: **6.29V** (위험 수준)

**발견 사항:**
- 배터리 방전 속도가 빠름 (약 3시간에 1.2V 감소)
- 모터 테스트 중 전원이 나가는 문제 발생
- 배터리 커넥터 접촉 문제 또는 배터리 노후 가능성

#### 3. 개발 도구 작성

**모터 캘리브레이션 프로그램 (`motor_calibration.py`):**
- 각 모터(1-4)를 개별적으로 테스트
- 정방향/역방향 회전 방향 확인
- 사용자 입력으로 회전 방향 기록
- 자동 진단 및 문제점 분석
- 결과를 파일로 저장

**배터리 전압 확인 프로그램 (`check_voltage.py`):**
- 실시간 배터리 전압 측정
- 배터리 상태 표시 (만충~위험)
- TurboPi 서버와 독립적으로 실행 가능

**통합 단위 테스트 메뉴 (`unit_test_menu.py`):**
- 모든 하드웨어 컴포넌트 테스트 메뉴
- 실시간 기기 상태 모니터링
- 테스트 항목:
  - 서보 모터 (팬/틸트)
  - DC 모터 (메카넘 휠, 개별 모터)
  - 부저 (음계, 사용자 정의)
  - RGB LED (7색 + 사용자 정의)
  - 초음파 센서 (실시간 거리)
  - 라인 센서 (4채널)
  - 카메라 (열기, 스냅샷, 서버)
  - 모터 캘리브레이션 통합

#### 4. 카메라 화질 개선 시도
**개선 작업:**
- JPEG 압축 품질: 70 → 90
- 리사이즈 알고리즘: INTER_NEAREST → INTER_LINEAR
- 카메라 설정: sharpness=8, contrast=35 추가

**결과:**
- 약간의 개선은 있었으나 근본적인 한계 확인
- 640x480 저가형 카메라의 하드웨어 한계
- AI 학습용으로는 충분하지만 고화질 영상은 불가

**카메라 문제 발생:**
- 테스트 중 카메라가 응답하지 않는 문제 발생
- USB 재연결 필요
- 라즈베리파이 재부팅 권장

#### 5. RGB LED 제어
**초음파 센서 RGB LED 의미 파악:**
- ColorTracking 기능에서 추적 색상 표시용
- Red: 빨간색 물체 추적
- Green: 녹색 물체 추적
- Blue: 파란색 물체 추적
- 기본 상태: 꺼짐

**제어:**
- Blue LED 꺼짐 확인
- RGB LED 제어 기능 단위 테스트 메뉴에 통합

### Git 커밋
- 커밋 1: "영상 화질 개선: JPEG 품질 및 리사이즈 알고리즘 최적화"
  - MjpgServer.py, Camera.py 수정

### 발견된 문제점
1. **메카넘 휠 방향 문제**
   - 좌우 이동 시 회전하는 현상
   - 모터 배선 또는 소프트웨어 설정 문제
   - 모터 캘리브레이션 필요

2. **배터리 빠른 방전**
   - 3시간 사용으로 7.5V → 6.3V
   - 배터리 상태 점검 필요
   - 충전 후 재테스트 필요

3. **카메라 불안정**
   - 간헐적으로 응답 없음
   - USB 연결 불안정 가능성
   - 재부팅으로 해결 가능

### 다음 단계 (2025-12-19 예정)
1. ✅ **배터리 충전** (7.4V까지)
2. 모터 캘리브레이션 완료
3. 메카넘 휠 방향 수정
4. 메카넘 휠 주행 테스트 완료
5. RPC API 원격 제어 테스트
6. AI 기능 테스트 (ColorTracking, LineFollower, Avoidance)

### 참고사항
- 배터리 방전 속도가 빠르므로 USB-C 전원 사용 권장
- 카메라 문제 발생 시 USB 재연결 또는 재부팅
- 모터 캘리브레이션 프로그램 사용법:
  ```bash
  python3 /home/yourshlee/TurboPi/motor_calibration.py
  ```
- 단위 테스트 메뉴 사용법:
  ```bash
  python3 /home/yourshlee/TurboPi/unit_test_menu.py
  ```

---

## 작업 메모
- 라즈베리파이 5에서 작업 진행 중
- 매일 작업 종료 시 GitHub 업데이트 예정
- 일 단위 작업 내용 요약 및 메모 진행
