import streamlit as st
import pandas as pd
import plotly.graph_objects as go


if st.session_state.mc is None:
    st.switch_page("app.py")

st.title("Player Statistics")
    
col1, col2 = st.columns(2)

with col1:
    # Dropdown
    players_sorted = sorted(st.session_state.players, key=lambda p: p.rank)

    selected_player = st.selectbox(
        "Select Player",
        options=players_sorted,
        format_func=lambda p: f"{p.name}",
        index=next(i for i, p in enumerate(players_sorted) if p.main_character)
    )

    p = selected_player

# Bio
col1, col2 = st.columns(2)

with col1:

    st.write(f"**Country:** {p.country}")
    st.write(f"**Age:** {p.age} years old")
    st.write(f"**Player Type:** {p.type}")

with col2:
    
    st.write(f"**Current Rank:** #{p.rank} ({p.points} points)")
    st.write(f"**Career High Rank:** #{p.career_high_rank}")
    st.write(f"**Career Trophies:** {len(p.trophies)}")
    

st.write("---")

st.subheader("Ratings")

col1, col2 = st.columns(2)


with col2:     

    st.metric(label=f"Overall Rating", value=f"{p.rating}")
    
    ratings_df = pd.DataFrame(
        {
            "Skill": [
                "Serve",
                "Forehand",
                "Backhand",
                "Slice",
                "Volley",
                "Clutch",
                "Endurance",
            ],
            "Rating": [
                f"{p.serve:.1f}",
                f"{p.forehand:.1f}",
                f"{p.backhand:.1f}",
                f"{p.slice:.1f}",
                f"{p.volley:.1f}",
                f"{p.clutch:.1f}",
                f"{p.endurance:.1f}",
            ],

        }
    )

    st.dataframe(ratings_df, use_container_width=False, hide_index=True)
    
with col1:

    # Radar chart
    categories = ['Serve', 'Forehand', 'Backhand', 'Slice', 'Volley', 'Clutch', 'Endurance']
    values = [p.serve, p.forehand, p.backhand, p.slice, p.volley, p.clutch, p.endurance]

    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself'
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)
    
st.write("---")

col1, col2 = st.columns(2)

with col1:
    
    slams, masters, atp500, atp250, atp_finals = [], [], [], [], []

    for trophy in p.trophies:
        for tourney in st.session_state.all_tournaments:
            if tourney.name in trophy:
                match (tourney.pts):
                    case 2000:
                        slams.append(trophy)
                    case 1000:
                        masters.append(trophy)
                    case 500:
                        atp500.append(trophy)
                    case 250:
                        atp250.append(trophy)
                    case 1500:
                        atp_finals.append(trophy)
                break
        
        
        
    st.subheader("Trophy Case")

    levels = ["Slams", "Masters", "ATP 500", "ATP 250", "ATP Finals"]

    gs_tab, m1000_tab, atp500_tab, atp250_tab, atpfinals_tab = st.tabs(levels)
    with gs_tab:
        if slams:
            for trophy in slams:
                if "Champion" in trophy: st.write(f"**{trophy}**")
                else: st.write(f"{trophy}")
        else:
            st.write("_None_")
    with m1000_tab:
        if masters:
            for trophy in masters:
                if "Champion" in trophy: st.write(f"**{trophy}**")
                else: st.markdown(f"{trophy}")
        else:
            st.write("_None_")
    with atp500_tab:
        if atp500:
            for trophy in atp500:
                if "Champion" in trophy: st.write(f"**{trophy}**")
                else: st.write(f"{trophy}")
        else:
            st.write("_None_")
    with atp250_tab:
        if atp250:
            for trophy in atp250:
                if "Champion" in trophy: st.write(f"**{trophy}**")
                else: st.write(f"{trophy}")
        else:
            st.write("_None_")
    with atpfinals_tab:
        if atp_finals:
            for trophy in atp_finals:
                if "Champion" in trophy: st.write(f"**{trophy}**")
                else: st.write(f"{trophy}")
        else:
            st.write("_None_")
        
with col2:
    
    # Trophies
    trophy_counts = {
        "Grand Slam": 0,
        "Masters 1000": 0,
        "ATP 500": 0,
        "ATP 250": 0,
        "ATP Finals": 0
    }

    trophy_lists = {
        "Grand Slam": [],
        "Masters 1000": [],
        "ATP 500": [],
        "ATP 250": [],
        "ATP Finals": []
    }

    for trophy in p.trophies:
        lvl = None
        for tourney in st.session_state.all_tournaments:
            if tourney.name in trophy:
                match (tourney.pts):
                    case 2000:
                        lvl = "Grand Slam"
                    case 1000:
                        lvl = "Masters 1000"
                    case 500:
                        lvl = "ATP 500"
                    case 250:
                        lvl = "ATP 250"
                    case 1500:
                        lvl = "ATP Finals"
                break
            
        if lvl: 
            trophy_lists[lvl].append(trophy)
            
            if "Champion" in trophy:
                trophy_counts[lvl] += 1

    # Build dataframe
    levels = ["Grand Slam", "Masters 1000", "ATP 500", "ATP 250", "ATP Finals"]
    trophies_df = pd.DataFrame(
        {
            "Level": levels,
            "Championships": [trophy_counts[lvl] for lvl in levels],
            "Finals": [len(trophy_lists[lvl]) for lvl in levels],
        }
    )

    st.dataframe(trophies_df, use_container_width=True, hide_index=True)
    
    
st.write("---")

# Rank History Graph

current_week = st.session_state.week
rank_history = p.rank_history

st.subheader("Rank History")

tab_career, tab_last_52, tab_ytd = st.tabs(
    ["Career", "Past 52 Weeks", "Year-to-Date"]
)

def plot_rank_history(weeks, ranks, key=None):
    if not ranks:
        st.info("No ranking data available")
        return

    y_max = max(ranks) + 10

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=weeks,
            y=ranks,
            mode="lines+markers",
        )
    )

    fig.update_layout(
        xaxis_title="Week",
        yaxis_title="Rank",
        yaxis=dict(
            autorange=False,
            range=[y_max, 1],  # inverted rank axis
        ),
    )

    st.plotly_chart(fig, use_container_width=True, key=key)

# Career (all data)
with tab_career:
    weeks = [i for i, r in enumerate(rank_history) if r > 0]
    ranks = [r for r in rank_history if r > 0]
    plot_rank_history(weeks, ranks, key="career_rank_history")

# Past 52 Weeks
with tab_last_52:
    weeks = [i for i, r in enumerate(rank_history) if r > 0]
    ranks = [r for r in rank_history if r > 0]
    weeks = weeks[-52:]
    ranks = ranks[-52:]
    plot_rank_history(weeks, ranks, key="last_52_rank_history")

# Year-to-Date
with tab_ytd:
    weeks = [i for i, r in enumerate(rank_history) if r > 0]
    ranks = [r for r in rank_history if r > 0]
    weeks = weeks[-current_week:]
    ranks = ranks[-current_week:]
    plot_rank_history(weeks, ranks, key="ytd_rank_history")
