import requests
import json
import streamlit as st
import time
import requestHandler as RequestHandler
import modules.requestHandler as RequestHandler

def login():
    placeholder = st.empty()

    with open("data/users.json") as f:
        user_data = json.load(f)
        f.close()
    

    with placeholder.form("Login"):
        st.markdown("#### Enter Agent Callsign")
        agent = st.text_input("Agent")
        submit = st.form_submit_button("Login")

    if submit and (agent in user_data):
        placeholder.empty()
        alert = st.success("Welcome " + agent)

        st.session_state.agent = user_data[agent]

        time.sleep(3)
        alert.empty()
        st.rerun()



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

        json_data = {
            "symbol": agent,
            "faction": faction.upper()
        }

        response = RequestHandler.register(json_data)


        if "error" in response:
            st.write(response)
        else:
            alert = st.success("Welcome " + agent)

            newUserData = {
                "data": {
                    "token": response["data"]["token"],
                    "agent": response["data"]["agent"],
                    "contract": response["data"]["contract"]
                }
            }

            st.session_state.agent = newUserData

            writeJson(newUserData, agent)

            time.sleep(3)
            alert.empty()
            st.rerun()
        
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

        response = RequestHandler.myAgent()
        response2 = RequestHandler.myContracts()


        if "error" in response:
            st.write(response)
        else:
            agent = response["data"]["symbol"]
            newUserData = {
                "data": {
                    "token": token,
                    "agent": response["data"],
                    "contract": response2["data"][0]
                }
            }

            alert = st.success("Welcome " + agent )
            st.session_state.agent = newUserData

            writeJson(newUserData, agent)

            time.sleep(3)
            alert.empty()
            st.rerun()
        
    else:
        pass



def writeJson(new_data, agent):
    with open("data/users.json", 'r+') as f:
        file_data = json.load(f)
        file_data[agent] = new_data
        f.seek(0)
        json.dump(file_data, f, indent=4)


def loginSection():
    tab1, tab2, tab3 = st.tabs(["Login", "Import", "Register"])

    with tab1:
        login()
    with tab2:
        loginImport()
    with tab3:
        register()