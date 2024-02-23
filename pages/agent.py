import streamlit as st
import modules.login as Login
import dateutil.parser
import random
import time
import modules.requestHandler as RequestHandler

agent = None

def renderAgentDetails():
        col1, col2 = st.columns([.3, 1])
        with col1:
            st.text("Agent ID:")
            st.text("Headquarters:")
            st.text("Credits:")
            st.text("Faction:")
        with col2:
            st.text(str(agent["data"]["accountId"]))
            st.text(agent["data"]["headquarters"])
            st.text(agent["data"]["credits"])
            st.text(agent["data"]["startingFaction"])

def renderContract(contract):
        col1, col2, col3, col4 = st.columns([.35, .6, .55, .7])
        accepted = contract["accepted"]

        with col1:
            st.text("Faction:")
            st.text("Type:")
            st.text("Accepted:")


        with col2:
            st.text(contract["factionSymbol"])
            st.text(contract["type"])
            st.text(accepted)

        with col3:
            if not accepted:
                st.text("Deadline To Accept:")

            st.text("Expiration:")
            st.text("Fulfilled:")

        with col4:
            if not accepted:
                st.text(dateutil.parser.parse(contract["deadlineToAccept"]).strftime("%m/%d/%y - %H:%M:%S"))

            st.text(dateutil.parser.parse(contract["expiration"]).strftime("%m/%d/%y - %H:%M:%S"))
            st.text(contract["fulfilled"])

def renderContractTerms(contract):
    col1, col2, col3, col4 = st.columns([1.1, 1.6, 1.4, 1])

    with col1:
        st.text("Deadline:")
        st.text("Required Items:")
        st.text("Units Required:")
        st.text("Units Fulfilled:")

    with col2:
        st.text(dateutil.parser.parse(contract["terms"]["deadline"]).strftime("%m/%d/%y - %H:%M:%S"))
        st.text(contract["terms"]["deliver"][0]["tradeSymbol"])
        st.text(contract["terms"]["deliver"][0]["unitsRequired"])
        st.text(contract["terms"]["deliver"][0]["unitsFulfilled"])

    with col3:
        st.text("Payment On Accept:")
        st.text("Payment On Fulfilled:")
        st.text("Delivery Dest:")

    with col4:
        st.text("$" + str(contract["terms"]["payment"]["onAccepted"]))
        st.text("$" + str(contract["terms"]["payment"]["onFulfilled"]))
        st.text(contract["terms"]["deliver"][0]["destinationSymbol"])

def generateFullDetails(ship):
    st.session_state.shipDetails = ship
    st.switch_page("pages/shipDetails.py") 

def setActive(ship):
    st.session_state.activeShip = ship

def onContractAccept(contractId):
    RequestHandler.acceptContract(contractId)


@st.cache_data(ttl=300)
def getRandom(range):
    return random.choice(range)


if "fullDetails" not in st.session_state:
    st.session_state['fullDetails'] = False

st.title("SpaceTraders - v2")

if 'headers' not in st.session_state:
    Login.loginSection()
else:
    agent = RequestHandler.myAgent()
    agentTab, contractTab, shipsTab, logoutTab = st.tabs(["Agent", "Contract", "Ships", "Logout"])
    
    with agentTab:
        col1, col2, col3 = st.columns([1, .5, 4])
        with col1:
            st.image(open("assets/pilot1.svg").read(), use_column_width="always", caption=str(agent["data"]["symbol"])) 
        with col3:
            renderAgentDetails()

    with contractTab:

        agentContracts = RequestHandler.myContracts()

        if 'error' in agentContracts:
            st.write("No Contracts Available")
        else:
            for contract in agentContracts["data"]:
                with st.container(height=70, border=False):
                    row1 = st.columns([.4, .5, 1, .6])
                    row2 = st.columns([.4, .5, 1, .6])

                    with row2[0]:
                        st.image(open("assets/Contract.svg").read(), use_column_width="never")  
                    with row2[1]:
                        st.container(height=5, border=False)
                        st.text("Contract ID:")
                    with row2[2]:
                        st.container(height=5, border=False)
                        st.text(str(contract["id"]))
                    with row2[3]:
                        butRow1 = st.columns([.6])
                        butRow2 = st.columns([.6])

                        with butRow2[0]:
                            st.button(label="Accept Contract", key="ContractAccept", on_click=onContractAccept, args=(contract["id"],))

                
                st.divider()

                with st.container():
                    renderContract(contract)
                
                container = st.container(border=True)
                container.subheader("Terms")

                with container:
                    renderContractTerms(contract) 
                
                st.divider()

    with shipsTab:
        response = RequestHandler.myShips()

        for ship in response["data"]:
            placeholder = st.empty()

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
                                satAsset = open("assets/satellite.svg").read()
                                st.image(satAsset, use_column_width="always")
                            else:

                                rand = [1,2,3]
                                st.image(open("assets/ship" + str(getRandom(rand)) + ".svg").read(), use_column_width="always")

                    butColLeft, butColRight = st.columns([.7, .8])

                    with butColLeft:
                        st.text("")
                        st.button(label="Set Active", key=ship["symbol"], on_click=setActive, args=(ship,))
                    with butColRight:
                        st.text("")
                        st.session_state.fullDetails = st.button(label="View Full Details", key=(ship["symbol"] + "FullDetails"))

            if st.session_state.fullDetails is not False:
                expander = st.expander(("Ship: " + ship["registration"]["role"] + " - Full Details"))
                expander.write(ship)




    with logoutTab:
        placeholder2 = st.empty()
        with placeholder2.container(border=True):
            row1 = st.columns([2, 1.1, 2])
            row2 = st.columns([1, 2, 1])
            row3 = st.columns([1, 4, 1])
            row4 = st.columns([2, 1, 2])

            with row1[1]:
                st.subheader("Logout")
            with row2[1]:
                st.text("Logging out of Agent: " + st.session_state.agentName)
            with row3[1]:
                st.text("All Data will be saved and available on next login")
            with row4[1]:
                submitted = st.button(label="Logout", key="logout")

        if submitted:
            placeholder2.empty()
            alert = st.success("You have been successfully logged out.")

            time.sleep(3)
            alert.empty()
            del st.session_state["agentName"]
            del st.session_state["headers"]
            st.rerun()







