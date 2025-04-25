import streamlit as st

# 페이지 설정
st.set_page_config(page_title="AI 낙상 감지 시스템", layout="wide")

# CSS를 사용하여 사이드바 너비 조정
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            width: 100px !important;  /* 원하는 너비 값 */
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 페이지 UI 구성
st.title("👋 낙상 감지 시스템에 오신 것을 환영합니다")
st.write("""
왼쪽 사이드바 메뉴에서 기능을 선택하세요.

- **영상분석**: 실시간 또는 업로드된 영상을 통해 관절을 분석합니다.  
- **모델생성**: 학습 데이터를 기반으로 모델을 생성합니다.  
- **감시**: 실시간 감시 모드를 실행합니다.
""")