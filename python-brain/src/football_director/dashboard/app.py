import sys
from pathlib import Path
import polars as pl
import streamlit as st
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.decomposition import PCA

st.markdown("""
    <style>
    div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlock"] {
        min-height: 180px;
    }
    </style>
""", unsafe_allow_html=True)


st.title("Football Director")
st.write("A data driven player scouting tool")

options = pl.read_parquet(Path("../../../../data/processed/player_profiles.parquet"))
similar_players = pl.read_parquet(Path("../../../../data/processed/player_vectors.parquet"))

# Extract a list of names from the df
player_names = options['player_name'].to_list()

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
