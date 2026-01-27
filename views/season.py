def render():

    import streamlit as st
    import pandas as pd
    from main import get_tournaments_for_week
    from main import country_to_flag

    # MC
    mc = st.session_state.mc

    if st.session_state.mc is None:
        st.warning("Please create a player first")
        st.stop()
        
    def ytd_points(player):
        current_week = st.session_state.week
        return sum(player.point_history[-current_week:])
        

    players_live_ranked = sorted(st.session_state.players, key=lambda p: (-p.points, -p.rating))
    players_ytd_ranked = sorted(st.session_state.players, key=lambda p: (-ytd_points(p), -p.rating))


    all_tournaments = st.session_state.all_tournaments
    tournaments_atp = sorted(
        [t for t in st.session_state.all_tournaments if t.pts >= 250],
        key=lambda t: ((t.week - st.session_state.week) % 52, t.pts)
    )

    tournaments_challenger = sorted(
        [t for t in st.session_state.all_tournaments if t.pts < 250],
        key=lambda t: ((t.week - st.session_state.week) % 52, t.pts)
    )
    
    weeks_ago = 1
    current_week = st.session_state.week
    while len(get_tournaments_for_week(((current_week - weeks_ago - 1) % 52) + 1, all_tournaments)) == 0:
        weeks_ago += 1

    def change_in_rank(player, weeks_ago=1):
        if weeks_ago >= len(player.rank_history):
            return 0
        return player.rank_history[-(weeks_ago + 1)] - player.rank

    def signed_change_in_rank(player, weeks_ago=1):
        if change_in_rank(player, weeks_ago) > 0: return f"↑{change_in_rank(player, weeks_ago)}"
        elif change_in_rank(player, weeks_ago) == 0: return "–"
        else: return f"↓{abs(change_in_rank(player, weeks_ago))}"
        
    # Highlight MC row
    def highlight_players_live(row):
        # MC
        if row['Player'] == mc.name:
            return ['background-color: rgb(200, 250, 0, .07)'] * (len(row))
        
        # # Race to ATP Finals
        # if row['Rank'] <= 8:
        #     return ['background-color: aliceblue'] + ([''] * (len(row) - 1))
        
        # Green/Red change in rank
        if '↑' in row['+/-']:
            value = abs(float(row["+/-"][1:]))
            alpha = max(0.1, min(0.32, float(value / 33)))   
            return [''] + [f'background-color: rgb(0, 255, 0, {alpha})'] + ([''] * (len(row) - 2))
        if '↓' in row['+/-']:
            value = abs(float(row["+/-"][1:]))
            alpha = max(0.1, min(0.32, float(value / 33)))   
            return [''] + [f'background-color: rgb(255, 0, 0, {alpha})'] + ([''] * (len(row) - 2))
        return [''] * len(row)
    
    
    def highlight_players_ytd(row):
        # MC
        if row['Player'] == mc.name:
            return ['background-color: rgb(200, 250, 0, .07)'] * (len(row))
        
        # Race to ATP Finals
        if row['YTD Rank'] <= 8:
            return ['background-color: rgb(0, 200, 250, .1)'] + ([''] * (len(row) - 1))
        

        return [''] * len(row)
    
    # Rankings Section -------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.title("ATP Rankings")

    with col2:
        
        st.metric(label=f"{mc.name} Rank", value=f"#{mc.rank}", delta=change_in_rank(mc))


    # Tabs for Live Rankings and Year-End Rankings
    tab1, tab2 = st.tabs(["Live Rankings", "YTD Rankings"])
    
    # Live Ranking 
    with tab1:
        
        p_data = []
        for p in players_live_ranked:
            p_data.append({
                "Rank": p.rank,
                "+/-": signed_change_in_rank(p, weeks_ago=weeks_ago),
                "Player": p.name,
                "Country": country_to_flag(p.country),
                "Age": p.age,
                "Type": p.type,
                "Points": p.points,
                "Rating": f"{p.rating:.1f}"
                
            })

        df = pd.DataFrame(p_data)

        st.dataframe(df.style.apply(highlight_players_live, axis=1), use_container_width=True, hide_index=True)

    # YTD Ranking
    with tab2:
        p_data = []
        for r, p in enumerate(players_ytd_ranked):
            p_data.append({
                "YTD Rank": r + 1,
                "Live Rank": p.rank,
                "Player": p.name,
                "Country": country_to_flag(p.country),
                "Age": p.age,
                "Type": p.type,
                "Points": ytd_points(p),
                "Rating": f"{p.rating:.1f}"
                
            })

        df = pd.DataFrame(p_data)

        st.dataframe(df.style.apply(highlight_players_ytd, axis=1), use_container_width=True, hide_index=True)

        
        
    st.write("---")

    # Tournaments Section -------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.title("Tournaments")

    with col2:
        
        st.metric(label="Current Week", value=f"{st.session_state.week}/52")
        
    tab1, tab2 = st.tabs(["ATP", "_Challenger_"])
    
    with tab1:

        # ATP tournaments
        t_data = []
        for t in tournaments_atp:
            t_data.append({
                "Week": t.week,
                "Tournament": t.name,
                "Points": t.pts,
                "Country": t.country,
                "Surface": t.surface,
                "Participants": t.participants
            })

        df_tourneys = pd.DataFrame(t_data)

        # Highlight MC row
        def highlight_tournaments(row):
            # Grand slams
            if row['Points'] == 2000:
                return ['background-color: rgb(255, 215, 0, .05)'] * len(row)
            return [''] * len(row)

        st.dataframe(df_tourneys.style.apply(highlight_tournaments, axis=1), use_container_width=True, hide_index=True)

    with tab2:
        
        # Challenger tournaments
        t_data = []
        for t in tournaments_challenger:
            t_data.append({
                "Week": t.week,
                "Tournament": t.name,
                "Points": t.pts,
                "Country": t.country,
                "Surface": t.surface,
                "Participants": t.participants
            })

        df_tourneys = pd.DataFrame(t_data)



        st.dataframe(df_tourneys.style.apply(highlight_tournaments, axis=1), use_container_width=True, hide_index=True)
