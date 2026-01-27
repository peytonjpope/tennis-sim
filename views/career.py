def render():

    import streamlit as st
    import math
    from main import (get_tournaments_for_week, sim_week_tournaments, year_end_changes,
                    update_rankings, TRAIN_OPTIONS, ENERGY_PER_SET)
    import pandas as pd
    import time
    import random
    
    if st.session_state.mc is None:
        st.switch_page("app.py")
    
    mc = st.session_state.mc
    
    if st.session_state.week <= 52:
        
        st.title(f"{st.session_state.year} Season - Week {st.session_state.week}")

        if not st.session_state.show_results:
            # WEEK ACTIONS VIEW
            mc = st.session_state.mc
            
            left_col, right_col = st.columns(2)
            
            with left_col:
                st.subheader("Tournaments")
                
                week_tournaments = get_tournaments_for_week(st.session_state.week, st.session_state.all_tournaments)
                
                if len(week_tournaments) == 0:
                    st.write("No tournaments this week")
                    for p in st.session_state.players:
                        p.point_history.append(0)
                    update_rankings(st.session_state.players)
                    st.session_state.week += 1
                    st.rerun()
                    
                else:
                    # Display tournament cards
                    tournament_options = []
                    for i, t in enumerate(week_tournaments):
                        required_energy = int(math.log2(t.participants)) * ENERGY_PER_SET * 3
                        eligible = t.pts < 1000 or mc.rank <= t.participants
                        enough_energy = mc.energy >= required_energy
                    
                        
                        if not eligible:
                            st.write(f"~~**{t.name}** ({t.country})~~")
                            st.write("_Ineligible ranking_")
                        elif not enough_energy:
                            st.write(f"~~**{t.name}** ({t.country})~~")
                            st.write("_Not enough Energy_")
                        else:
                            st.write(f"**{t.name}** ({t.country})")
                            st.write(f"{t.pts} pts | {t.surface} | {t.participants} players")
                            
                            tournament_options.append((i, f"{t.name}"))
            
            st.write("---")
            
            with right_col:
                st.subheader("Training")
                            
                train_df = pd.DataFrame(    
                    {
                        "Skill": 
                            [
                                "Serve",
                                "Forehand",
                                "Backhand",
                                "Slice",
                                "Volley",
                            ],
                        "": 
                            [
                                f"{mc.serve:.1f}",
                                f"{mc.forehand:.1f}",
                                f"{mc.backhand:.1f}",
                                f"{mc.slice:.1f}",
                                f"{mc.volley:.1f}",
                            ],
                        "Intangibles": 
                            [
                                "Energy",
                                "Clutch",
                                "Endurance",
                                "", 
                                "",
                            ],
                        " ": 
                            [
                                f"{mc.energy}",
                                f"{mc.clutch:.1f}",
                                f"{mc.endurance:.1f}",
                                "",
                                "",
                            ]
                    }
                )
                
                st.dataframe(train_df, use_container_width=False, hide_index=True)
                
            
            left_col, right_col = st.columns(2)
            
            with left_col:
                # Selectbox for tournaments
                if tournament_options:
                    selected_tournament = st.selectbox(
                        "Select Tournament",
                        options=[None] + tournament_options,
                        format_func=lambda x: "-- None --" if x is None else x[1],
                        key="tournament_select"
                    )
                else:
                    selected_tournament = None
            
            with right_col:
                # Selectbox for training
                selected_training = st.selectbox(
                    "Select Training",
                    options=[None] + TRAIN_OPTIONS,
                    format_func=lambda x: "-- None --" if x is None else x,
                    key="training_select"
                )
            
            # Determine which action is selected
            tournament_chosen = selected_tournament is not None
            training_chosen = selected_training is not None
            
            if tournament_chosen and training_chosen:
                st.warning("Please deselect one.")
                if 'selected_action' in st.session_state:
                    del st.session_state.selected_action
            elif tournament_chosen:
                st.session_state.selected_action = ("tournament", selected_tournament[0])
            elif training_chosen:
                st.session_state.selected_action = ("train", selected_training)
            else:
                if 'selected_action' in st.session_state:
                    del st.session_state.selected_action
            
            # Place Confirm button in appropriate column
            if 'selected_action' in st.session_state and not (tournament_chosen and training_chosen):
                action_type, action_data = st.session_state.selected_action
                
                button_col1, button_col2 = st.columns(2)
                
                # Show button in left column for tournament, right column for training
                if action_type == "tournament":
                    with button_col1:
                        confirm_clicked = st.button("Confirm", type="primary", use_container_width=True)
                else:  # training
                    with button_col2:
                        confirm_clicked = st.button("Confirm", type="primary", use_container_width=True)
                
                if confirm_clicked:
                    if action_type == "train":
                        selected_option = action_data
                        old_val = getattr(mc, selected_option.lower()) if selected_option != "Rest" else mc.energy
                        
                        if selected_option == "Rest":
                            mc.energy += 25
                        else:
                            setattr(mc, selected_option.lower(), getattr(mc, selected_option.lower()) + random.choices([1, 2, 3], weights=[2, 3, 1])[0])

                            mc.update_rating()
                        
                        new_val = getattr(mc, selected_option.lower()) if selected_option != "Rest" else mc.energy
                        
                        st.session_state.week_results = {
                            'type': 'training',
                            'stat': selected_option,
                            'old_val': old_val,
                            'new_val': new_val
                        }
                        
                        week_tournaments = get_tournaments_for_week(st.session_state.week, st.session_state.all_tournaments)
                        tournament_results, _ = sim_week_tournaments(week_tournaments, st.session_state.players, 
                                                                    mc_tournament_selection=None, main_character=None, 
                                                                    year=st.session_state.year)
                        
                    else:  # tournament
                        mc_tournament_selection = action_data
                        week_tournaments = get_tournaments_for_week(st.session_state.week, st.session_state.all_tournaments)
                        
                        tournament_results, mc_matches = sim_week_tournaments(week_tournaments, st.session_state.players, 
                                        mc_tournament_selection=mc_tournament_selection, 
                                        main_character=mc,
                                        year=st.session_state.year)
                        
                        st.session_state.week_results = {
                            'type': 'tournament',
                            'tournament': week_tournaments[mc_tournament_selection],
                            'matches': mc_matches
                        }
                                        
                    # Store other tournament winners
                    st.session_state.other_tournament_results = [
                        (result['tournament'].name, result['champion']) 
                        for result in tournament_results
                    ]
                    
                    st.session_state.selected_action = None
                    st.session_state.show_results = True
                    st.rerun()

        else:
            # RESULTS VIEW
            mc = st.session_state.mc
            
            # Determine column layout based on content
            if st.session_state.week_results['type'] == 'training':
                num_cols = 3
            elif len(st.session_state.week_results.get('matches', [])) == 1:
                num_cols = 2
            else:
                num_cols = 3
            
            # HEADER ROW
            if num_cols == 2:
                h1, h2 = st.columns(2)
                with h1:
                    st.subheader("Your Results")
                with h2:
                    st.subheader("Tournament Results")
            else:
                h1, h2, h3 = st.columns(3)
                with h1:
                    st.subheader("Your Results")
                with h3:
                    st.subheader("Tournament Results")
            
            # CONTENT ROW
            if num_cols == 2:
                col1, col2 = st.columns(2)
                col3 = None
            else:
                col1, col2, col3 = st.columns(3)
            
            # Display training results
            if st.session_state.week_results['type'] == 'training':
                with col1:
                    stat = st.session_state.week_results['stat']
                    old = st.session_state.week_results['old_val']
                    new = st.session_state.week_results['new_val']
                    st.metric(label=f"{stat}", value=f"{new:.1f}", delta=f"{new - old:.1f}")
                
                with col2:
                    # Show overall rating change if not Rest
                    if stat != "Rest":
                        old_rating = mc.rating - (new - old)  # Approximate old rating
                        st.metric(label="Overall", value=f"{mc.rating:.1f}", delta=f"{mc.rating - old_rating:.1f}")
            
            # Display tournament results
            else:
                matches = st.session_state.week_results.get('matches', [])
                
                # Alternate matches between col1 and col2 (if col2 exists)
                for idx, match in enumerate(matches):
                    # Select column based on index
                    if col3 is None:
                        current_col = col1
                    else:
                        current_col = col1 if idx % 2 == 0 else col2
                    
                    with current_col:
                        winner = match['winner']
                        loser = match['loser']
                        p1 = match['p1']
                        p2 = match['p2']
                        
                        # Format player names with rankings
                        if p1.rank < 26:  # Top 25 players
                            p1_name = f"({p1.rank}) {p1.name}"
                        else:
                            p1_name = f"{p1.name}"
                        if p2.rank < 26:
                            p2_name = f"({p2.rank}) {p2.name}"
                        else:
                            p2_name = f"{p2.name}"
                        
                        # Build table with winner on top
                        if p1 == winner:
                            table = f"""
                                    R{0 + 1} {'**Win**' if winner == mc else 'Loss'} {"| " * (len(match['p1_scores']))}|
                                    {"|---" * (len(match['p1_scores'])+1)} |
                                    | {p1_name} | {' | '.join(str(s) for s in match['p1_scores'])} |
                                    | {p2_name} | {' | '.join(str(s) for s in match['p2_scores'])} |

                                    """
                        else:
                            table = f"""
                                    R{0 + 1} {'**Win**' if winner == mc else 'Loss'} {"| " * (len(match['p2_scores']))}|
                                    {"|---" * (len(match['p2_scores'])+1)} |
                                    | {p2_name} | {' | '.join(str(s) for s in match['p2_scores'])} |
                                    | {p1_name} | {' | '.join(str(s) for s in match['p1_scores'])} |

                                    """
                        st.markdown(table)
                        # if idx > 0: time.sleep(1)  # Pause for dramatic effect
            
            # Tournament Results content (in col3 if exists, else col2)
            tournament_col = col3 if col3 is not None else col2
            with tournament_col:
                if 'other_tournament_results' in st.session_state:
                    for tourney_name, winner in st.session_state.other_tournament_results:
                        st.markdown(f"- {tourney_name} Champion:\n    - ({winner.rank}) {winner.name}")

            st.write("---")
            
            col1, button_col, col3 = st.columns([1, 2, 1])
            
            with button_col:
                if st.button("Advance Week", type="primary", use_container_width=True):
                    update_rankings(st.session_state.players)
                    st.session_state.week += 1
                    st.session_state.show_results = False
                    st.session_state.week_results = {}
                    st.rerun()
    else:
        # End of Year Summary -------------------------------
        players = st.session_state.players
        mc = [p for p in players if p.main_character][0]
                
        st.title(f"{st.session_state.year} Season Summary")
        
        col1, col2 = st.columns(2)
        
        with col1:
            
            st.subheader(f"{mc.name}'s Year")
            
            st.write(f"**Final Rank:** #{mc.rank} ({mc.points} points)")
            st.write(f"**Rank Improvement:** {mc.rank_history[-52] - mc.rank if len(mc.rank_history) > 52 else 'N/A'} spots")
            
            
        with col2:
            
            st.subheader("Highlights")
            
            st.write(f"Year-End World No. 1: {[p for p in st.session_state.players if p.rank == 1][0].name}")
            
            
        
        st.write("---")
        
        col1, button_col, col3 = st.columns([1, 2, 1])
        
        # Advance Year Button
        
        with button_col:
            if st.button("Advance Year", type="primary", use_container_width=True):
                
                st.session_state.players = year_end_changes(st.session_state.players, st.session_state.year)
                
                # Resume career logic
                st.session_state.year += 1
                st.session_state.week = 1
                
                # Reload Page
                st.rerun()
                