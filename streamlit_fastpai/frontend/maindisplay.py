import streamlit as st

def show():
    st.success(f"환영합니다, {st.session_state.get('username', '사용자')}님!!! 여기는 maindisplay 파일입니다.🎉")
    if st.button("로그아웃"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.experimental_rerun()
