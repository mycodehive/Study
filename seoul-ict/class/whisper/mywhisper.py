# pip install streamlit
# pip install openai-whisper
# pip install sounddevice
# pip install wavio

import streamlit as st
import whisper
import sounddevice as sd
import wavio
import os
import time

# 현재 실행 중인 파이썬 파일 경로
file_path = os.path.abspath(__file__)
dir_path = os.path.dirname(file_path)

# Whisper 모델 로드
# model = whisper.load_model("base")

# 오디오 녹음 설정
duration = 20  # 초
fs = 44100  # 샘플 레이트

# 파일 경로
audio_file = os.path.join(dir_path, "recording.mp3")

# 오디오를 녹음하는 함수
def record_audio(duration, fs, file_path):
    st.info("녹음 중...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)

    # 녹음 진행 상황을 표시
    progress_bar = st.progress(0)
    for i in range(duration):
        time.sleep(1)
        progress_bar.progress((i + 1) / duration)
    
    sd.wait()  # 녹음이 끝날 때까지 대기
    wavio.write(file_path, recording, fs, sampwidth=2)
    st.success("녹음 완료!")

# Whisper를 사용하여 오디오를 문자로 변환하는 함수
def transcribe_audio(file_path):
    st.info("변환 중...")
    result = model.transcribe(file_path)
    st.success("변환 완료!")
    return result["text"]

# Streamlit 인터페이스
st.title("음성 인식 및 번역 앱")

# 1. 모델 선택
model_name = st.selectbox("Whisper 모델 선택", ["tiny", "base", "small", "medium", "large"], index=1)
model = whisper.load_model(model_name)

duration = st.slider("⏱️ 변환할 길이 (앞부분 기준, 초)", min_value=5, max_value=60, value=10, step=5)

if st.button("녹음 시작"):
    record_audio(duration, fs, audio_file)

if os.path.exists(audio_file):
    st.audio(audio_file, format='audio/mp3')

    if st.button("오디오 번역"):
        transcription = transcribe_audio(audio_file)
        st.text_area("번역 결과", transcription)