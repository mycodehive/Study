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