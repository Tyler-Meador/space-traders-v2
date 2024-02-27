import requests
import streamlit as st

@st.cache_data(ttl=12000)
def myShips():
    if "headers" in st.session_state:
        return requests.get("https://api.spacetraders.io/v2/my/ships", headers=st.session_state.headers).json()
    
def myShipsNoCache():
    if "headers" in st.session_state:
        return requests.get("https://api.spacetraders.io/v2/my/ships", headers=st.session_state.headers).json()

def register(json_data):
    return requests.post("https://api.spacetraders.io/v2/register", json_data).json()

@st.cache_data(ttl=12000)
def myAgent():
    if "headers" in st.session_state:
        return requests.get("https://api.spacetraders.io/v2/my/agent", headers=st.session_state.headers).json()
    
def myContracts():
    if "headers" in st.session_state:
        return requests.get("https://api.spacetraders.io/v2/my/contracts", headers=st.session_state.headers).json()
    
def acceptContract(contractId):
    if "headers" in st.session_state:
        return requests.post("https://api.spacetraders.io/v2/my/contracts/" + str(contractId) + "/accept", headers=st.session_state.headers).json()

@st.cache_data(ttl=12000)
def allSystems():
    return requests.get("https://api.spacetraders.io/v2/systems").json()

@st.cache_data(ttl=300)
def specificSystem(system):
    return requests.get(f"https://api.spacetraders.io/v2/systems/{system}").json()

@st.cache_data(ttl=300)
def waypoint(system, waypoint):
    return requests.get(f"https://api.spacetraders.io/v2/systems/{system}/waypoints/{waypoint}").json()

@st.cache_data(ttl=600)
def viewShipyard(system, waypoint):
    return requests.get(f"https://api.spacetraders.io/v2/systems/{system}/waypoints/{waypoint}/shipyard", headers=st.session_state.headers).json()

def viewMarket(system, waypoint):
    return requests.get(f"https://api.spacetraders.io/v2/systems/{system}/waypoints/{waypoint}/market", headers=st.session_state.headers).json()

def viewJumpGate(system, waypoint):
    return requests.get(f"https://api.spacetraders.io/v2/systems/{system}/waypoints/{waypoint}/jump-gate", headers=st.session_state.headers).json()

def viewConstruction(system, waypoint):
    return requests.get(f"https://api.spacetraders.io/v2/systems/{system}/waypoints/{waypoint}/construction", headers=st.session_state.headers).json()

def supplyConstruction(system, waypoint, supply):
    return requests.get(f"https://api.spacetraders.io/v2/systems/{system}/waypoints/{waypoint}/construction/supply", data=supply, headers=st.session_state.headers).json()

def orbit(ship):
    return requests.post(f"https://api.spacetraders.io/v2/my/ships/{ship}/orbit", headers=st.session_state.headers).json()

def dock(ship):
    return requests.post(f"https://api.spacetraders.io/v2/my/ships/{ship}/dock", headers=st.session_state.headers).json()

def flightMode(ship, mode):
    return requests.patch(f"https://api.spacetraders.io/v2/my/ships/{ship}/nav", data=mode, headers=st.session_state.headers).json()

def navToWaypoint(ship, navDetails):
    return requests.post(f"https://api.spacetraders.io/v2/my/ships/{ship}/navigate", data=navDetails, headers=st.session_state.headers).json()

def warp(ship, warpData):
    return requests.post(f"https://api.spacetraders.io/v2/my/ships/{ship}/warp", data=warpData, headers=st.session_state.headers).json()

def jump(ship, jumpData):
    return requests.post(f"https://api.spacetraders.io/v2/my/ships/{ship}/jump", data=jumpData, headers=st.session_state.headers).json()

def extract(ship):
    return requests.post(f"https://api.spacetraders.io/v2/my/ships/{ship}/extract", headers=st.session_state.headers).json()

def survey(ship):
    return requests.post(f"https://api.spacetraders.io/v2/my/ships/{ship}/survey", headers=st.session_state.headers).json()

def extractFromSurvey(ship, survey):
    return requests.post(f"https://api.spacetraders.io/v2/my/ships/{ship}/extract", data=survey, headers=st.session_state.headers).json()

def refuel(ship):
    return requests.post(f"https://api.spacetraders.io/v2/my/ships/{ship}/refuel", headers=st.session_state.headers).json()

def cargo(ship):
    return requests.get(f"https://api.spacetraders.io/v2/my/ships/{ship}/cargo", headers=st.session_state.headers).json()

def sellCargo(ship, sellData):
    return requests.post(f"https://api.spacetraders.io/v2/my/ships/{ship}/sell", data=sellData, headers=st.session_state.headers).json()

def deliver(contractId, delivery):
    return requests.post(f"https://api.spacetraders.io/v2/my/contracts/{contractId}/deliver", data=delivery, headers=st.session_state.headers).json()

def fulfill(contractId):
    return requests.post(f"https://api.spacetraders.io/v2/my/contracts/{contractId}/fulfill", headers=st.session_state.headers).json()

def refine(ship, material):
    return requests.post(f"https://api.spacetraders.io/v2/my/ships/{ship}/refine", data=material, headers=st.session_state.headers).json()

def chart(ship):
    return requests.post(f"https://api.spacetraders.io/v2/my/ships/{ship}/chart", headers=st.session_state.headers).json()

def siphon(ship):
    return requests.post(f"https://api.spacetraders.io/v2/my/ships/{ship}/chart", headers=st.session_state.headers).json()

def jettison(ship, cargo):
    return requests.post(f"https://api.spacetraders.io/v2/my/ships/{ship}/jettison", data=cargo, headers=st.session_state.headers).json()

def scanSystems(ship):
    return requests.post(f"https://api.spacetraders.io/v2/my/ships/{ship}/scan/systems", headers=st.session_state.headers).json()

def scanWaypoints(ship):
    return requests.post(f"https://api.spacetraders.io/v2/my/ships/{ship}/scan/waypoints", headers=st.session_state.headers).json()

def scanShips(ship):
    return requests.post(f"https://api.spacetraders.io/v2/my/ships/{ship}/scan/ships", headers=st.session_state.headers).json()

def purchase(ship, purchaseItem):
    return requests.post(f"https://api.spacetraders.io/v2/my/ships/{ship}/purchase", data=purchaseItem, headers=st.session_state.headers).json()

def transferCargo(ship, cargo):
    return requests.post(f"https://api.spacetraders.io/v2/my/ships/{ship}/transfer", data=cargo, headers=st.session_state.headers).json()

def negotiateContract(ship):
    return requests.post(f"https://api.spacetraders.io/v2/my/ships/{ship}/negotiate/contract", headers=st.session_state.headers).json()

def getMounts(ship):
    return requests.get(f"https://api.spacetraders.io/v2/my/ships/{ship}/mounts", headers=st.session_state.headers).json()

def installMount(ship, mount):
    return requests.post(f"https://api.spacetraders.io/v2/my/ships/{ship}/mounts/install", data=mount, headers=st.session_state.headers).json()

def removeMount(ship, mount):
    return requests.post(f"https://api.spacetraders.io/v2/my/ships/{ship}/mounts/remove", data=mount, headers=st.session_state.headers).json()