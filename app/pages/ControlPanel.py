import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import streamlit_shadcn_ui as ui
from modules.requestHandler import orbit, dock, flightMode, refuel
import modules.topBar as TopBar
from constants.Constants import StyleConstants
from modules.menu import menu_with_redirect

menu_with_redirect()


def determineModeIndex():
    if st.session_state['ship']['nav']['flightMode'] == 'CRUISE':
        st.session_state['modeIndex'] = 0

    elif st.session_state['ship']['nav']['flightMode'] == 'BURN':
        st.session_state['modeIndex'] = 1

    elif st.session_state['ship']['nav']['flightMode'] == 'DRIFT':
        st.session_state['modeIndex'] = 2

    elif st.session_state['ship']['nav']['flightMode'] == 'STEALTH':
        st.session_state['modeIndex'] = 3


def determineStatusIndex():
    if st.session_state['ship']['nav']['status'] == 'IN_ORBIT':
        st.session_state['statusIndex'] = 0
        st.session_state['statusDisable'] = False
    
    elif st.session_state['ship']['nav']['status'] == 'DOCKED':
        st.session_state['statusIndex'] = 1
        st.session_state['statusDisable'] = False

    else:
        st.session_state['statusIndex'] = None
        st.session_state['statusDisable'] = True


def statusChange():
    if st.session_state['shipStatusModeRadio'] == 'Orbit':
        st.session_state['ship']['nav'] = orbit(st.session_state['ship']['symbol'])['data']['nav']
        st.session_state['statusIndex'] = 0

    elif st.session_state['shipStatusModeRadio'] == 'Dock':
        st.session_state['ship']['nav'] = dock(st.session_state['ship']['symbol'])['data']['nav']
        st.session_state['statusIndex'] = 1


def modeChange():
    if st.session_state['shipFlightModeRadio'] == "Cruise":
        st.session_state['ship']['nav'] = flightMode(st.session_state['ship']['symbol'], flightModeData('CRUISE'))['data']
        st.session_state['modeIndex'] = 0

    elif st.session_state['shipFlightModeRadio'] == "Burn":
        st.session_state['ship']['nav'] = flightMode(st.session_state['ship']['symbol'], flightModeData('BURN'))['data']
        st.session_state['modeIndex'] = 1

    elif st.session_state['shipFlightModeRadio'] == "Drift":
        st.session_state['ship']['nav'] = flightMode(st.session_state['ship']['symbol'], flightModeData('DRIFT'))['data']
        st.session_state['modeIndex'] = 2

    elif st.session_state['shipFlightModeRadio'] == "Stealth":
        st.session_state['ship']['nav'] = flightMode(st.session_state['ship']['symbol'], flightModeData('STEALTH'))['data']
        st.session_state['modeIndex'] = 3
        

def controlPanelChange():
    if st.session_state['controlPanelRadio'] == "Navigate":
        setControlPanel("nav")
        st.session_state['controlPanelIndex'] = 0

    if st.session_state['controlPanelRadio'] == "Mine Resources":
        setControlPanel("mine")
        st.session_state['controlPanelIndex'] = 1

    if st.session_state['controlPanelRadio'] == "Cargo":
        setControlPanel("cargo")
        st.session_state['controlPanelIndex'] = 2

    if st.session_state['controlPanelRadio'] == "Loadout":
        setControlPanel("loadout")
        st.session_state['controlPanelIndex'] = 3


def flightModeData(mode):
    return { "flightMode": mode.upper() }


def setControlPanel(display):
    st.session_state['controlPanelDisplay'] = display

def refuelShip():
    response = refuel(st.session_state['ship']['symbol'])

    st.session_state['ship']['fuel'] = response['data']['fuel']

    TopBar.updateAgent()



determineStatusIndex()
determineModeIndex()

if 'statusDisable' not in st.session_state:
    st.session_state['statusDisable'] = False

if 'controlPanelIndex' not in st.session_state:
    st.session_state['controlPanelIndex'] = None

if 'controlPanelDisplay' not in st.session_state:
    st.session_state['controlPanelDisplay'] = 2

if 'ship' not in st.session_state:
    st.write("No Fleet to Display")
else:
    st.title('Control Panel')
    st.divider()

    TopBar.renderTopBar()

    ### SHIP HEADER

    with stylable_container(key="controlPanelShipHeader", css_styles=StyleConstants.FLEET_HEADER):
        row = st.columns([.2, .2, .5, .07])
        with row[0]:
            st.header(st.session_state['ship']['symbol'])

        with row[1]:
            st.text("")
            st.text("")
            st.write(f"{st.session_state['ship']['frame']['name']} | {st.session_state['ship']['registration']['role']} | {st.session_state['ship']['registration']['factionSymbol']}")

        with row[3]:
            st.text("")
            submit = st.button(label="return", key="returnButton", args=(None, False))
            
            if submit:
                st.switch_page('pages\\Fleet.py')

    ### SYSTEM INFO
    
    with stylable_container(key="controlPanelSystemHeader", css_styles=StyleConstants.CONTROL_PANEL_WAYPOINT_INFO):
        row = st.columns([0.145, 0.5, 0.18, 0.4, 0.8, 0.3])

        with row[0]:
            with stylable_container(key="systemLocations", css_styles=StyleConstants.PADDING_TOP_5):
                st.write("System:")

        with row[1]:
            ui.button(st.session_state['ship']["nav"]["systemSymbol"], key="shipSystemButton", variant="default")

        with row[2]:
            with stylable_container(key="systemLocations", css_styles=""):
                st.write("Waypoint:")

        with row[3]:
            ui.button(st.session_state['ship']["nav"]["waypointSymbol"], key="shipWaypointButton", variant="default")

        with row[4]:
            with stylable_container(key="systemLocations", css_styles=""):
                st.write("Type: Engineered Asteroid")

        with row[5]:
            with stylable_container(key="systemLocations", css_styles=""):
                st.write(f"Position: {st.session_state['ship']['nav']['route']['destination']['x']}, {st.session_state['ship']['nav']['route']['destination']['y']}")

    ### SHIP INFO

    with stylable_container(key="shipInfo", css_styles=StyleConstants.SHIP_INFO):
        row = st.columns([.03, .2, .2, .2, .1, .21, .05])

        with row[1]:
            st.write(f"Status: {st.session_state['ship']["nav"]["status"].replace("_", " ").lower().title()}")
            st.write(f"Flight Mode: {st.session_state['ship']["nav"]["flightMode"].lower().capitalize()}")
            
        with row[5]:
            with stylable_container(key="Fuel", css_styles=StyleConstants.MARGIN_TOP_ZERO):
                if st.session_state['ship']["fuel"]["current"] > 0:
                    val = (st.session_state['ship']["fuel"]["current"] / st.session_state['ship']["fuel"]["capacity"])

                else:
                    val = 0

                st.progress(val, text=f"Fuel: {st.session_state['ship']["fuel"]["current"]} / {st.session_state['ship']["fuel"]["capacity"]}")

        with row[3]:
            with stylable_container(key="Fuel", css_styles=StyleConstants.PADDING_TOP_15):
                if st.session_state['ship']["cargo"]["units"] > 0:
                    val = (st.session_state['ship']["cargo"]["units"] / st.session_state['ship']["cargo"]["capacity"])
                    
                else:
                    val = 0

                st.progress(val, text=f"Cargo: {st.session_state['ship']["cargo"]["units"]} / {st.session_state['ship']["cargo"]["capacity"]}")

        with row[2]:
            st.write(f"Crew: {st.session_state['ship']["crew"]["current"]} / {st.session_state['ship']["crew"]["capacity"]}")
            st.write(f"Morale: {st.session_state['ship']["crew"]["morale"]}")

    ### CONTROL PANEL

    with stylable_container(key="shipControls", css_styles=StyleConstants.SHIP_INFO):
        row = st.columns([0.33, 0.6, 0.7, 0.15])
        
        with row[0]:
            st.radio(
                "Status:", ["Orbit", "Dock"], key="shipStatusModeRadio", horizontal=True, on_change=statusChange, index=st.session_state['statusIndex'], disabled=st.session_state['statusDisable']
            )

        with row[1]:
            st.radio(
                "Flight Mode:", ["Cruise", "Burn", "Drift", "Stealth"], key="shipFlightModeRadio", horizontal=True, on_change=modeChange, index=st.session_state['modeIndex']
            )

        with row[2]:
            st.radio(
                "Display", ["Navigate", "Mine Resources", "Cargo", "Loadout"], key="controlPanelRadio", on_change=controlPanelChange, horizontal=True, index=st.session_state['controlPanelIndex']
            )

        with row[3]:
            with stylable_container(key="controlPanelButtons", css_styles=""):
                if (st.session_state['ship']['fuel']['current'] < st.session_state['ship']['fuel']['capacity']) and st.session_state['ship']['nav']['status'] == 'DOCKED':
                    st.session_state['refuelDisable'] = False

                else:
                    st.session_state['refuelDisable'] = True

                st.button(label="Refuel", key="shipRefuelButton", type="primary", on_click=refuelShip, disabled=st.session_state['refuelDisable'])


    if st.session_state['controlPanelDisplay'] == "nav":
        with stylable_container(key="shipControlDisplay", css_styles=StyleConstants.CONTROL_PANEL_DISPLAY):
            st.text("nav")

    elif st.session_state['controlPanelDisplay'] == "mine":
        with stylable_container(key="shipControlDisplay", css_styles=StyleConstants.CONTROL_PANEL_DISPLAY):
            st.text("mine")

    elif st.session_state['controlPanelDisplay'] == "cargo":
        with stylable_container(key="shipControlDisplay", css_styles=StyleConstants.CONTROL_PANEL_DISPLAY):
            st.text("cargo")

    elif st.session_state['controlPanelDisplay'] == "loadout":
        with stylable_container(key="shipControlDisplay", css_styles=StyleConstants.CONTROL_PANEL_DISPLAY):
            st.text("loadout")