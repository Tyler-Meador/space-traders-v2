import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import math
import modules.requestHandler as RequestHandler
import modules.dbManager as db
from constants.Constants import DB_CONSTANTS
from constants.Constants import StyleConstants
import streamlit_shadcn_ui as ui
from datetime import datetime

def calculateDistance(item1, item2):
    return round(math.sqrt((item1['x'] - item2['x'])**2 + (item1['y'] - item2['y'])**2))

def calculateTime(dist, multiplier, engineSpeed):
    return round(round(max(1, dist)) * (multiplier / engineSpeed) + 15)

def getWaypointsInSystem(system):
    res = db.query(DB_CONSTANTS.SELECT_WAYPOINT, [system], "read")
    waypoints = []
    for wp in res:
        waypoints.append(wp)
    return waypoints
        
def getMultiplier(flightMode):
    if flightMode == 'CRUISE':
        return 25
    
    elif flightMode == 'DRIFT':
        return 250
    
    elif flightMode == 'BURN':
        return 12.5
    
    elif flightMode == 'STEALTH':
        return 30
    
def fuelEstimation(dist, flightMode):
    fuel = 0
    if flightMode == 'CRUISE' or flightMode == 'STEALTH':
        fuel = round(dist)

    elif flightMode == 'DRIFT':
        fuel = 1

    elif flightMode == 'BURN':
        fuel = 2 * round(dist)
        if fuel < 2: fuel = 2

    if fuel <= 0: fuel = 1

    return fuel


def grabTraits(system, waypoint):
    data = db.query(DB_CONSTANTS.READ_TRAITS_SHIPYARD_MARKETPLACE, [waypoint], "read")

    if not data:
        traits = RequestHandler.waypoint(system, waypoint) 
        db.insertTraits(traits['data'])

        grabTraits(system, waypoint)

    finalData = [poi[1] for poi in data if (poi[1] == 'Shipyard' or poi[1] == 'Marketplace')]

    return finalData
 
def navButtonSubmit(waypoint):
    data = {
        "waypointSymbol": waypoint
    }
    response = RequestHandler.navToWaypoint(st.session_state['ship']['symbol'], data)

    st.session_state['ship']['nav'] = response['data']['nav']
    st.session_state['ship']['fuel'] = response['data']['fuel']

    departureTime = datetime.fromisoformat(response['data']['nav']['route']['departureTime'])
    arrival = datetime.fromisoformat(response['data']['nav']['route']['arrival'])


    st.session_state['navTimeDifference'] = (arrival - departureTime).total_seconds()

    st.session_state['progressStarted'] = True
    st.session_state['navDisabled'] = True
    

st.cache_data(ttl=300)
def tableStyleRows(waypoint, ship, counter):
    if (waypoint[6] > st.session_state['ship']['fuel']['current']) or (ship['nav']['status'] != 'IN_ORBIT') or (waypoint[0] ==  st.session_state['ship']["nav"]["waypointSymbol"]):
        st.session_state['navDisabled'] = True
    else:
        st.session_state['navDisabled'] = False

    traits = grabTraits(ship["nav"]["systemSymbol"], waypoint[0])
    #print(traits)

    container = stylable_container(key="fleetRows", css_styles=StyleConstants.FLEET_ROWS)
    with container:
        row = st.columns([7, 7, 7, 8, 4, 3, 4, 3])

        with row[0]:
            ui.button(waypoint[0], key=f"{waypoint[0]}navSystemButton{str(counter)}", variant="default", class_name="m-2")
            with row[1]:
                st.text("")
                st.write(f'{waypoint[4]} AUs')

            with row[2]: 
                st.text("")
                st.write(f'{waypoint[5]}s')

        with row[3]:
            st.text("")
            ui.badges(badge_list=[(waypoint[1], "secondary")], class_name="", key=f"{ship["nav"]["systemSymbol"]}{waypoint[1]}Type{str(counter)}")
        
        with row[4]:
            st.text("")
            st.write(str(waypoint[6]))
        
        with row[5]:
            st.text("")
            if 'Shipyard' in traits:
                idx = traits.index('Shipyard')
                ui.badges(badge_list=[(traits[idx], "secondary")], class_name="", key=f"{ship["nav"]["systemSymbol"]}{traits[idx]}badges1{str(counter)}")
#
        with row[6]: 
            st.text("") 
            if 'Marketplace' in traits:
                idx = traits.index('Marketplace')
                ui.badges(badge_list=[(traits[idx], "secondary")], class_name="", key=f"{ship["nav"]["systemSymbol"]}{traits[idx]}badges1{str(counter)}")
        
        with row[7]:
            st.button("GO", key=f"{waypoint[0]}navSubmitButton{str(counter)}", on_click=navButtonSubmit, args=(waypoint[0],), type="primary", disabled = st.session_state['navDisabled'])
                
    return container

def tableStyleHeader(waypoint, dist, time, type, estimatedFuel, Traits):
    container = stylable_container(key="fleetHeader", css_styles=StyleConstants.FLEET_HEADER) 
    with container:
        row = st.columns([.3, .35, .4, .3, .5, .3]) 
        with row[0]: st.write(waypoint)

        with row[1]: st.write(dist)

        with row[2]: st.write(time)

        with row[3]: st.write(type)

        with row[4]: st.write(estimatedFuel)

        with row[5]: st.write(Traits)

    return container