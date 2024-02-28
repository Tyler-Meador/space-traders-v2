import streamlit as st
import modules.requestHandler as RequestHandler


def renderTopBar():
    st.session_state['agent'] = RequestHandler.myAgentNoCache()['data']
    st.session_state['reloadTopBar'] = False

    row = st.columns([.35, 1, 1, 1, 1, 1])


    with row[1]:
        st.markdown(f"<p style='font-size: 1rem; margin-bottom: 0px; margin-top: 5px;' >Agent: {st.session_state['agentName']}</p>", unsafe_allow_html=True)
    with row[2]:
        st.markdown(f"<p style='font-size: 1rem; margin-bottom: 0px; margin-top: 5px;' >HQ: {st.session_state['agent']["headquarters"]}</p>", unsafe_allow_html=True)
    with row[3]:
        st.markdown(f"<p style='font-size: 1rem; margin-bottom: 0; margin-top: 5px;' >Faction: {st.session_state['agent']['startingFaction']}</p>", unsafe_allow_html=True)
    with row[4]:
        st.markdown(f"<p style='font-size: 1rem; margin-bottom: 0; margin-top: 5px;' >Ship Count: {st.session_state['agent']['shipCount']}</p>", unsafe_allow_html=True)
    with row[5]:
        st.markdown(f"<p style='font-size: 1rem; margin-bottom: 0; margin-top: 5px;' >Credits: {st.session_state['agent']['credits']:,}</p>", unsafe_allow_html=True)

    st.divider()

