import requests
import json
import streamlit as st
import time
import modules.pageSwitcher as PageSwitcher

with open("data/users.json") as f:
    user_data = json.load(f)
    f.close()


def loginPage():
    st.title("SpaceTraders - v2")

    tab1, tab2, tab3 = st.tabs(["Login", "Import", "Register"])

    with tab1:
        login()
    with tab2:
        loginImport()
    with tab3:
        register()


def login():
    placeholder = st.empty()

    with placeholder.form("Login"):
        st.markdown("#### Enter Agent Callsign")
        agent = st.text_input("Agent")
        submit = st.form_submit_button("Login")

    if submit and (agent in user_data):
        placeholder.empty()
        alert = st.success("Welcome " + agent)
        time.sleep(3)
        alert.empty()
        PageSwitcher.pageState(0)

    elif submit and (agent not in user_data):
        alert = st.error("Agent: " + agent + " - not found, please register to continue")
        time.sleep(3)
        alert.empty()

    else:
        pass


def register():
    placeholder = st.empty()

    with placeholder.form("Register"):
        st.markdown("#### Register Agent")
        agent = st.text_input("Agent")
        faction = st.selectbox(
            "Select a Faction",
            ('Cosmic', 'Galactic', 'Quantum', 'Dominion', 'Astro', 'Corsairs', 'Void', 'Obsidian', 'Aegis', 'United')
        )
        submit = st.form_submit_button("Register")

    if submit:
        placeholder.empty()
        alert = st.success("Welcome " + agent)
        time.sleep(3)
        alert.empty()
        st.session_state.page = 0
        
    else:
        pass

def loginImport():
    placeholder = st.empty()

    with placeholder.form("Import"):
        st.markdown("#### Import Agent")
        token = st.text_input("Token")
        submit = st.form_submit_button("Import")

    if submit:
        placeholder.empty()
        agent = "Test"
        alert = st.success("Welcome " + agent)
        time.sleep(3)
        alert.empty()
        st.session_state.page = 0
        
    else:
        pass