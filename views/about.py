def render():
    
    import streamlit as st
    
    st.title("About Tennis Career Sim")
        
    st.subheader("How to Play")
    
    st.markdown(
    """
                
    - Hundreds of players are randomly generated, several seasons of tennis are simulated
    - Each week, you can view upcoming tournaments and choose to enter your player in one
    - Or, you can choose to train your player that week to improve their skills
    - Every tournament is simulated match-by-match, tracking 
    
    """
    )
    
    st.write("---")
    
    # Credits
    st.subheader("More Info")
    
    st.markdown(
    """
             
    - Version: **v0.1.0**   
    - Created by: [Peyton Pope](https://peytonjpope.com)
    - Source Code: [tennis-sim](https://github.com/peytonjpope/tennis-sim)
    - Built with: [Streamlit](https://streamlit.io/)
    
    
    """
    )
    
    st.write("---")
    
    # Reset button
    def reset_all():
        # Clear everything
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        # Optional: re-run to apply changes immediately

    st.button("Reset Simulation", type="secondary", on_click=reset_all)
    
    