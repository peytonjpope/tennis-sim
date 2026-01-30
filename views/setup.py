def render():

    import streamlit as st
    import random
    import json
    from player import Player
    from tournament import Tournament
    from main import generate_random_player, simulate_tournament, update_rankings, get_tournaments_for_week, sim_week_tournaments, year_end_changes
    from datetime import date

    if st.session_state.mc is not None:
        st.switch_page("app.py")

    st.title("Welcome to TenniSim!")
    
    st.subheader("Create your player to get started.")

    with st.form("create_player"):
        type_options = ["**Grass** - Serve, Volley, and Slice", 
                        "**Clay**  - Groundstrokes and Endurance", 
                        "**Hard**  - Balanced Skills, Strong Mental Game"]
        
        name = st.text_input("Name (ex. R. Nadal)")
        country = st.text_input("Country (3-letter code)").upper()
        player_type = st.radio("Playing Style", type_options, index=2)
        
        submit = st.form_submit_button("Create Player")
        
        if submit and name and len(country) == 3:        
            if player_type == type_options[0]:  # Grass
                # Create MC
                mc = Player(name, country, "Grass")
                
                mc.serve = random.randint(58, 68)
                mc.forehand = random.randint(48, 60)
                mc.backhand = random.randint(48, 60)
                mc.slice = random.randint(50, 62)
                mc.volley = random.randint(56, 66)
                mc.clutch = random.randint(50, 62)
                mc.endurance = random.randint(48, 60)
            elif player_type == type_options[1]:  # Clay
                # Create MC
                mc = Player(name, country, "Clay")
                
                mc.serve = random.randint(48, 60)
                mc.forehand = random.randint(58, 68)
                mc.backhand = random.randint(58, 68)
                mc.slice = random.randint(50, 62)
                mc.volley = random.randint(45, 58)
                mc.clutch = random.randint(50, 62)
                mc.endurance = random.randint(58, 68)
            else:  # Hard
                # Create MC
                mc = Player(name, country, "Hard")
                
                mc.serve = random.randint(52, 62)
                mc.forehand = random.randint(52, 62)
                mc.backhand = random.randint(52, 62)
                mc.slice = random.randint(50, 60)
                mc.volley = random.randint(50, 60)
                mc.clutch = random.randint(54, 64)
                mc.endurance = random.randint(54, 64)
            
            mc.update_rating()
            mc.main_character = True
            mc.rank = 250  # Initial rank
            
            # Generate other players
            players = []
            for i in range(249):
                cpu = generate_random_player()
                players.append(cpu)
                    
            # Load tournaments
            with open('tournaments.json', 'r') as f:
                tournament_data = json.load(f)
            
            all_tournaments = []
            for t in tournament_data:
                tourney = Tournament(t['name'], t['pts'], t['participants'], 
                                t['slam'], t['surface'], t['week'], t['country'])
                all_tournaments.append(tourney)
            
            # Simulate past 5 years
            current_year = date.today().year
            years_to_sim = 10
            sim_year = current_year - years_to_sim
            
            while sim_year < current_year:
                for week in range(1, 53):
                    week_tournaments = get_tournaments_for_week(week, all_tournaments)
                    
                    if len(week_tournaments) > 0:
                        sim_week_tournaments(week_tournaments, players, year=sim_year)
                    else:
                        for p in players:
                            p.point_history.append(0)
                    
                    players = update_rankings(players)
                
                players = year_end_changes(players, year=sim_year)
                
                sim_year += 1
            
            players.append(mc)
            
            # Save to session state
            st.session_state.mc = mc
            st.session_state.players = players
            st.session_state.all_tournaments = all_tournaments
            st.session_state.year = current_year
            st.session_state.week = 1
            
            st.success("Player created!")
            st.rerun()
            
        elif submit and not name:
            st.error("Please enter a valid name.")
        
        elif submit and (len(country) != 3):
            st.error("Please enter a valid 3-letter country code (ex. USA, ESP, FRA)")