import json
import streamlit as st
import time
import modules.requestHandler as RequestHandler

def login():
    st.container(height=10,border=False)
    placeholder = st.empty()

    with open("app/data/users.json") as f:
        stored_users = json.load(f)
        f.close()
    

    with placeholder.form("Login"):
        st.markdown("#### Enter Agent Callsign")
        agent = st.text_input("Agent").upper()
        submit = st.form_submit_button("Login")

    if submit and (agent in stored_users):
        placeholder.empty()
        alert = st.success("Welcome " + agent)

        st.session_state.headers = {
            "Authorization": "Bearer " + stored_users[agent]
        }

        st.session_state.agentName = agent

        time.sleep(3)
        alert.empty()
        st.rerun()

    elif submit and (agent not in stored_users):
        alert = st.error("Agent: " + agent + " - not found, please register to continue")
        time.sleep(3)
        alert.empty()

    else:
        pass


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

            writeJson(response["data"]["token"], agent)

            time.sleep(3)
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

            alert = st.success("Welcome " + agent )

            st.session_state.agentName = agent

            writeJson(token, agent)

            time.sleep(3)
            alert.empty()
            st.rerun()
        
    else:
        pass



def writeJson(new_data,agent):
    with open("app/data/users.json", 'r+') as f:
        file_data = json.load(f)
        file_data[agent] = new_data
        f.seek(0)
        json.dump(file_data, f, indent=4)


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