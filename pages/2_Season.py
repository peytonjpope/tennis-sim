import streamlit as st
import pandas as pd

# MC
mc = st.session_state.mc

if st.session_state.mc is None:
    st.switch_page("app.py")

players = sorted(st.session_state.players, key=lambda p: (-p.points, -p.rating))

tournaments = sorted(
    st.session_state.all_tournaments,
    key=lambda t: ((t.week - st.session_state.week) % 52, t.pts)
)



def change_in_rank(player):
    return player.rank_history[-2] - player.rank

def signed_change_in_rank(player):
    if change_in_rank(player) > 0: return f"↑{change_in_rank(player)}"
    elif change_in_rank(player) == 0: return "–"
    else: return f"↓{abs(change_in_rank(player))}"

col1, col2 = st.columns(2)

with col1:

    st.title("ATP Rankings")

with col2:
    
    st.metric(label=f"{mc.name} Rank", value=f"#{mc.rank}", delta=change_in_rank(mc))


# Full rankings
p_data = []
for p in players:
    p_data.append({
        "Rank": p.rank,
        "+/-": signed_change_in_rank(p),
        "Player": p.name,
        "Country": p.country,
        "Age": p.age,
        "Type": p.type,
        "Points": p.points,
        "Rating": f"{p.rating:.1f}"
        
    })

df = pd.DataFrame(p_data)

# Highlight MC row
def highlight_players(row):
    # MC
    if row['Player'] == mc.name:
        return ['background-color: lightgreen'] * len(row)
    
    # # Race to ATP Finals
    # if row['Rank'] <= 8:
    #     return ['background-color: aliceblue'] + ([''] * (len(row) - 1))
    
    # Green/Red change in rank
    if '↑' in row['+/-']:
        return [''] + ['background-color: lavenderblush'] + ([''] * (len(row) - 2))
    if '↓' in row['+/-']:
        return [''] + ['background-color: honeydew'] + ([''] * (len(row) - 2))
    return [''] * len(row)

st.dataframe(df.style.apply(highlight_players, axis=1), use_container_width=True, hide_index=True)

st.write("---")

# Schedule -------------------------------

col1, col2 = st.columns(2)

with col1:

    st.title("Tour Tournaments")

with col2:
    
    st.metric(label="Current Week", value=f"{st.session_state.week}/52")

# All tournaments
t_data = []
for t in tournaments:
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
    # MC
    if row['Points'] == 2000:
        return ['background-color: cornsilk'] * len(row)
    return [''] * len(row)

st.dataframe(df_tourneys.style.apply(highlight_tournaments, axis=1), use_container_width=True, hide_index=True)
