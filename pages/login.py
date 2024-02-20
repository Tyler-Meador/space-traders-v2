import requests
import json
import streamlit as st
import time
from streamlit_extras.switch_page_button import switch_page
from st_pages import hide_pages, show_pages
import modules.hiddenPages as hiddenPages

hide_pages(hiddenPages.pages)

with open("data/users.json") as f:
    user_data = json.load(f)
    f.close()


def updatePage():
    hiddenPages.removePage("Agent")
    hiddenPages.addPage("Login")

    switch_page("Agent")

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

        updatePage()



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

        response = requests.post("https://api.spacetraders.io/v2/register", json_data).json()


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


            writeJson(newUserData, agent)

            time.sleep(3)
            alert.empty()

            updatePage()
        
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

        headers = {
            "Authorization": "Bearer " + token
        }

        response = requests.get("https://api.spacetraders.io/v2/my/agent", headers=headers).json()
        response2 = requests.get("https://api.spacetraders.io/v2/my/contracts", headers=headers).json()


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

            writeJson(newUserData, agent)

            time.sleep(3)
            alert.empty()

            updatePage()
        
    else:
        pass



def writeJson(new_data, agent):
    with open("data/users.json", 'r+') as f:
        file_data = json.load(f)
        file_data[agent] = new_data
        f.seek(0)
        json.dump(file_data, f, indent=4)


st.title("SpaceTraders - v2")

tab1, tab2, tab3 = st.tabs(["Login", "Import", "Register"])

with tab1:
    login()
with tab2:
    loginImport()
with tab3:
    register()