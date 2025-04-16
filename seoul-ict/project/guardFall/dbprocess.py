import os
import sqlite3
import util as ut
import toml
import streamlit as st

# 1. data 폴더가 없으면 생성
if not os.path.exists("data"):
    os.makedirs("data")

# 2. DB 경로 설정
# 로컬에서 원하는 경로로 지정하는 경우에만 -[------------------
"""
toml_path = os.path.join(ut.exedir("script"), "\\.streamlit\\secrets.toml")

print("exedir: ",ut.exedir("script"))
print("toml_path:", toml_path)

secrets = toml.load(toml_path)
"""
# -]-----------------------------------------------------

db_path = st.secrets['database']['path']

# 3. SQLite 연결
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

if not os.path.exists(db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
if not os.path.isfile(db_path):
    open(db_path, 'w').close()
    # 4. 테이블 생성 (낙상 이벤트 예시)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fall_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_name TEXT,
        fall_time TEXT,
        fall_location TEXT
    )
    """)
    conn.commit()
else:
    print("DB 파일이 이미 존재합니다.")

# 5. CRUD 함수 정의

# Create
def insert_fall_event(name, time, location):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO fall_events (person_name, fall_time, fall_location) VALUES (?, ?, ?)",
                   (name, time, location))
    conn.commit()
    conn.close()

# Read
def get_all_events():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fall_events")
    conn.close()
    return cursor.fetchall()

# Update
def update_event(event_id, name=None, time=None, location=None):
    cursor = conn.cursor()
    if name:
        cursor.execute("UPDATE fall_events SET person_name = ? WHERE id = ?", (name, event_id))
    if time:
        cursor.execute("UPDATE fall_events SET fall_time = ? WHERE id = ?", (time, event_id))
    if location:
        cursor.execute("UPDATE fall_events SET fall_location = ? WHERE id = ?", (location, event_id))
    conn.commit()
    conn.close()

# Delete
def delete_event(event_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM fall_events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()