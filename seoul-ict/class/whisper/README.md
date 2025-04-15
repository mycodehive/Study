# 모델 선택
model_name = st.selectbox("Whisper 모델 선택", ["tiny", "base", "small", "medium", "large"], index=1)
model = whisper.load_model(model_name)

# 녹음 길이 조절
duration = st.slider("⏱️ 변환할 길이 (앞부분 기준, 초)", min_value=5, max_value=60, value=10, step=5)
