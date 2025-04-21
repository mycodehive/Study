# train_and_save.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# 1. 데이터 로드
df = pd.read_csv("synthetic_pose_data.csv")
X = df.drop("fall", axis=1)
y = df["fall"]

# 2. 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. 스케일링
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 4. 모델 생성
model = Sequential([
    Dense(32, input_shape=(16,), activation='relu'),
    Dense(16, activation='relu'),
    Dense(1, activation='sigmoid')  # 이진 분류
])

model.compile(optimizer=Adam(learning_rate=0.001),
              loss='binary_crossentropy',
              metrics=['accuracy'])

# 5. 학습
model.fit(X_train_scaled, y_train, epochs=30, batch_size=8, validation_split=0.2)

# 6. 평가
loss, accuracy = model.evaluate(X_test_scaled, y_test)
print(f"✅ 테스트 정확도: {accuracy:.4f}")

# 7. 모델 저장
model.save("fall_model.h5")
print("✅ 모델 저장 완료: fall_model.h5")

# 8. 스케일러 저장
joblib.dump(scaler, "scaler.pkl")
print("✅ 스케일러 저장 완료: scaler.pkl")