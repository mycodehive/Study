# uv pip install tensorflow==2.15.0

from tensorflow.keras.models import load_model  # 딥러닝 모델 불러오기

def is_fall(left_shoulder, right_shoulder, left_knee, right_knee, prev_avg_shoulder_y):
    current_avg_shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
    avg_knee_y = (left_knee.y + right_knee.y) / 2
    shoulder_drop = 0

    if prev_avg_shoulder_y is not None:
        shoulder_drop = prev_avg_shoulder_y - current_avg_shoulder_y

    print("어깨 하락량:", round(shoulder_drop, 3))

    if shoulder_drop > 0.2 and current_avg_shoulder_y > avg_knee_y:
        print("🔴 낙상 가능성 높음")
        return True
    else:
        print("🟢 정상 자세")
        return False