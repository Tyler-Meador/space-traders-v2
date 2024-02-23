import streamlit as st
import st_pages
from modules.login import registerQuickstart
#st_pages.add_indentation()
#
#st_pages.show_pages(
#    [
#        st_pages.Page("main.py", "Home"),
#        st_pages.Page("pages/agent.py", "Agent"),
#        st_pages.Page("pages/galaxy.py", "Galaxy"),
#    ]
#)

st.title("SpaceTraders - v2")
st.subheader("Welcome to SpaceTraders!")
st.write("This app aims to provideseverything you need to know to play SpaceTraders.")
st.write("If you have experience in the game and would like to jump in without any guidance, proceed to the Agent page in your sidebar. From there you will be able to either login if you've used this app before, import an existing agent, or register a new one!")

st.write("If this is your first experience with SpaceTraders, we will walk you through everything below!")

st.divider()

st.write("SpaceTraders is a space-themed economic game with HTTP endpoints for automating gameplay and building custom tools.")
st.write("To get started we will be walking through the quickstart which is available [here!](https://docs.spacetraders.io/quickstart/new-game)")

st.divider()

st.header("Starting The Game")
st.write("The first section of the quickstart shows you the necessary requests in order to register and your view starting location.")
st.write("Since this app has all of the functionality needed, instead of sending the requests manually we will provide you with the UI to do so.")
st.subheader("Register")

token = registerQuickstart()

if token != None:
    st.write("Now that you have registered, you were issued a token! This token represents your Agent's access to the game.")
    with st.expander(label="Token"):
        st.write(token)
    st.write("This app will save your token and you will be able to login with just your Agent name as long as server's haven't reset.")
    st.write("It is always good practice to save that token just incase something were to happen and it is lost.")

