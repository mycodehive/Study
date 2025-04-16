import getcapture as gct
import getposedata as gpd
import msgtelegram as msg
import dbprocess as db
import streamlit as st
import util as ut

# msgtelegram : 메시지 전송 함수
# msg.send_message("낙상 감지됨! 즉시 확인 바랍니다.1")

# dbprocess : DB 전송 함수
# db.insert_fall_event("홍길동1", "2023-10-01 12:00:00", "거실")