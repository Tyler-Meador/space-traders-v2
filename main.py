import streamlit as st
import json
import modules.login as Login
import modules.pageSwitcher as PageSwitcher

def login(): PageSwitcher.pageState(1)
def home(): PageSwitcher.pageState(0)

st.sidebar.button(label="Home", on_click=home)
st.sidebar.button(label="Login", on_click=login, type="primary")

placeholder = st.empty()

PageSwitcher.grabPage()



