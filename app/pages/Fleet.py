import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from modules.menu import menu_with_redirect
import modules.topBar as topBar
from modules.requestHandler import myShips, myShipsNoCache
import streamlit_shadcn_ui as ui
from constants.Constants import StyleConstants

menu_with_redirect()


def tableStyleHeader(Symbol, System, Waypoint, Fuel, Cargo):
    with stylable_container(key="fleetHeader", css_styles=StyleConstants.FLEET_HEADER):
        row = st.columns([.12, .35, .38, .6, .23, .21])
        with row[0]: st.write(Symbol)

        with row[2]: st.write(System)

        with row[3]: st.write(Waypoint)

        with row[4]: st.write(Fuel)

        with row[5]: st.write(Cargo)
        

def tableStyleRows(symbol, badges, system, waypoint, fuel, cargo, counter, ship):
    with stylable_container(key="fleetRows", css_styles=StyleConstants.FLEET_ROWS):
        row = st.columns([.21, .25, .33, .17, .11, .25, .2, .2])

        with row[0]:
            selected = ui.button(symbol, key=f"{symbol}FleetButton{str(counter)}", class_name="")
            if selected:
                st.session_state['ship'] = ship
                st.switch_page('pages\\ControlPanel.py')

        with row[1]: ui.badges(badge_list=[(badges[0], "secondary")], class_name="py-1", key=f"badges0{str(counter)}")

        with row[2]: ui.button(system, key=f"{system}SystemButton{str(counter)}")

        with row[3]: ui.button(waypoint, key=f"{waypoint}WaypointButton{str(counter)}")

        with row[4]: ui.badges(badge_list=[(badges[1], "secondary")], class_name="py-1", key=f"badges1{str(counter)}")

        with row[5]: ui.badges(badge_list=[(badges[2], "secondary")], class_name="py-1", key=f"badges2{str(counter)}")

        with row[6]:
            with stylable_container(key="Fuel", css_styles=StyleConstants.MARGIN_TOP_ZERO):
                if fuel[0] > 0:
                    val = (fuel[0] / fuel[1])

                else:
                    val = 0
                    
                st.progress(val, text=f"Fuel: {fuel[0]} / {fuel[1]}")

        with row[7]:
            with stylable_container(key="Cargo", css_styles=StyleConstants.MARGIN_TOP_ZERO):
                if cargo[0] > 0:
                    val = (cargo[0] / cargo[1])

                else:
                    val = 0

                st.progress(val, text=f"Cargo: {cargo[0]} / {cargo[1]}")         
                

def refreshShipData():
    st.session_state['shipData'] = myShipsNoCache()




if 'shipData' not in st.session_state:
    st.session_state['shipData'] = myShips()





st.title("Fleet")
st.divider()

topBar.renderTopBar()

placeholder = st.empty()

with placeholder.container():
    row = st.columns([.9, .1])
    with row[1]: 
        st.button(label="Refresh", key="fleetRefresh", on_click=refreshShipData)

    tableStyleHeader("Symbol", "System", "Waypoint", "Fuel", "Cargo")
        
    counter = 0
    for ship in st.session_state['shipData']["data"]:
        tableStyleRows(
                symbol = ship["symbol"], 
                badges = [ship["frame"]["name"], ship["nav"]["status"].replace("_", " ").lower().title(), ship["nav"]["flightMode"].lower().capitalize()],
                system = ship["nav"]["systemSymbol"], 
                waypoint = ship["nav"]["waypointSymbol"], 
                fuel = [ship["fuel"]["current"], ship["fuel"]["capacity"]],
                cargo = [ship["cargo"]["units"], ship["cargo"]["capacity"]],
                counter = counter,
                ship = ship
            )
        counter = counter + 1


    