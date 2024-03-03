import modules.requestHandler as RequestHandler
import modules.dbManager as db
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from constants.Constants import StyleConstants


def getContracts():
    dbRes = db.query("select * from contracts where agent = (?)", [st.session_state['agentName']], 'read')

    if not dbRes:
        response = RequestHandler.myContracts()['data']
        db.insertContracts(response, st.session_state['agentName'])
        getContracts()

    return dbRes

def tableStyleHeader():
    container = stylable_container(key="contractHeader", css_styles=StyleConstants.FLEET_HEADER) 
    with container:
        row = st.columns([.3, .35, .4, .3, .5, .3]) 
        with row[0]: st.write('Faction')

        with row[1]: st.write('Type')

        with row[2]: st.write('Units')

        with row[3]: st.write('Accept By')

        with row[4]: st.write('Expiration')

        with row[5]: st.write('Payment')

    return container