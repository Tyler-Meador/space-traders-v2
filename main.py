import streamlit as st
from st_pages import show_pages_from_config, hide_pages
import modules.hiddenPages as hiddenPages

hide_pages(hiddenPages.pages)

show_pages_from_config()

st.title("SpaceTraders - v2")