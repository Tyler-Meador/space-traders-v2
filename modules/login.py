import requests
import json
import streamlit as st
import time

with open("data/users.json") as f:
    user_data = json.load(f)
    f.close()

def login():
    st.title("SpaceTraders - v2")
    st.subheader("Login")
    
    placeholder = st.empty()

    with placeholder.form("Login"):
        #col1, col2 = st.columns([1, 1])

        st.markdown("#### Enter your credentials")
        agent = st.text_input("Agent")
        submit = st.form_submit_button("Login")

    if submit and (agent in user_data):
        placeholder.empty()
        alert = st.success("Welcome " + agent)
        time.sleep(3)
        alert.empty()

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
        
    else:
        pass
