import streamlit as st
import modules.requestHandler as RequestHandler


def openExpander(location):
    st.session_state["systemButton"] = location

css='''
        <style>
            section.main > div {max-width:75rem}
        </style>
    '''
st.markdown(css, unsafe_allow_html=True)

hide_img_fs = '''
            <style>
            button[title="View fullscreen"]{
                visibility: hidden;}
            </style>
            '''

st.markdown(hide_img_fs, unsafe_allow_html=True)

st.title("SpaceTraders - v2")
st.container(height=10, border=False)

response = RequestHandler.systems()

systemTab, mapTab = st.tabs(["Systems", "Maps"])

with systemTab:
    if 'systemButton' in st.session_state:
        with st.expander(label=st.session_state["systemButton"]):
            st.text("Test")
    container = st.container()

    with container:
        placeholder = st.empty()
        n_rows = int(1 + len(response["data"]) // 5)
        rows = [st.columns(5) for _ in range(n_rows)]
        cols = [column for row in rows for column in row]
        for col, location in zip(cols, response["data"]):
            with col:
                with st.container(border=True):
                    
                    row1 = st.columns([.65, .35])
                    with row1[0]:
                        st.markdown(f"<h1 style='text-align: left; font-size: 1.5rem'; font-weight: bold >{location["symbol"]}</h1>", unsafe_allow_html=True)
                    with row1[1]:
                        submit = st.button("View", key=location["symbol"] + "1", on_click=openExpander, args=(location["symbol"],))

                    row2 = st.columns([1])
                    with row2[0]:
                        st.divider()

                    row3 = st.columns([1, 1])
                    with row3[0]:
                        st.markdown("<p style='text-align: left;'>Name:</p>", unsafe_allow_html=True) 
                    with row3[1]:
                        if f"{location["symbol"]}Name" in st.session_state: 
                            st.text(st.session_state[f"{location["symbol"]}Name"])
                        else:
                            st.markdown("<p style='text-align: right;'>Unknown</p>", unsafe_allow_html=True) 

                    row4 = st.columns([1, 1])
                    with row4[0]:
                        st.markdown("<p style='text-align: left;'>Type:</p>", unsafe_allow_html=True) 
                    with row4[1]:
                        st.markdown(f"<p style='text-align: right;'>{location["type"].replace("_", " ").title()}</p>", unsafe_allow_html=True) 

                    row5 = st.columns([1, 1])
                    with row5[0]:
                        st.markdown("<p style='text-align: left;'>Position:</p>", unsafe_allow_html=True) 
                    with row5[1]:
                        st.markdown(f"<p style='text-align: right;'>{str(location["x"]) + ", " + str(location["y"])}</p>", unsafe_allow_html=True) 

                    row6 = st.columns([1, 1])
                    with row6[0]:
                        st.markdown("<p style='text-align: left;'>Waypoints:</p>", unsafe_allow_html=True)
                    with row6[1]:
                        st.markdown(f"<p style='text-align: right;'>{len(location["waypoints"])}</p>", unsafe_allow_html=True) 