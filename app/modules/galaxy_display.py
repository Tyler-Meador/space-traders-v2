import pandas as pd
import modules.requestHandler as RequestHandler
import streamlit_shadcn_ui as ui
import streamlit as st

def grabSystemTable():
    response = RequestHandler.allSystems()

    systemData = []

    for system in response["data"]:
        systemData.append({
            "Sector": system["sectorSymbol"],
            "System": system["symbol"],
            "Star Type": system["type"],
            "Position": str(system["x"]) + ", " + str(system["y"]),
            "Waypoints": len(system["waypoints"]),
            "Factions": len(system["factions"])
        })
    df = pd.DataFrame(systemData)

    return pd.DataFrame(df)

def grabSystemsMap():
    response = RequestHandler.allSystems()

    mapData = []

    for system in response["data"]:
        mapData.append({
            "x": system["x"],
            "y": system["y"]
        })

    return pd.DataFrame(mapData)


def systemWaypoints(system):
    systemResponse = RequestHandler.specificSystem(system)["data"]

    waypointsData = {}

    if len(systemResponse["waypoints"]) > 0:
        for waypoint in systemResponse["waypoints"]:
            waypointResponse = RequestHandler.waypoint(system, waypoint["symbol"])

            waypointsData[waypointResponse["data"]["symbol"]] = waypointResponse["data"]
    else:
        waypointsData = "No Waypoints Available"
    
    return waypointsData




