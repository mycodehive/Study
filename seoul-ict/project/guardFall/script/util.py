from datetime import datetime
from zoneinfo import ZoneInfo
import ast

# 현재 시간 가져오기
def now_kst():
    return datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # 초 단위까지 포함

# 변환을 시도하기 전에 데이터 타입 확인
def safe_literal_eval(x):
    if isinstance(x, str):  # 문자열일 때만 변환
        return ast.literal_eval(x)
    return x  # 이미 튜플이면 그대로 반환

# 낙상 여부 판단
def is_fallen(ls_y, rs_y, lk_y, rk_y, ls_ok, rs_ok, lk_ok, rk_ok):
    if sum([ls_ok, rs_ok, lk_ok, rk_ok]) >= 3: # 정상범주 데이터여만 한다.
        count = 0
        if isinstance(ls_y, (int, float)) and ls_y >= 0.55:
            count += 1
        if isinstance(rs_y, (int, float)) and rs_y >= 0.55:
            count += 1
        if isinstance(lk_y, (int, float)) and lk_y >= 0.65:
            count += 1
        if isinstance(rk_y, (int, float)) and rk_y >= 0.65:
            count += 1
        return 1 if count >= 3 else 0 #1이 낙상, 0은 정상, 판별불가
    return 0