import streamlit as st


def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.title("SpaceTraders - v2")
    st.sidebar.divider()
    st.sidebar.page_link("pages\\Fleet.py", label="Fleet")



def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.title("SpaceTraders - v2")
    st.sidebar.divider()
    st.sidebar.page_link("app.py", label="Login")


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if "agentName" not in st.session_state or st.session_state.agentName is None:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "agentName" not in st.session_state or st.session_state.agentName is None:
        st.switch_page("pages\\Fleet.py")
    menu()