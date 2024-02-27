import streamlit_extras.stylable_container as stylabel_container
import streamlit as st
import modules.requestHandler as RequestHandler

def renderTopBar():
    agent = RequestHandler.myAgent()
    st.session_state['hq'] = agent["data"]["headquarters"]
    st.session_state['faction'] = agent["data"]["startingFaction"]
    st.session_state['shipCount'] = agent["data"]["shipCount"]
    st.session_state['credits'] = agent["data"]["credits"]

    row = st.columns([1, 1, 1, 1, 1])


    with row[0]:
        st.markdown(f"<p style='font-size: 1rem; margin-bottom: 0px; margin-top: 5px;' >Agent: {st.session_state['agentName']}</p>", unsafe_allow_html=True)
    with row[1]:
        st.markdown(f"<p style='font-size: 1rem; margin-bottom: 0px; margin-top: 5px;' >HQ: {st.session_state['hq']}</p>", unsafe_allow_html=True)
    with row[2]:
        st.markdown(f"<p style='font-size: 1rem; margin-bottom: 0; margin-top: 5px;' >Faction: {st.session_state['faction']}</p>", unsafe_allow_html=True)
    with row[3]:
        st.markdown(f"<p style='font-size: 1rem; margin-bottom: 0; margin-top: 5px;' >Ship Count: {st.session_state['shipCount']}</p>", unsafe_allow_html=True)
    with row[4]:
        st.markdown(f"<p style='font-size: 1rem; margin-bottom: 0; margin-top: 5px;' >Credits: {st.session_state['credits']:,}</p>", unsafe_allow_html=True)

    st.divider()