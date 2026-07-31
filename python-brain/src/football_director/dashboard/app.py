import sys
import plotly.graph_objects as go
from pathlib import Path
import polars as pl
import streamlit as st
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.decomposition import PCA


st.title("Football Director")
st.write("A data driven player scouting tool")

BASE = Path(__file__).parent.parent.parent.parent.parent
options = pl.read_parquet(BASE / 'data/processed/player_profiles.parquet')
similar_players = pl.read_parquet(BASE / 'data/processed/player_vectors.parquet')

# Extract a list of names from the df
player_names = options['player_name'].to_list()

# Create the min-max for the graphs
min_prog_carries = options["progressive_carries"].min()
max_prog_carries = options["progressive_carries"].max()

min_xg = options["avg_xg"].min()
max_xg = options["avg_xg"].max()

min_pressures = options["total_pressures"].min()
max_pressures = options["total_pressures"].max()

min_tackles = options["tackles"].min()
max_tackles = options["tackles"].max()

all_defensive_actions = options['total_interceptions'] + options['tackles']
min_defensive_actions = all_defensive_actions.min()
max_defensive_actions = all_defensive_actions.max()

min_carries_under_press = options["carries_under_pressure"].min()
max_carries_under_press = options["carries_under_pressure"].max()

# Calculate for all players
all_pass_completion = (options['successful_passes'] / options['total_passes'] * 100).fill_nan(0)
all_shot_accuracy = (options['shots_on_target'] / options['total_shots'] * 100).fill_nan(0)

# Get min and max
pass_completion_min = all_pass_completion.min()
pass_completion_max = all_pass_completion.max()

shot_accuracy_min = all_shot_accuracy.min()
shot_accuracy_max = all_shot_accuracy.max()

# Helper function
def normalise(value, min_val, max_val):
    if max_val == min_val:
        return 0
    return (value - min_val) / (max_val - min_val)

search_bar = st.selectbox(
    "Search Player",player_names, placeholder= 'Player Search...',
    filter_mode = "contains", index = None
)

if search_bar:
    # find the player row
    player_row = options.filter(pl.col('player_name') == search_bar)

    # Extract values
    total_passes = player_row['total_passes'][0]
    successful_passes = player_row['successful_passes'][0]
    passes_under_pressure = player_row['passes_under_pressure'][0]
    pass_completion_pct = (successful_passes / total_passes * 100) if total_passes > 0 else 0
    pass_completion_under_pressure_pct = player_row['pass_completion_under_pressure_pct'][0]

    total_carries = player_row['total_carries'][0]
    progressive_carries = player_row['progressive_carries'][0]
    carries_under_pressure = player_row['carries_under_pressure'][0]

    total_shots = player_row['total_shots'][0]
    goals = player_row['goals'][0]
    shots_on_target = player_row['shots_on_target'][0]
    avg_xg = player_row['avg_xg'][0]
    shot_accuracy_pct = (shots_on_target / total_shots * 100) if total_shots > 0 else 0

    total_pressures = player_row['total_pressures'][0]
    total_interceptions = player_row['total_interceptions'][0]
    total_clearances = player_row['total_clearances'][0]
    tackles = player_row['tackles'][0]

    # The normalised metrics for the players
    norm_pass_completion = normalise(pass_completion_pct, pass_completion_min, pass_completion_max)
    norm_prog_carries = normalise(progressive_carries, min_prog_carries, max_prog_carries)
    norm_XG = normalise(avg_xg, min_xg, max_xg)
    norm_shot_accuracy = normalise(shot_accuracy_pct, shot_accuracy_min, shot_accuracy_max)
    norm_pressures = normalise(total_pressures , min_pressures, max_pressures)
    norm_tackles = normalise(tackles, min_tackles, max_tackles)
    norm_carries_under_press = normalise(carries_under_pressure, min_carries_under_press, max_carries_under_press)


    col_img, col_name = st.columns([1, 3])
    with col_img:
        st.image("https://upload.wikimedia.org/wikipedia/commons/8/89/Portrait_Placeholder.png", width=120)
    with col_name:
        st.title(search_bar)


    categories = [
    'Pass Completion', 'Progressive Carries', 'Avg xG',
    'Shot Accuracy', 'Pressures', 'Tackles', 'Carries Under Pressure'
    ]

    values = [
        norm_pass_completion, norm_prog_carries, norm_XG,
        norm_shot_accuracy, norm_pressures, norm_tackles, norm_carries_under_press
    ]

    # Close the radar chart by repeating first value
    values_closed = values + [values[0]]
    categories_closed = categories + [categories[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill='toself',
        name=search_bar
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=False
    )

    st.plotly_chart(fig)

    # Card
    st.subheader("Passing")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Passes", total_passes)
    with col2:
        st.metric("Completion %", f"{pass_completion_pct:.1f}%")
    with col3:
        st.metric("Under Pressure %", f"{pass_completion_under_pressure_pct:.1f}%")

    st.divider()

    st.subheader("Carrying")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Carries", total_carries)
    with col2:
        st.metric("Progressive Carries", progressive_carries)
    with col3:
        st.metric("Under Pressure", f"{carries_under_pressure:.1f}%")

    st.divider()

    st.subheader("Shots")
    col1, col2, col3, col4, col5= st.columns(5)
    with col1:
        st.metric("Total Shots", total_shots)
    with col2:
        st.metric("Total Goals", goals)
    with col3:
        st.metric("Shots on Target", shots_on_target)
    with col4:
        st.metric("Average XG", f"{avg_xg:.2f}")
    with col5:
        st.metric("Shot Accuracy", f"{shot_accuracy_pct :.1f}%")

    st.divider()

    st.subheader("Defending & Pressing")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Pressures", total_pressures)
    with col2:
        st.metric("Total Interceptions", total_interceptions)
    with col3:
        st.metric("Total Clearances", total_clearances)
    with col4:
        st.metric("Total Tackles", tackles)

    st.divider()

    # Cosine Similarity, Get component columns only
    vectors = similar_players.select(
        [col for col in similar_players.columns if col.startswith('component_')]
    ).to_numpy()

    # Find player index
    player_names_list = similar_players['player_name'].to_list()
    idx = player_names_list.index(search_bar)

    st.subheader("Similar Players")

    # Split into rows of 5

    player_vectors = vectors[idx].reshape(1, -1)
    similarities = cosine_similarity(player_vectors, vectors)[0]
    similar_indices = np.argsort(similarities)[::-1][1:11]

    # Split into rows of 5
    cols = st.columns(5)
    for count, i in enumerate(similar_indices):
        name = player_names_list[int(i)]
        score = similarities[i]
        with cols[count % 5]:
            with st.container(border=True):
                st.image("https://upload.wikimedia.org/wikipedia/commons/8/89/Portrait_Placeholder.png", width=60)
                st.write(f"**{name}**")
                st.write(f"Similarity: {score:.2f}")
