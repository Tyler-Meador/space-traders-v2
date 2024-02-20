import streamlit as st
import json
import modules.login as Login

if "page" not in st.session_state:
    st.session_state.page = 0

def login(): st.session_state.page = 1
def home(): st.session_state.page = 0

st.sidebar.button(label="Home", on_click=home)
st.sidebar.button(label="Login", on_click=login, type="primary")

placeholder = st.empty()

if st.session_state.page == 0:
    st.title("SpaceTraders - v2")
    st.subheader("Home Page")
elif st.session_state.page == 1:
    Login.login()



