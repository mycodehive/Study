import pandas as pd
import numpy as np

# 랜덤 시드 고정
np.random.seed(42)

def generate_sample(fall: bool):
    if fall:
        # 낙상한 경우: 무릎의 y값이 높거나, 좌우 어깨 차이가 큼, 신뢰도가 낮은 경우
        left_shoulder = [np.random.uniform(0.6, 0.8), np.random.uniform(0.8, 1.0), np.random.uniform(-1.0, -0.8), np.random.uniform(0.9, 1.0)]
        right_shoulder = [np.random.uniform(0.2, 0.3), np.random.uniform(0.8, 1.0), np.random.uniform(-0.5, -0.3), np.random.uniform(0.9, 1.0)]
        left_knee = [np.random.uniform(0.6, 0.7), np.random.uniform(2.5, 3.0), np.random.uniform(-0.5, 0.0), np.random.uniform(0.0, 0.2)]
        right_knee = [np.random.uniform(0.3, 0.4), np.random.uniform(2.5, 3.0), np.random.uniform(0.5, 1.0), np.random.uniform(0.0, 0.2)]
    else:
        # 정상 상태
        left_shoulder = [np.random.uniform(0.5, 0.6), np.random.uniform(0.4, 0.5), np.random.uniform(-0.3, -0.2), np.random.uniform(0.9, 1.0)]
        right_shoulder = [np.random.uniform(0.3, 0.4), np.random.uniform(0.4, 0.5), np.random.uniform(-0.3, -0.2), np.random.uniform(0.9, 1.0)]
        left_knee = [np.random.uniform(0.5, 0.6), np.random.uniform(0.8, 1.0), np.random.uniform(0.1, 0.2), np.random.uniform(0.9, 1.0)]
        right_knee = [np.random.uniform(0.3, 0.4), np.random.uniform(0.8, 1.0), np.random.uniform(0.1, 0.2), np.random.uniform(0.9, 1.0)]

    return left_shoulder + right_shoulder + left_knee + right_knee + [int(fall)]

# 100개씩 낙상/정상 데이터 생성
data = [generate_sample(fall=True) for _ in range(10000)] + [generate_sample(fall=False) for _ in range(10000)]
columns = [
    'l_sh_x', 'l_sh_y', 'l_sh_z', 'l_sh_conf',
    'r_sh_x', 'r_sh_y', 'r_sh_z', 'r_sh_conf',
    'l_kn_x', 'l_kn_y', 'l_kn_z', 'l_kn_conf',
    'r_kn_x', 'r_kn_y', 'r_kn_z', 'r_kn_conf',
    'fall'
]

df = pd.DataFrame(data, columns=columns)

# 저장
df.to_csv("synthetic_pose_data.csv", index=False)
print("✅ synthetic_pose_data.csv 파일이 저장되었습니다.")
