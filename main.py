import streamlit as st
import st_pages

st_pages.add_indentation()

st_pages.show_pages(
    [
        st_pages.Page("main.py", "Home"),
        st_pages.Page("pages/agent.py", "Agent"),
        st_pages.Page("pages/galaxy.py", "Galaxy"),
    ]
)

st.title("SpaceTraders - v2")
st.subheader("Welcome to SpaceTraders!")
st.write("Visit [SpaceTraders](https://spacetraders.io) for information on the game!")
st.write("If this is your first time we recommend following the [quickstart](https://docs.spacetraders.io/quickstart/new-game)")
st.write("All SpaceTraders interactions are available within this app. Visit the Agent page to the left to register/login!")