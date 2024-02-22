import streamlit as st
import modules.requestHandler as RequestHandler


st.title("SpaceTraders - v2")

response = RequestHandler.systems()

for system in response["data"]:
    placeholder = st.empty()

    container = placeholder.container(border=True)

    with container:
        st.subheader(system["symbol"])
        st.divider()

        
        if len(system["waypoints"]) > 0:
            n_rows = int(1 + len(system["waypoints"]) // 6)
            rows = [st.columns(6) for _ in range(n_rows)]
            cols = [column for row in rows for column in row]
            
            for col, waypoint in zip(cols, system["waypoints"]):
                if waypoint["type"] == "PLANET": 
                    col.image(open("assets/planet1.svg").read(), use_column_width="always", caption=waypoint["symbol"])
                elif waypoint["type"] == "ASTEROID":
                    col.image(open("assets/asteroid2.svg").read(), use_column_width="always", caption=waypoint["symbol"])
                elif waypoint["type"] == "GAS_GIANT":
                    col.image(open("assets/gas_giant.svg").read(), use_column_width="always", caption=waypoint["symbol"])
                elif waypoint["type"] == "MOON":
                    col.image(open("assets/moon.svg").read(), use_column_width="always", caption=waypoint["symbol"])
        else:
            st.text("No Waypoints Found")