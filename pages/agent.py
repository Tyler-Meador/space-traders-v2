import streamlit as st
import modules.login as Login
import dateutil.parser
import requests
import random
from streamlit_modal import Modal

agent = None


def renderAgentDetails():
        col1, col2 = st.columns([.3, 1])
        with col1:
            st.text("Agent ID:")
            st.text("Headquarters:")
            st.text("Credits:")
            st.text("Faction:")
        with col2:
            st.text(str(agent["data"]["agent"]["accountId"]))
            st.text(agent["data"]["agent"]["headquarters"])
            st.text(agent["data"]["agent"]["credits"])
            st.text(agent["data"]["agent"]["startingFaction"])

def renderContract():
        col1, col2, col3, col4 = st.columns([.35, .6, .55, .7])
        accepted = agent["data"]["contract"]["accepted"]

        with col1:
            st.text("Faction:")
            st.text("Type:")
            st.text("Accepted:")


        with col2:
            st.text(agent["data"]["contract"]["factionSymbol"])
            st.text(agent["data"]["contract"]["type"])
            st.text(accepted)

        with col3:
            if not accepted:
                st.text("Deadline To Accept:")

            st.text("Expiration:")
            st.text("Fulfilled:")

        with col4:
            if not accepted:
                st.text(dateutil.parser.parse(agent["data"]["contract"]["deadlineToAccept"]).strftime("%m/%d/%y - %H:%M:%S"))

            st.text(dateutil.parser.parse(agent["data"]["contract"]["expiration"]).strftime("%m/%d/%y - %H:%M:%S"))
            st.text(agent["data"]["contract"]["fulfilled"])

def renderContractTerms():
    col1, col2, col3, col4 = st.columns([1.1, 1.6, 1.4, 1])

    with col1:
        st.text("Deadline:")
        st.text("Required Items:")
        st.text("Units Required:")
        st.text("Units Fulfilled:")

    with col2:
        st.text(dateutil.parser.parse(agent["data"]["contract"]["terms"]["deadline"]).strftime("%m/%d/%y - %H:%M:%S"))
        st.text(agent["data"]["contract"]["terms"]["deliver"][0]["tradeSymbol"])
        st.text(agent["data"]["contract"]["terms"]["deliver"][0]["unitsRequired"])
        st.text(agent["data"]["contract"]["terms"]["deliver"][0]["unitsFulfilled"])

    with col3:
        st.text("Payment On Accept:")
        st.text("Payment On Fulfilled:")
        st.text("Delivery Dest:")

    with col4:
        st.text("$" + str(agent["data"]["contract"]["terms"]["payment"]["onAccepted"]))
        st.text("$" + str(agent["data"]["contract"]["terms"]["payment"]["onFulfilled"]))
        st.text(agent["data"]["contract"]["terms"]["deliver"][0]["destinationSymbol"])

def generateFullDetails(ship):
    st.session_state.shipDetails = ship
    st.switch_page("pages/shipDetails.py") 

def setActive(ship):
    st.session_state.activeShip = ship

st.title("SpaceTraders - v2")

if 'agent' not in st.session_state:
    Login.loginSection()
else:
    agent = st.session_state.agent
    tab1, tab2, tab3 = st.tabs(["Agent", "Contract", "Ships"])
    
    with tab1:
        col1, col2, col3 = st.columns([1, .5, 4])
        with col1:
            st.image(open("assets/pilot1.svg").read(), use_column_width="always", caption=str(agent["data"]["agent"]["symbol"]).lower().capitalize()) 
        with col3:
            renderAgentDetails()

    with tab2:
        with st.container(height=50, border=False):
            col1, col2, col3 = st.columns([.4, .5, 2])
            with col1:
                st.image(open("assets/Contract.svg").read(), use_column_width="never")  
            with col2:
                st.container(height=5, border=False)
                st.text("Contract ID:")
            with col3:
                st.container(height=5, border=False)
                st.text(str(agent["data"]["contract"]["id"]))
        
        st.divider()
 
        with st.container():
            renderContract()
        
        container = st.container(border=True)
        container.subheader("Terms")

        with container:
            renderContractTerms()

    with tab3:
        headers = {
            "Authorization": "Bearer " + agent["data"]["token"]
        }
        response = requests.get("https://api.spacetraders.io/v2/my/ships", headers=headers).json()

        for ship in response["data"]:

            container = st.container(border=True)
                 
            with container:
                conCol1, conCol2, conCol3 = st.columns([1, 1, 1.5])

                with conCol1:
                    st.text("Symbol:")
                    st.text("Role:")
                    st.text("Waypoint:")
                    st.text("Status:")
                    st.text("Flight Mode:")
                    st.text("Fuel Capacity:")
                    st.text("Fuel Current:")
                    st.text("Cargo Capacity:")
                    st.text("Current Cargo Units:")

                with conCol2:
                    st.text(ship["symbol"])
                    st.text(ship["registration"]["role"])
                    st.text(ship["nav"]["waypointSymbol"])
                    st.text(ship["nav"]["status"])
                    st.text(ship["nav"]["flightMode"])
                    st.text(ship["fuel"]["capacity"])
                    st.text(ship["fuel"]["current"])
                    st.text(ship["cargo"]["capacity"])
                    st.text(ship["cargo"]["units"])

                with conCol3:
                    shipImageContainer = st.container(height=250, border=True)

                    with shipImageContainer:
                        row1 = st.columns([.5, 3 , .5])
                        row2 = st.columns([.5, 3 , .5])
                        row3 = st.columns([.5, 3 , .5])

                        with row2[1]:
                            if ship["registration"]["role"] == "SATELLITE":
                                st.image(open("assets/satellite.svg").read(), use_column_width="always")
                            else:
                                rand = random.choice([1,2,3])
                                st.image(open("assets/ship" + str(rand) + ".svg").read(), use_column_width="always")

                    butColLeft, butColCenter, butColRight = st.columns([.6, 1, .3])

                    with butColCenter:
                        st.text("")

                        st.button(label="Set Active", key=ship["symbol"], on_click=setActive, args=(ship,))



