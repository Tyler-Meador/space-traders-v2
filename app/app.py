import streamlit as st
import modules.login as Login
from modules.menu import menu

st.set_page_config(layout="wide")

if 'agentName' not in st.session_state:
    st.markdown(f"<h1 style='text-align: center; font-size: 3rem'; font-weight: bold >SpaceTraders - v2</h1>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; font-size: 1.5rem'; font-weight: bold >A SpaceTraders.io Interface</h1>", unsafe_allow_html=True)
    st.divider()
    Login.loginSection()
    st.divider()
    menu()

else:

    st.switch_page("pages\\Fleet.py")