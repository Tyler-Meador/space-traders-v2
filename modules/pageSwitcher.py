import streamlit as st
import modules.login as Login

if "page" not in st.session_state:
    st.session_state.page = 0

def pageState(state):
    st.session_state.page = state

def getSessionState():
    return st.session_state.page

def grabPage():
    if st.session_state.page == 0:
        st.title("SpaceTraders - v2")
        st.subheader("Home Page")
    elif st.session_state.page == 1:
        Login.loginPage()