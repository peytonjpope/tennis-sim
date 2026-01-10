import streamlit as st
from datetime import date

st.set_page_config(page_title="Tennis Career Sim", page_icon="🎾", layout="wide")

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.mc = None
    st.session_state.players = []
    st.session_state.all_tournaments = []
    st.session_state.year = date.today().year
    st.session_state.week = 1
    st.session_state.initialized = True
    st.session_state.show_results = False
    st.session_state.week_results = {}

# Route to setup if no MC
if st.session_state.mc is None:
    st.switch_page("pages/_Setup.py")
else:
    st.switch_page("pages/1_Career Home.py")