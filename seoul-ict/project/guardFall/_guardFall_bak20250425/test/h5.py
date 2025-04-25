import numpy as np
from tensorflow.keras.models import load_model

# 1. 학습된 모델 로드
model = load_model("fall_model.h5")

# 2. 예측에 사용할 관절 좌표값 (정규화된 값이라고 가정)
# 예: 왼쪽 어깨(x, y), 오른쪽 어깨(x, y), 왼쪽 무릎(x, y), 오른쪽 무릎(x, y)
left_shoulder = (0.45, 0.30)
right_shoulder = (0.55, 0.30)
left_knee = (0.47, 0.70)
right_knee = (0.53, 0.72)

# 3. 입력 데이터 준비 (shape = (1, 8))
input_data = np.array([[
    left_shoulder[0], left_shoulder[1],
    right_shoulder[0], right_shoulder[1],
    left_knee[0], left_knee[1],
    right_knee[0], right_knee[1]
]])

# 4. 모델 예측
prediction = model.predict(input_data)

# 5. 결과 해석
# 예: 이진 분류라면 0 = 정상, 1 = 낙상
result = "낙상 감지됨" if prediction[0][0] > 0.5 else "정상 상태"
print(f"예측 결과: {result} (확률: {prediction[0][0]:.2f})")
