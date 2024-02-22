import requests
import streamlit as st


def myShips():
    if "headers" in st.session_state:
        return requests.get("https://api.spacetraders.io/v2/my/ships", headers=st.session_state.headers).json()

def register(json_data):
    return requests.post("https://api.spacetraders.io/v2/register", json_data).json()

def myAgent():
    if "headers" in st.session_state:
        return requests.get("https://api.spacetraders.io/v2/my/agent", headers=st.session_state.headers).json()
    
def myContracts():
    if "headers" in st.session_state:
        return requests.get("https://api.spacetraders.io/v2/my/contracts", headers=st.session_state.headers).json()
    
def acceptContract(contractId):
    if "headers" in st.session_state:
        return requests.post("https://api.spacetraders.io/v2/my/contracts/" + str(contractId) + "/accept", headers=st.session_state.headers).json()

@st.cache_data(ttl=12000)
def systems():
    return requests.get("https://api.spacetraders.io/v2/systems").json()