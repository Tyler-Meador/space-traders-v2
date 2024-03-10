import modules.requestHandler as RequestHandler
import modules.dbManager as db
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from constants.Constants import StyleConstants
from datetime import datetime


def getContracts():

    res = db.query('select accountId from Agent where symbol = (?)', [st.session_state['agentName']], 'read')

    dbRes = db.query("""
        select c.*, cd.tradeSymbol, cd.destinationSymbol, cd.unitsRequired, cd.unitsFulfilled 
        from Contracts c
        join ContractDeliverables cd
        on c.id = cd.contractId
        where agent = (?);
    """, [res[0][0]], 'read')

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

        with row[5]: st.write('Payment (Up Front)')

    return container

def tableStyleRow(contract):
    container = stylable_container(key="contractRow", css_styles=StyleConstants.FLEET_ROWS) 
    with container:
        row = st.columns([.3, .35, .4, .3, .5, .3]) 
        with row[0]: st.write(contract[2])

        with row[1]: st.write(contract[3])

        with row[2]: st.write(f'{contract[13]}')

        with row[3]: st.write(f'{datetime.fromisoformat(contract[10]).replace(microsecond=0, tzinfo=None)}')

        with row[4]: st.write(f'{datetime.fromisoformat(contract[9]).replace(microsecond=0, tzinfo=None)}')

        with row[5]: st.write(f'{contract[6]:,} ({contract[5]:,})')

    return container