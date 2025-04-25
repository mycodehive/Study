import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av
import cv2
import mediapipe as mp
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from collections import defaultdict

# 세션 상태 초기화 (앱 최상단에 위치)
for key, default in {
    "csv_data": [],
    "csv_ready": False,
    "csv_path": None,
    "downloaded": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = default
        
# 설정
st.set_page_config(page_title="낙상 감지 시스템", layout="wide")
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# 시간 함수
def now_kst():
    return datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # 초 단위까지 포함

# 낙상 여부 판단
def is_fallen(ls_y, rs_y, lk_y, rk_y, ls_ok, rs_ok, lk_ok, rk_ok):
    if sum([ls_ok, rs_ok, lk_ok, rk_ok]) >= 3:
        count = 0
        if isinstance(ls_y, (int, float)) and ls_y >= 0.55:
            count += 1
        if isinstance(rs_y, (int, float)) and rs_y >= 0.55:
            count += 1
        if isinstance(lk_y, (int, float)) and lk_y >= 0.65:
            count += 1
        if isinstance(rk_y, (int, float)) and rk_y >= 0.65:
            count += 1
        return "FALL" if count >= 3 else "-"
    return "-"

# wide format으로 변환
def convert_to_wide_format(data):
    import pandas as pd
    from collections import defaultdict

    grouped = defaultdict(dict)
    for r in data:
        ts   = r["시간"]
        joint = r["관절"]
        grouped[ts][joint] = r

    rows = []
    for ts, joints in grouped.items():
        row = [ts]
        for joint_name in ["왼쪽 어깨", "오른쪽 어깨", "왼쪽 무릎", "오른쪽 무릎"]:
            j = joints.get(joint_name, {})
            row.extend([
                j.get("X", ""), j.get("Y", ""), j.get("Z", ""),
                j.get("신뢰도", ""), j.get("적합", "")
            ])

        # ───── 낙상 여부 계산 ─────
        try:
            ls_y = float(row[2])   # idx 2 = LS_Y
            rs_y = float(row[7])   # idx 7 = RS_Y
            lk_y = float(row[12])  # idx 12 = LK_Y
            rk_y = float(row[17])  # idx 17 = RK_Y

            ls_ok = row[5] == "Y"
            rs_ok = row[10] == "Y"
            lk_ok = row[15] == "Y"
            rk_ok = row[20] == "Y"

            fallen = is_fallen(ls_y, rs_y, lk_y, rk_y, ls_ok, rs_ok, lk_ok, rk_ok)
        except Exception:
            fallen = False

        row.append(fallen)
        rows.append(row)

    columns = [
        "시간",
        "LS_X", "LS_Y", "LS_Z", "LS_신뢰", "LS_적합",
        "RS_X", "RS_Y", "RS_Z", "RS_신뢰", "RS_적합",
        "LK_X", "LK_Y", "LK_Z", "LK_신뢰", "LK_적합",
        "RK_X", "RK_Y", "RK_Z", "RK_신뢰", "RK_적합",
        "낙상여부"
    ]
    return pd.DataFrame(rows, columns=columns)

# 관절 추출 클래스 (웹캠용)
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

# 선택 메뉴
mode = st.radio("분석 모드를 선택하세요", ["📷 웹캠 스트리밍", "🎞️ MP4 영상 업로드"])

# 웹캠 모드
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

                def fmt(j): return {
                    "X": f"{j['x']:.2f}", "Y": f"{j['y']:.2f}",
                    "Z": f"{j['z']:.2f}", "신뢰도": f"{j['visibility']:.2f}",
                    "적합": "Y" if j['visibility'] > 0.7 else "N"
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

# 영상 업로드 모드
else:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("MP4 영상 업로드")
        video_file = st.file_uploader("MP4 파일을 업로드하세요", type=["mp4"])
        if video_file:
            import pandas as pd
            import os
            if "csv_data" not in st.session_state:
                st.session_state.csv_data = []
            if "csv_ready" not in st.session_state:
                st.session_state.csv_ready = False
            if "csv_path" not in st.session_state:
                st.session_state.csv_path = None

            st.session_state.csv_data.clear()

            file_path = f"./mov/{video_file.name}"
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
                    def fmt(j): return {
                        "X": f"{j['x']:.2f}", "Y": f"{j['y']:.2f}",
                        "Z": f"{j['z']:.2f}", "신뢰도": f"{j['visibility']:.2f}",
                        "적합": "Y" if j['visibility'] > 0.7 else "N"
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
                            st.session_state.csv_data.append({
                                "시간": formatted["시간"],
                                "관절": name,
                                "X": joint["X"],
                                "Y": joint["Y"],
                                "Z": joint["Z"],
                                "신뢰도": joint["신뢰도"],
                                "적합": joint["적합"]
                            })
                    landmark_output.markdown(md)
                    last_print_time = current_time

                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                frame_placeholder.image(frame_bgr, channels="BGR", width=320)
                time.sleep(0.03)

            cap.release()
            st.session_state.csv_ready = True

            # 다운로드 버튼 실행 조건 (단 한 번만 실행)
            if st.session_state.csv_ready and st.session_state.csv_data and not st.session_state.downloaded:
                df = convert_to_wide_format(st.session_state.csv_data)
                os.makedirs("./mov/outputs", exist_ok=True)
                #csv_path = f"./outputs/landmarks_{now_kst().replace(':', '-').replace(' ', '_')}.csv"
                base_name = os.path.splitext(video_file.name)[0]  # 확장자 제거
                csv_path = f"./mov/outputs/{base_name}.csv"
                df.to_csv(csv_path, index=False, encoding='utf-8-sig')
                st.session_state.csv_path = csv_path
                csv_bytes = df.to_csv(index=False).encode('utf-8-sig')

                if st.download_button(
                    label="📥 좌표 CSV 다운로드",
                    data=csv_bytes,
                    file_name=os.path.basename(csv_path),
                    mime="text/csv",
                    key="csv_download_button"
                ):
                    st.session_state.downloaded = True
