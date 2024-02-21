import requests
import streamlit as st

@st.cache_data(ttl=600)
def myShips():
    if "headers" in st.session_state:
        return requests.get("https://api.spacetraders.io/v2/my/ships", headers=st.session_state.headers).json()

def register(json_data):
    return requests.post("https://api.spacetraders.io/v2/register", json_data).json()

@st.cache_data(ttl=600)
def myAgent():
    if "headers" in st.session_state:
        return requests.get("https://api.spacetraders.io/v2/my/agent", headers=st.session_state.headers).json()
    
@st.cache_data(ttl=600)
def myContracts():
    if "headers" in st.session_state:
        return requests.get("https://api.spacetraders.io/v2/my/contracts", headers=st.session_state.headers).json()