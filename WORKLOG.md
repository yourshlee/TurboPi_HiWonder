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

### 다음 단계
1. ~~메인 프로그램 실행 테스트 (`python3 TurboPi.py`)~~ ✅ 완료
2. 기본 AI 기능 테스트 (ColorTracking, LineFollower 등)
3. 카메라 캘리브레이션
4. 메카넘 휠 제어 테스트
5. 웹 브라우저로 비디오 스트림 확인
6. Python 3.11 가상환경 구성 (mediapipe 설치용)

### 참고사항
- 부품 목록: 첨부 이미지 참조
- TurboPi 하드웨어: HiWonder사 AI Vision Robot Car
- 공식 문서: https://docs.hiwonder.com/projects/TurboPi/en/standard/

---

## 작업 메모
- 라즈베리파이 5에서 작업 진행 중
- 매일 작업 종료 시 GitHub 업데이트 예정
- 일 단위 작업 내용 요약 및 메모 진행
