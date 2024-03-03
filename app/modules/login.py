import json
import streamlit as st
import time
import modules.requestHandler as RequestHandler
import modules.dbManager as db
from constants.Constants import DB_CONSTANTS

def login():
    st.container(height=10,border=False)
    placeholder = st.empty()

    with placeholder.form("Login"):
        st.markdown("#### Enter Agent Callsign")
        agent = st.text_input("Agent").upper()
        submit = st.form_submit_button("Login")

    if submit:
        token = db.query(DB_CONSTANTS.READ_TOKEN, [agent], "read")

        if not token:
            alert = st.error("Agent: " + agent + " - not found, please register to continue")
            time.sleep(1)
            alert.empty()
            
        else:
            placeholder.empty()
            alert = st.success("Welcome " + agent)

            st.session_state.headers = {
                "Authorization": "Bearer " + token[0][0]
            }

            st.session_state.agentName = agent 

            time.sleep(3)
            alert.empty()
            st.rerun()


def register():
    st.container(height=10,border=False)
    placeholder = st.empty()

    with placeholder.form("Register"):
        st.markdown("#### Register Agent")
        agent = st.text_input("Agent").upper()
        faction = st.selectbox(
            "Select a Faction",
            ('Cosmic', 'Galactic', 'Quantum', 'Dominion', 'Astro', 'Corsairs', 'Void', 'Obsidian', 'Aegis', 'United')
        )
        submit = st.form_submit_button("Register")

    if submit:
        placeholder.empty()

        json_data = {
            "symbol": agent,
            "faction": faction.upper()
        }

        response = RequestHandler.register(json_data)

        if "error" in response:
            st.write(response)
        else:
            alert = st.success("Welcome " + agent)

            st.session_state.headers = {
                "Authorization": "Bearer " + response["data"]["token"]
            }

            st.session_state.agentName = agent

            dbAgent = [
                    response["data"]['agent']['accountId'], 
                    response["data"]['agent']['symbol'], 
                    response["data"]['agent']['headquarters'],
                    response["data"]['agent']['credits'],
                    response["data"]['agent']['startingFaction'],
                    response["data"]['agent']['shipCount'],
                    response["data"]['token'],
                ]

            db.query(DB_CONSTANTS.INSERT_AGENT,
                    dbAgent, 
                    "write"
                )

            time.sleep(1)
            alert.empty()
            st.rerun()
        
    else:
        pass

def loginImport():
    st.container(height=10,border=False)
    placeholder = st.empty()

    with placeholder.form("Import"):
        st.markdown("#### Import Agent")
        token = st.text_input("Token")
        submit = st.form_submit_button("Import")

    if submit:
        placeholder.empty()

        st.session_state.headers = {
            "Authorization": "Bearer " + token
        }

        response = RequestHandler.myAgent()

        if "error" in response:
            st.write(response)
        else:
            agent = response["data"]["symbol"]

            dbAgent = [
                response["data"]["accountId"],
                response["data"]["symbol"],
                response["data"]["headquarters"],
                response["data"]["credits"],
                response["data"]["startingFaction"],
                response["data"]["shipCount"],
                token
            ]

            db.query(DB_CONSTANTS.INSERT_AGENT, dbAgent, "write")

            alert = st.success("Welcome " + agent )

            st.session_state.agentName = agent

            time.sleep(3)
            alert.empty()
            st.rerun()
        
    else:
        pass


def loginSection():
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        tab1, tab2, tab3 = st.tabs(["Login", "Import", "Register"])

        with tab1:
            login()
        with tab2:
            loginImport()
        with tab3:
            register()