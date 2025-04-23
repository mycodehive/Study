import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av
import cv2
import mediapipe as mp
import time
from datetime import datetime
from zoneinfo import ZoneInfo

# 페이지 설정
st.set_page_config(
    page_title="비동기 낙상 감지 시스템",
    layout="wide"
)

# Mediapipe 초기화
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# 현재 시각 (KST)
def now_kst():
    return datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S")

# Pose 추출 클래스
class PoseVideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.pose = mp_pose.Pose()
        self.landmark_data = {}

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        image = frame.to_ndarray(format="bgr24")
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            def extract(p):
                return {"x": p.x, "y": p.y, "z": p.z, "visibility": p.visibility}

            lm = results.pose_landmarks.landmark
            self.landmark_data = {
                "timestamp": now_kst(),
                "left_shoulder": extract(lm[mp_pose.PoseLandmark.LEFT_SHOULDER]),
                "right_shoulder": extract(lm[mp_pose.PoseLandmark.RIGHT_SHOULDER]),
                "left_knee": extract(lm[mp_pose.PoseLandmark.LEFT_KNEE]),
                "right_knee": extract(lm[mp_pose.PoseLandmark.RIGHT_KNEE])
            }

        return av.VideoFrame.from_ndarray(image, format="bgr24")

# UI 구성
st.title("🦴 비동기 실시간 관절 추출 시스템")

col1, col2 = st.columns(2)

# 📷 영상 스트리밍
with col1:
    st.subheader("📷 실시간 카메라 영상")
    webrtc_ctx = webrtc_streamer(
        key="fall-detection",
        video_processor_factory=PoseVideoProcessor,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

# 📋 관절 정보 출력
with col2:
    st.subheader("📋 관절 정보")
    landmark_box = st.empty()

    if webrtc_ctx.video_processor:
        processor = webrtc_ctx.video_processor
        last_print_time = 0

        while True:
            current_time = time.time()
            data = processor.landmark_data

            if data and current_time - last_print_time >= 1:
                def format_joint(joint):
                    return {
                        "X": f"{joint['x']:.2f}",
                        "Y": f"{joint['y']:.2f}",
                        "Z": f"{joint['z']:.2f}",
                        "신뢰도": f"{joint['visibility']:.2f}",
                        "적합": "적합" if joint['visibility'] > 0.7 else "부적합"
                    }

                formatted = {
                    "시간": data["timestamp"],
                    "왼쪽 어깨": format_joint(data["left_shoulder"]),
                    "오른쪽 어깨": format_joint(data["right_shoulder"]),
                    "왼쪽 무릎": format_joint(data["left_knee"]),
                    "오른쪽 무릎": format_joint(data["right_knee"]),
                }

                # 표 형태로 출력
                table_md = f"**🕒 {formatted['시간']}**\n\n"
                table_md += "| 구분 | X | Y | Z | 신뢰도 | 적합 |\n|:--:|:--:|:--:|:--:|:--:|:--:|\n"
                for name, joint in formatted.items():
                    if name == "시간":
                        continue
                    table_md += f"| {name} | {joint['X']} | {joint['Y']} | {joint['Z']} | {joint['신뢰도']} | {joint['적합']} |\n"

                landmark_box.markdown(table_md)
                last_print_time = current_time

            time.sleep(0.03)
