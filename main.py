import streamlit as st
import st_pages

st_pages.show_pages(
    [
        st_pages.Page("pages/agent.py", "Agent"),
        st_pages.Page("main.py", "Home")
    ]
)

st.title("SpaceTraders - v2")