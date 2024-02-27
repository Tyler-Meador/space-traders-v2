import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from modules.menu import menu_with_redirect
import modules.topBar as topBar
from modules.requestHandler import myShips, myShipsNoCache
import streamlit_shadcn_ui as ui

menu_with_redirect()

def setFleetInfo(state, rerun):
    st.session_state['FleetInfo'] = state

    if rerun:
        st.rerun()

def tableStyleHeader(Symbol, System, Waypoint, Fuel, Cargo):
    with stylable_container(key="fleetHeader", css_styles="""
                {
                    border: 1px solid rgba(49, 51, 63, 0.6);
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px);
                    background-color: #262730
                }
                """):
        row = st.columns([.12, .35, .38, .6, .23, .21])
        with row[0]:
            st.write(Symbol)
        with row[2]:
            st.write(System)
        with row[3]:
            st.write(Waypoint)
        with row[4]:    
            st.write(Fuel)
        with row[5]:
            st.write(Cargo)

def tableStyleRows(symbol, badges, system, waypoint, fuel, cargo, counter, ship):
    with stylable_container(key="fleetRows", css_styles="""
                {
                    border-bottom: 1px solid rgba(49, 51, 63, 0.6);
                }
                """):
        row = st.columns([.17, .25, .33, .17, .1, .25, .2, .2])
        with row[0]:
            openModal = ui.button(symbol, key=f"{symbol}FleetButton{str(counter)}", class_name="")
            if openModal:
                setFleetInfo(ship, True)
        with row[1]:
            ui.badges(badge_list=[(badges[0], "secondary")], class_name="py-1", key=f"badges0{str(counter)}")
        with row[2]:
            ui.button(system, key=f"{system}SystemButton{str(counter)}")
        with row[3]:
            ui.button(waypoint, key=f"{waypoint}WaypointButton{str(counter)}")
        with row[4]:
            ui.badges(badge_list=[(badges[1], "secondary")], class_name="py-1", key=f"badges1{str(counter)}")
        with row[5]:
            ui.badges(badge_list=[(badges[2], "secondary")], class_name="py-1", key=f"badges2{str(counter)}")
        with row[6]:
            with stylable_container(key="Fuel", css_styles="{margin-top: 0px}"):
                if fuel[0] > 0:
                    val = (fuel[0] / fuel[1])
                else:
                    val = 0
                st.progress(val, text=f"Fuel: {fuel[0]} / {fuel[1]}")
        with row[7]:
            with stylable_container(key="Cargo", css_styles="{margin-top: 0px}"):
                if cargo[0] > 0:
                    val = (cargo[0] / cargo[1])
                else:
                    val = 0
                st.progress(val, text=f"Cargo: {cargo[0]} / {cargo[1]}")         

def refreshShipData():
    st.session_state['shipData'] = myShipsNoCache()

if 'FleetInfo' not in st.session_state:
    st.session_state['FleetInfo'] = None

st.title("Fleet")
st.divider()
topBar.renderTopBar()
placeholder = st.empty()


if 'shipData' not in st.session_state:
    st.session_state['shipData'] = myShips()


shipData = st.session_state['shipData']

if st.session_state['FleetInfo'] == None:
    with placeholder.container():
        row = st.columns([.9, .1])
        with row[1]: 
            st.button(label="Refresh", key="fleetRefresh", on_click=refreshShipData)
        tableStyleHeader("Symbol", "System", "Waypoint", "Fuel", "Cargo")
         

        counter = 0
        for ship in shipData["data"]:
            tableStyleRows(
                ship["symbol"], 
                [ship["frame"]["name"], ship["nav"]["status"].lower().capitalize(), ship["nav"]["flightMode"].lower().capitalize()],
                ship["nav"]["systemSymbol"], 
                ship["nav"]["waypointSymbol"], 
                [ship["fuel"]["current"], ship["fuel"]["capacity"]],
                [ship["cargo"]["units"], ship["cargo"]["capacity"]],
                counter,
                ship
                )
            counter = counter + 1
else:
    placeholder.empty()
    if 'FleetInfo' not in st.session_state:
        st.write("No Fleet to Display")
    else:
        with stylable_container(key="shipHeader", css_styles="""
                {
                    border-bottom: 1px solid rgba(49, 51, 63, 0.6);
                    padding-bottom: 5px;
                }
            """):
            row = st.columns([.2, .2, .5, .07])
            with row[0]:
                st.header(st.session_state['FleetInfo']['symbol'])
            with row[1]:
                st.text("")
                st.text("")
                st.write(f"{st.session_state['FleetInfo']['frame']['name']} | {st.session_state['FleetInfo']['registration']['role']} | {st.session_state['FleetInfo']['registration']['factionSymbol']}")
            with row[3]:
                st.text("")
                st.button(label="return", key="returnButton", on_click=setFleetInfo, args=(None, False))

        controlTab, cargoTab, shipBuildTab = st.tabs(["Control Panel", "Cargo", "Configuration"])

        with controlTab:
            with stylable_container(key="locationHeader", css_styles="""
                                        {
                                            border-bottom: 1px solid rgba(49, 51, 63, 0.6);
                                            padding-top: 0px;
                                        }
                                    """):
                row = st.columns([0.145, 0.5, 0.18, 0.4, 0.8, 0.4])
                with row[0]:
                    with stylable_container(key="systemLocations", css_styles="""
                                        {
                                            padding-top: 5px;
                                        }
                                    """):
                        st.write("System:")

                with row[1]:
                    ui.button(st.session_state['FleetInfo']["nav"]["systemSymbol"], key="shipSystemButton", variant="default")

                with row[2]:
                    with stylable_container(key="systemLocations", css_styles="""
                                        {
                                            padding-top: 5px;
                                        }
                                    """):
                        st.write("Waypoint:")

                with row[3]:
                    ui.button(st.session_state['FleetInfo']["nav"]["waypointSymbol"], key="shipWaypointButton", variant="default")

                with row[4]:
                    with stylable_container(key="systemLocations", css_styles="""
                                        {
                                            padding-top: 5px;
                                        }
                                    """):
                        st.write("Type: Engineered Asteroid")

                with row[5]:
                    with stylable_container(key="systemLocations", css_styles="""
                                        {
                                            padding-top: 5px;
                                        }
                                    """):
                        st.write("Position: 0, 0")

            with stylable_container(key="shipHeader", css_styles="""
                            {
                                border-bottom: 1px solid rgba(49, 51, 63, 0.6);
                                padding-bottom: 15px;
                            }
                        """):
                row = st.columns([.05, .3, .15, .2, .15])
                with row[1]:
                    st.write(f"Status: {st.session_state['FleetInfo']["nav"]["status"].lower().capitalize()}")
                    st.write(f"Flight Mode: {st.session_state['FleetInfo']["nav"]["flightMode"].lower().capitalize()}")
                with row[2]:
                    with stylable_container(key="Fuel", css_styles="{margin-top: 0px}"):
                        if st.session_state['FleetInfo']["fuel"]["current"] > 0:
                            val = (st.session_state['FleetInfo']["fuel"]["current"] / st.session_state['FleetInfo']["fuel"]["capacity"])
                        else:
                            val = 0
                        st.progress(val, text=f"Fuel: {st.session_state['FleetInfo']["fuel"]["current"]} / {st.session_state['FleetInfo']["fuel"]["capacity"]}")

                    with stylable_container(key="Fuel", css_styles="{margin-top: 0px}"):
                        if st.session_state['FleetInfo']["cargo"]["units"] > 0:
                            val = (st.session_state['FleetInfo']["cargo"]["units"] / st.session_state['FleetInfo']["cargo"]["capacity"])
                        else:
                            val = 0
                        st.progress(val, text=f"Cargo: {st.session_state['FleetInfo']["cargo"]["units"]} / {st.session_state['FleetInfo']["cargo"]["capacity"]}")
                with row[4]:
                    st.write(f"Crew: {st.session_state['FleetInfo']["crew"]["current"]} / {st.session_state['FleetInfo']["crew"]["capacity"]}")
                    st.write(f"Morale: {st.session_state['FleetInfo']["crew"]["morale"]}")

            with stylable_container(key="shipControls", css_styles="""
                            {
                                border-bottom: 1px solid rgba(49, 51, 63, 0.6);
                                padding-bottom: 015px;
                            }
                        """):
                row = st.columns([0.4, 0.9, 0.3, 0.4, 0.4])
                with row[0]:
                    st.radio(
                        "Status:", ["Orbit", "Dock"], key="shipStatusRadio", horizontal=True
                    )
                with row[1]:
                    st.radio(
                        "Flight Mode:", ["Cruise", "Burn", "Drift", "Stealth"], key="shipFlightModeRadio", horizontal=True
                    )
                with row[2]:
                    with stylable_container(key="navbuttoncontainer", css_styles="""
                            {
                                padding-top: 5px;
                            }
                        """):
                        st.button(label="Navigate", key="shipNavButton", type="primary", disabled=False)
                with row[3]:
                    with stylable_container(key="navbuttoncontainer", css_styles="""
                            {
                                padding-top: 5px;
                            }
                        """):
                        st.button(label="Mine Resources", key="shipMineButton", type="primary", disabled=False)
                with row[4]:
                    with stylable_container(key="navbuttoncontainer", css_styles="""
                            {
                                padding-top: 5px;
                            }
                        """):
                        st.button(label="Refuel", key="shipRefuelButton", type="primary", disabled=False)
            
            


    