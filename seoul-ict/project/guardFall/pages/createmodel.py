import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="모델 생성", layout="wide")

st.title("🧠 모델 생성")
st.write("수집된 데이터를 기반으로 학습 모델을 생성합니다.")

# CSV 파일이 저장된 폴더 경로
csv_dir = os.path.abspath(os.path.join("user", "csv"))

# 폴더 내 CSV 파일 리스트 가져오기
# csv_files = [f for f in os.listdir(csv_dir) if f.endswith(".csv")]
csv_files = [f for f in os.listdir(csv_dir) if f.endswith(".csv") and f != "merged_user_data.csv"]

# 결과 출력
st.write("CSV 파일 목록:")
df_list = []
file_name=""
for file in csv_files:
    file_path = os.path.join(csv_dir, file)
    file_name = (", ".join(csv_files))
    df = pd.read_csv(file_path)  # CSV 파일 읽기
    df_list.append(df)  # 리스트에 추가

st.code(file_name)

# 모든 데이터프레임 합치기
merged_df = pd.concat(df_list, ignore_index=True)

st.write(f"총 {len(csv_files)}개의 CSV 파일을 합쳐서 하나의 데이터로 만들었습니다.")

# 데이터 출력
st.dataframe(merged_df)  # 인터랙티브 테이블 표시

if st.button("🏂 낙상 데이터만 보기"):
    filtered_df = merged_df[merged_df["checkFall"] == 1]  # `checkFall == 1`인 데이터만 필터링
    total_falls = filtered_df.shape[0]  # 데이터 개수 계산
    st.success(f"전체 데이터중 낙상으로 판별된 데이터({total_falls}건)만 보기") 
    st.dataframe(filtered_df)  # 필터링된 데이터 출력

# df to csv로 저장하기
# CSV 파일 경로 설정
csv_path = os.path.join(csv_dir, "merged_user_data.csv")
merged_df.to_csv(csv_path, index=False)

####################################################################
#https://colab.research.google.com/drive/1t1wUuKxdr4HJrycLKXPTZpeihLFfmHfe?usp=sharing#scrollTo=0DsmbprI2Q1c

"""
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
"""

# CSV 불러오기
df = pd.read_csv(os.path.abspath(os.path.join("user", "csv", "merged_user_data.csv")))
st.write(df.head())
st.write(df.info())
#print(df.head())
#print(df.info())