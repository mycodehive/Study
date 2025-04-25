import streamlit as st
import cv2
import time
from getposedata import process_frame
import mediapipe as mp
import datetime
from zoneinfo import ZoneInfo

# 페이지 설정
st.set_page_config(
    page_title="지능형 노인 낙상 감지 및 인터랙티브 알림 시스템",
    layout="wide"
)

# 언어 및 스타일 설정
kst_now = datetime.datetime.now(ZoneInfo("Asia/Seoul"))
timestamp = kst_now.strftime("%Y%m%d_%H%M%S")

# 세션 상태 초기화
if 'history' not in st.session_state:
    st.session_state.history = []

# 화면 2분할 구성
col1, col2 = st.columns([1, 1])

# col1: 영상 출력용 요소 정의
with col1:
    st.title("📷 실시간 관절 추출")

    if 'camera' not in st.session_state:
        st.session_state.camera = None

    # 카메라 시작/종료 버튼을 가로로 나란히 배치
    button_col1, button_col2, button_col3 = st.columns([2, 2, 2], gap="small")
    with button_col1:
        start = st.button("카메라 시작")
    with button_col2:
        stop = st.button("카메라 종료")
    with button_col3:
        print("")
    frame_display = st.empty()  # 영상 표시용

# col2: landmark 정보 출력용 요소 정의
with col2:
    landmark_info = st.empty()  # 관절 정보 표시용
    history_area = st.container()  # 최근 히스토리 표시용 컨테이너

    # 카메라 시작 처리
    if start:
        st.session_state.camera = cv2.VideoCapture(0)

    # 카메라 종료 처리
    if stop and st.session_state.camera:
        st.session_state.camera.release()
        st.session_state.camera = None

    # 실시간 프레임 처리 루프
    last_print_time = 0
    if st.session_state.camera and st.session_state.camera.isOpened():
        while True:
            ret, frame = st.session_state.camera.read()
            if not ret:
                st.warning("카메라 프레임을 읽을 수 없습니다.")
                break

            image, landmarks = process_frame(frame)
            frame_display.image(image, channels="RGB")

            current_time = time.time()
            if landmarks and current_time - last_print_time >= 1:
                left_shoulder = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
                right_shoulder = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER]
                left_knee = landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE]
                right_knee = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_KNEE]

                landmark_info.markdown(f"""
                ### 🦴 관절 정보
                |구분|X좌표|Y좌표|Z좌표|신뢰도|적합|
                |:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
                |**왼쪽 어깨**|{left_shoulder.x:.3f}|{left_shoulder.y:.3f}|{left_shoulder.z:.3f}|{left_shoulder.visibility:.2f}|{"적합" if left_shoulder.visibility > 0.7 else "부적합"}|
                |**오른쪽 어깨**|{right_shoulder.x:.3f}|{right_shoulder.y:.3f}|{right_shoulder.z:.3f}|{right_shoulder.visibility:.2f}|{"적합" if right_shoulder.visibility > 0.7 else "부적합"}|
                |**왼쪽 무릎**|{left_knee.x:.3f}|{left_knee.y:.3f}|{left_knee.z:.3f}|{left_knee.visibility:.2f}|{"적합" if left_knee.visibility > 0.7 else "부적합"}|
                |**오른쪽 무릎**|{right_knee.x:.3f}|{right_knee.y:.3f}|{right_knee.z:.3f}|{right_knee.visibility:.2f}|{"적합" if right_knee.visibility > 0.7 else "부적합"}|
                """)
                last_print_time = current_time
            time.sleep(0.03)