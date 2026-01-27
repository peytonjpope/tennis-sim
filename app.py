import streamlit as st
from datetime import date
from views import career, season, players, setup, about

st.set_page_config(page_title="TenniSim", page_icon="🎾", layout="wide")

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

# Route to setup if no MC, otherwise show navigation
if st.session_state.mc is None:
    setup.render()
else:
    
    st.sidebar.title("TenniSim 🎾")
    
    st.sidebar.write(f"{st.session_state.mc.name}")
    
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "",
        ["**Home**", "**Season**", "**Players**"]
    )
    
    st.sidebar.markdown("---")
    
    show_about = False
    if st.sidebar.button("About", type="secondary", use_container_width=True):
        about.render()
    else:
        if page == "**Home**":
            career.render()
        elif page == "**Season**":
            season.render()
        elif page == "**Players**":
            players.render()
        
    
    # st.sidebar.markdown(" ")
    # st.sidebar.markdown(" ")
    
    # st.sidebar.markdown(" ")
    



    
    # st.sidebar.metric(
    #     label=f"Rank", 
    #     value=f"#{st.session_state.mc.rank}", 
    # )
    
    # st.sidebar.metric(
    #     label=f"Rating", 
    #     value=f"{st.session_state.mc.rating}", 
    # )
    
        