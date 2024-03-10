import streamlit as st
from modules.menu import menu_with_redirect
from modules.topBar import renderTopBar
import modules.contractHelper as ContractHelper
from streamlit_extras.stylable_container import stylable_container
from constants.Constants import StyleConstants

menu_with_redirect()


st.markdown("""
    <style>
    [role=radiogroup]{
        gap: 5rem;
    }
    </style>
    """,unsafe_allow_html=True)

st.title('Contracts')
st.divider()

renderTopBar()

with stylable_container(key="contractRadios", css_styles="{ border-bottom: 1px solid rgba(49, 51, 63, 0.6); padding-bottom: 35px; }"):
    cols = st.columns([1, 3, 1])
    with cols[1]:
        st.radio(
            "Status:", ["Accepted", "Pending", "Completed", "Expired"], key="contractRadio", horizontal=True, label_visibility="collapsed"
        )


contracts = ContractHelper.getContracts()

if st.session_state['contractRadio'] == 'Accepted':
    st.write('Accepted')

if st.session_state['contractRadio'] == 'Pending':
    ContractHelper.tableStyleHeader()
    ContractHelper.tableStyleRow(contracts[0])

if st.session_state['contractRadio'] == 'Completed':
    st.write('Completed')

if st.session_state['contractRadio'] == 'Expired':
    st.write('Expired')