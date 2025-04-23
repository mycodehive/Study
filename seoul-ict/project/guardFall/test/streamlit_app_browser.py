import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av
import cv2
import mediapipe as mp
import time
from datetime import datetime
from zoneinfo import ZoneInfo

# 설정
st.set_page_config(page_title="낙상 감지 시스템", layout="wide")
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# 시간 함수
def now_kst():
    return datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S")

# 🧠 관절 추출 클래스 (웹캠용)
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
            def extract(p): return {"x": p.x, "y": p.y, "z": p.z, "visibility": p.visibility}
            lm = results.pose_landmarks.landmark
            self.landmark_data = {
                "timestamp": now_kst(),
                "left_shoulder": extract(lm[mp_pose.PoseLandmark.LEFT_SHOULDER]),
                "right_shoulder": extract(lm[mp_pose.PoseLandmark.RIGHT_SHOULDER]),
                "left_knee": extract(lm[mp_pose.PoseLandmark.LEFT_KNEE]),
                "right_knee": extract(lm[mp_pose.PoseLandmark.RIGHT_KNEE])
            }

        return av.VideoFrame.from_ndarray(image, format="bgr24")

# 🧩 선택 메뉴
mode = st.radio("분석 모드를 선택하세요", ["📷 웹캠 스트리밍", "🎞️ MP4 영상 업로드"])

# 📷 웹캠 모드
if mode == "📷 웹캠 스트리밍":
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("실시간 영상")
        webrtc_ctx = webrtc_streamer(
            key="webcam",
            video_processor_factory=PoseVideoProcessor,
            media_stream_constraints={"video": True, "audio": False},
            async_processing=True,
        )

    with col2:
        st.subheader("관절 정보")
        landmark_box = st.empty()

        if webrtc_ctx.video_processor:
            processor = webrtc_ctx.video_processor
            last_print_time = 0
            while True:
                current_time = time.time()
                data = processor.landmark_data

                if data and current_time - last_print_time >= 1:
                    def fmt(j): return {
                        "X": f"{j['x']:.2f}", "Y": f"{j['y']:.2f}",
                        "Z": f"{j['z']:.2f}", "신뢰도": f"{j['visibility']:.2f}",
                        "적합": "적합" if j['visibility'] > 0.7 else "부적합"
                    }
                    formatted = {
                        "시간": data["timestamp"],
                        "왼쪽 어깨": fmt(data["left_shoulder"]),
                        "오른쪽 어깨": fmt(data["right_shoulder"]),
                        "왼쪽 무릎": fmt(data["left_knee"]),
                        "오른쪽 무릎": fmt(data["right_knee"]),
                    }
                    md = f"**🕒 {formatted['시간']}**\n\n| 구분 | X | Y | Z | 신뢰도 | 적합 |\n|:--:|:--:|:--:|:--:|:--:|:--:|\n"
                    for name, joint in formatted.items():
                        if name != "시간":
                            md += f"| {name} | {joint['X']} | {joint['Y']} | {joint['Z']} | {joint['신뢰도']} | {joint['적합']} |\n"
                    landmark_box.markdown(md)
                    last_print_time = current_time

                time.sleep(0.1)

# 🎞️ 영상 업로드 모드
else:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("MP4 영상 업로드")
        video_file = st.file_uploader("MP4 파일을 업로드하세요", type=["mp4"])
        if video_file:
            file_path = f"./mov/uploaded_{video_file.name}"
            with open(file_path, "wb") as f:
                f.write(video_file.read())

            cap = cv2.VideoCapture(file_path)
            frame_placeholder = st.empty()
            pose = mp_pose.Pose()
            stop_button = st.button("⏹ 영상 처리 중지")
            last_print_time = 0

    with col2:
        if video_file:
            landmark_output = st.empty()
            while cap.isOpened() and not stop_button:
                ret, frame = cap.read()
                if not ret:
                    st.success("영상 분석이 완료되었습니다.")
                    break

                image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(image_rgb)

                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                    def extract(p): return {"x": p.x, "y": p.y, "z": p.z, "visibility": p.visibility}
                    lm = results.pose_landmarks.landmark
                    data = {
                        "timestamp": now_kst(),
                        "left_shoulder": extract(lm[mp_pose.PoseLandmark.LEFT_SHOULDER]),
                        "right_shoulder": extract(lm[mp_pose.PoseLandmark.RIGHT_SHOULDER]),
                        "left_knee": extract(lm[mp_pose.PoseLandmark.LEFT_KNEE]),
                        "right_knee": extract(lm[mp_pose.PoseLandmark.RIGHT_KNEE])
                    }

                    current_time = time.time()
                    if current_time - last_print_time >= 1:
                        def fmt(j): return {
                            "X": f"{j['x']:.2f}", "Y": f"{j['y']:.2f}",
                            "Z": f"{j['z']:.2f}", "신뢰도": f"{j['visibility']:.2f}",
                            "적합": "적합" if j['visibility'] > 0.7 else "부적합"
                        }
                        formatted = {
                            "시간": data["timestamp"],
                            "왼쪽 어깨": fmt(data["left_shoulder"]),
                            "오른쪽 어깨": fmt(data["right_shoulder"]),
                            "왼쪽 무릎": fmt(data["left_knee"]),
                            "오른쪽 무릎": fmt(data["right_knee"]),
                        }
                        md = f"**🕒 {formatted['시간']}**\n\n| 구분 | X | Y | Z | 신뢰도 | 적합 |\n|:--:|:--:|:--:|:--:|:--:|:--:|\n"
                        for name, joint in formatted.items():
                            if name != "시간":
                                md += f"| {name} | {joint['X']} | {joint['Y']} | {joint['Z']} | {joint['신뢰도']} | {joint['적합']} |\n"
                        landmark_output.markdown(md)
                        last_print_time = current_time

                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                # Streamlit에 출력
                frame_placeholder.image(frame_bgr, channels="BGR", width=320)

                #frame_placeholder.image(frame_bgr, channels="BGR", use_column_width=True)
                time.sleep(0.03)

            cap.release()
