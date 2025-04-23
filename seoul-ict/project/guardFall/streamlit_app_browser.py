import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode
from streamlit_autorefresh import st_autorefresh
import cv2
import mediapipe as mp
import time
import av
import queue
import threading

# 페이지 설정
st.set_page_config(page_title="관절 추출", layout="wide")
st.title("📷 브라우저 카메라로 관절 추출")

# 🔄 3초마다 새로고침
st_autorefresh(interval=3000, key="pose_refresh")

# MediaPipe 설정
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Queue: 스레드 간 데이터 전달
info_queue = queue.Queue()

# 영상 처리 클래스
class PoseProcessor(VideoProcessorBase):
    def __init__(self):
        self.pose = mp_pose.Pose()
        self.last_print_time = time.time()

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        print("🔄 프레임 수신 중")
        img = frame.to_ndarray(format="bgr24")
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.pose.process(img_rgb)

        if results.pose_landmarks:
            print("✅ 관절 감지됨")
            mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            current_time = time.time()
            if current_time - self.last_print_time >= 1:  # 1초 간격으로 전송
                landmarks = results.pose_landmarks.landmark
                msg = {
                    "left_shoulder": landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER],
                    "right_shoulder": landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER],
                    "left_knee": landmarks[mp_pose.PoseLandmark.LEFT_KNEE],
                    "right_knee": landmarks[mp_pose.PoseLandmark.RIGHT_KNEE],
                }
                info_queue.put(msg)
                print("📬 좌표 전송됨")
                self.last_print_time = current_time
        else:
            print("❌ 관절 감지 안됨")

        return av.VideoFrame.from_ndarray(img, format="bgr24")

# ▶️ 관절 정보 지속 소비 쓰레드
def pose_listener():
    while True:
        try:
            msg = info_queue.get(timeout=1)
            st.session_state.latest_pose = msg
        except queue.Empty:
            continue

# Thread 시작 (앱 최초 실행 시 1회만)
if 'listener_started' not in st.session_state:
    threading.Thread(target=pose_listener, daemon=True).start()
    st.session_state.listener_started = True

# 2열 화면 구성
col1, col2 = st.columns([1, 1])

# 📹 좌측: 카메라 영상
with col1:
    st.subheader("실시간 카메라 영상")
    webrtc_streamer(
        key="pose",
        mode=WebRtcMode.SENDRECV,
        video_processor_factory=PoseProcessor,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

# 🦴 우측: 관절 정보 출력
with col2:
    st.subheader("관절 좌표 정보")
    info_box = st.empty()

    # 초기화
    if "latest_pose" not in st.session_state:
        st.session_state.latest_pose = None

    # UI 출력
    if st.session_state.latest_pose:
        msg = st.session_state.latest_pose
        info_box.markdown(f"""
        ### ⏱ 최신 관절 정보  
        |구분|X좌표|Y좌표|Z좌표|신뢰도|적합도|
        |:--:|:--:|:--:|:--:|:--:|:--:|
        |왼쪽 어깨|{msg['left_shoulder'].x:.3f}|{msg['left_shoulder'].y:.3f}|{msg['left_shoulder'].z:.3f}|{msg['left_shoulder'].visibility:.2f}|{"적합" if msg['left_shoulder'].visibility > 0.7 else "부적합"}|
        |오른쪽 어깨|{msg['right_shoulder'].x:.3f}|{msg['right_shoulder'].y:.3f}|{msg['right_shoulder'].z:.3f}|{msg['right_shoulder'].visibility:.2f}|{"적합" if msg['right_shoulder'].visibility > 0.7 else "부적합"}|
        |왼쪽 무릎|{msg['left_knee'].x:.3f}|{msg['left_knee'].y:.3f}|{msg['left_knee'].z:.3f}|{msg['left_knee'].visibility:.2f}|{"적합" if msg['left_knee'].visibility > 0.7 else "부적합"}|
        |오른쪽 무릎|{msg['right_knee'].x:.3f}|{msg['right_knee'].y:.3f}|{msg['right_knee'].z:.3f}|{msg['right_knee'].visibility:.2f}|{"적합" if msg['right_knee'].visibility > 0.7 else "부적합"}|
        """)
    else:
        info_box.info("관절 정보를 기다리는 중입니다...")
