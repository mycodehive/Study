import streamlit as st
import requests
import maindisplay as md

BACKEND = "http://localhost:8000"

def login_page():
    st.subheader("로그인")
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")
    if st.button("로그인"):
        if not login_username or not login_password:
            st.error("아이디와 비밀번호를 입력해주세요.")
        else:
            res = requests.post(f"{BACKEND}/login", json={
                "username": login_username,
                "password": login_password
            })
            if res.status_code == 200:
                st.success(res.json().get("msg"))
                st.session_state["logged_in"] = True
                st.session_state["username"] = login_username
                st.experimental_rerun()
            else:
                st.error(res.json().get("detail"))

def signup_page():
    st.subheader("회원가입")
    signup_username = st.text_input("Username", key="signup_username")
    signup_password = st.text_input("Password", type="password", key="signup_password")
    if st.button("회원가입"):
        if not signup_username or not signup_password:
            st.error("아이디와 비밀번호를 입력해주세요.")
        else:
            res = requests.post(f"{BACKEND}/signup", json={
                "username": signup_username,
                "password": signup_password
            })
            if res.status_code == 200:
                st.success(res.json().get("msg"))
            else:
                st.error(res.json().get("detail"))

def main_page():
    st.success(f"환영합니다, {st.session_state.get('username', '사용자')}님! 🎉")
    if st.button("로그아웃"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.experimental_rerun()
    # --- 여기에 메인 페이지에서 보여줄 추가 기능 구현 ---

def maindisplay():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "username" not in st.session_state:
        st.session_state["username"] = ""

    if st.session_state["logged_in"]:
        #main_page()
        md.show()
    else:
        tab1, tab2 = st.tabs(["로그인", "회원가입"])
        with tab1:
            login_page()
        with tab2:
            signup_page()

if __name__ == "__main__":
    maindisplay()
