import streamlit as st
import modules.requestHandler as RequestHandler
import modules.dbManager as db
from constants.Constants import DB_CONSTANTS


def updateAgent():
    agent = RequestHandler.myAgentNoCache()['data']

    db.query(DB_CONSTANTS.UPDATE_AGENT,
                [
                    agent["credits"],
                    agent["shipCount"],
                    agent["accountId"]
                ],
                'write'
             )

def renderTopBar():

    res = db.query(DB_CONSTANTS.READ_AGENT, [st.session_state['agentName']], "read")

    if not res:
        agent = updateAgent()
    else:
        agent = {
            "accountId": res[0][0],
            "symbol": res[0][1],
            "headquarters": res[0][2],
            "credits": res[0][3],
            "startingFaction": res[0][4],
            "shipCount": res[0][5],

        }

    row = st.columns([.35, 1, 1, 1, 1, 1])


    with row[1]:
        st.markdown(f"<p style='font-size: 1rem; margin-bottom: 0px; margin-top: 5px;' >Agent: {st.session_state['agentName']}</p>", unsafe_allow_html=True)
    with row[2]:
        st.markdown(f"<p style='font-size: 1rem; margin-bottom: 0px; margin-top: 5px;' >HQ: {agent["headquarters"]}</p>", unsafe_allow_html=True)
    with row[3]:
        st.markdown(f"<p style='font-size: 1rem; margin-bottom: 0; margin-top: 5px;' >Faction: {agent['startingFaction']}</p>", unsafe_allow_html=True)
    with row[4]:
        st.markdown(f"<p style='font-size: 1rem; margin-bottom: 0; margin-top: 5px;' >Ship Count: {agent['shipCount']}</p>", unsafe_allow_html=True)
    with row[5]:
        st.markdown(f"<p style='font-size: 1rem; margin-bottom: 0; margin-top: 5px;' >Credits: {agent['credits']:,}</p>", unsafe_allow_html=True)

    st.divider()

