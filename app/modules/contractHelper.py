import modules.requestHandler as RequestHandler
import modules.dbManager as db
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from constants.Constants import StyleConstants
from datetime import datetime
from modules.topBar import updateAgent


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
        db.insertContracts(response, st.session_state['agentName'], 'append')
        getContracts()

    return dbRes

def acceptContract(contractId):
    res = RequestHandler.acceptContract(contractId)['data']['contract']
    db.insertContracts(res, st.session_state['agentName'], 'replace')

    updateAgent()
    st.session_state['contractRadio'] = 'Accepted'

def tableStyleHeaderPending():
    container = stylable_container(key="contractHeader", css_styles=StyleConstants.FLEET_HEADER) 
    with container:
        row = st.columns([.3, .3, .3, .45, .4, .3, .01, .12]) 
        with row[0]: st.write('Faction')

        with row[1]: st.write('Type')

        with row[2]: st.write('Units')

        with row[3]: st.write('Accept By')

        with row[4]: st.write('Expiration')

        with row[5]: st.write('Payment (Up Front)')

    return container

def tableStyleHeaderAccepted():
    container = stylable_container(key="contractHeader", css_styles=StyleConstants.FLEET_HEADER) 
    with container:
        row = st.columns([.23, .22, .3, .45, .33]) 
        with row[0]: st.write('Faction')

        with row[1]: st.write('Units')

        with row[2]: st.write('Units Fulfilled')

        with row[3]: st.write('Fulfillment Destination')

        with row[4]: st.write('Deadline')

    return container


def tableStyleRowPending(contract):
    container = stylable_container(key="contractRow", css_styles=StyleConstants.SHIP_INFO) 
    with container:
        row = st.columns([.01, .26, .26, .35, .45, .5, .3, .16])  
        with row[1]: st.write(contract[2])

        with row[2]: st.write(contract[3])
        
        with row[3]: st.write(f'{contract[13]} - {contract[11]}')

        with row[4]: st.write(f'{datetime.fromisoformat(contract[10]).replace(microsecond=0, tzinfo=None)}')

        with row[5]: st.write(f'{datetime.fromisoformat(contract[9]).replace(microsecond=0, tzinfo=None)}')

        with row[6]: st.write(f'{contract[6]:,} ({contract[5]:,})')

        with row[7]: 
            submit = st.button(label="Accept", key='contractAcceptButton', type="primary")

            if submit:
                acceptContract(contract[0])

    return container


def tableStyleRowAccepted(contract):
    container = stylable_container(key="contractRow", css_styles=StyleConstants.SHIP_INFO) 
    with container:
        row = st.columns([.01, .2, .4, .35, .4, .3, .15])  
        with row[1]: st.write(contract[2])

        with row[2]: st.write(f'{contract[13]} - {contract[11]}')

        with row[3]: st.write(f'{contract[14]}')

        with row[4]: st.write(f'{contract[12]}')

        with row[5]: st.write(f'{datetime.fromisoformat(contract[8]).replace(microsecond=0, tzinfo=None)}')

        with row[6]:
            submit = st.button(label="Fulfill", key='fulfillmentButton', type='primary')

    return container