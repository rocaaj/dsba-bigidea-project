import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import Sbopen, Pitch
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="xG Shot Map Dashboard",
    page_icon="⚽",
    layout="wide"
)

# Introduction Section
st.title("⚽ Expected Goals (xG) Shot Map Dashboard")
st.markdown("---")

st.markdown("""
### What is Expected Goals (xG)?

**Expected Goals (xG)** is a metric that quantifies the probability of scoring from a particular shot. 
It evaluates shot quality based on factors like location, angle, distance from goal, and shot type.

Think of xG as answering: *"How likely is this shot to result in a goal?"* A shot from 6 yards out, 
directly in front of goal might have an xG of 0.75 (75% chance), while a shot from 30 yards at a 
tight angle might have an xG of 0.05 (5% chance).

### Why xG Matters for Player Development

**For Attackers:**
- **Shot Selection**: Understanding xG helps you recognize when to shoot versus when to pass. 
  A 0.10 xG shot from distance might be better served as a pass to a teammate in a 0.40 xG position.
- **Positioning**: Learn which areas of the field create the highest-quality chances. 
  Focus your movement to get into these "danger zones" more often.
- **Performance Tracking**: Compare your actual goals to your xG total. 
  Consistently outperforming xG suggests clinical finishing; underperforming indicates areas to improve.

**For Defenders:**
- **Danger Recognition**: Identify which areas require tighter marking and defensive focus.
- **Tactical Awareness**: Understand where opponents are most likely to create high-quality chances.
- **Positioning**: Learn to deny space in high xG zones, forcing attackers into lower-quality shots.

**For Coaches:**
- **Tactical Analysis**: Evaluate whether your team is creating quality chances, not just volume.
- **Player Development**: Help players understand shot selection and positioning through data-driven feedback.
- **Game Planning**: Identify patterns in where your team creates and concedes dangerous opportunities.

---

### Interactive Shot Map

Use the controls below to explore shot maps from professional matches. Each shot is sized by its xG value 
(larger = higher quality chance), with goals highlighted and labeled with the scorer's name.
""")

st.markdown("---")

# Shot Map Functionality
parser = Sbopen()

# Load competition and match data
with st.spinner("Loading match data..."):
    df_competition = parser.competition()
    liga_df = df_competition.loc[df_competition['competition_name'] == 'La Liga']
    
    # Load matches for multiple seasons
    df_matches1 = parser.match(competition_id=11, season_id=23)
    df_matches2 = parser.match(competition_id=11, season_id=24)
    df_matches3 = parser.match(competition_id=11, season_id=25)
    df_matches4 = parser.match(competition_id=11, season_id=26)
    df_matches5 = parser.match(competition_id=11, season_id=27)
    df_matches6 = parser.match(competition_id=11, season_id=2)
    df_matches7 = parser.match(competition_id=11, season_id=1)
    df_matches8 = parser.match(competition_id=11, season_id=4)
    df_matches9 = parser.match(competition_id=11, season_id=42)
    df_matches10 = parser.match(competition_id=11, season_id=90)
    
    frames = [df_matches1, df_matches2, df_matches3, df_matches4, df_matches5, 
              df_matches6, df_matches7, df_matches8, df_matches9, df_matches10]
    df_matches = pd.concat(frames)

# Get unique seasons and teams
season_names = sorted(df_matches['season_name'].unique(), reverse=True)
all_teams = sorted(set(df_matches['home_team_name'].unique()) | set(df_matches['away_team_name'].unique()))

# Sidebar filters
st.sidebar.header("Match Filters")

selected_season = st.sidebar.selectbox(
    "Select Season",
    season_names,
    index=0 if len(season_names) > 0 else None,
    placeholder="Select season...",
)

selected_team = st.sidebar.selectbox(
    "Select Team",
    all_teams,
    index=0 if len(all_teams) > 0 else None,
    placeholder="Select team...",
)

# Filter matches based on selections
if selected_season and selected_team:
    team_matches = df_matches.loc[
        (df_matches['season_name'] == selected_season) & 
        ((df_matches['home_team_name'] == selected_team) | (df_matches['away_team_name'] == selected_team))
    ]
    
    if len(team_matches) > 0:
        # Create match options
        match_options = []
        for _, match in team_matches.iterrows():
            home = match['home_team_name']
            away = match['away_team_name']
            match_id = match['match_id']
            label = f"{home} vs {away}"
            match_options.append({
                'label': label,
                'match_id': match_id,
                'home_team': home,
                'away_team': away
            })
        
        labels = [option['label'] for option in match_options]
        
        if len(labels) > 0:
            selected_match_label = st.sidebar.selectbox(
                "Select Match",
                labels,
            )
            
            if selected_match_label:
                selected_match = next((option for option in match_options if option['label'] == selected_match_label), None)
                
                if selected_match:
                    # Load and display shot map
                    with st.spinner("Loading match events..."):
                        events_df = parser.event(selected_match['match_id'])[0]
                    
                    home_team_name = selected_match['home_team']
                    away_team_name = selected_match['away_team']
                    
                    shots = events_df.loc[(events_df.type_name == 'Shot')].set_index('id')
                    
                    shots_home_mask = (shots.team_name == home_team_name)
                    shots_away_mask = (shots.team_name == away_team_name)
                    
                    shots_home_df = shots.loc[shots_home_mask, ['x', 'y', 'shot_statsbomb_xg', 'outcome_name', 'player_name']]
                    shots_away_df = shots.loc[shots_away_mask, ['x', 'y', 'shot_statsbomb_xg', 'outcome_name', 'player_name']]
                    
                    # Create pitch visualization
                    pitch = Pitch(line_color='black')
                    fig, ax = pitch.grid(
                        grid_height=0.9, 
                        title_height=0.06, 
                        axis=False,
                        endnote_height=0.04, 
                        title_space=0, 
                        endnote_space=0
                    )
                    
                    # Plot home team shots
                    for i, row in shots_home_df.iterrows():
                        if row["outcome_name"] == 'Goal':
                            pitch.scatter(row.x, row.y, alpha=1, s=row.shot_statsbomb_xg * 1000, 
                                         color="red", ax=ax['pitch'], zorder=3)
                            pitch.annotate(row["player_name"], (row.x + 1, row.y - 2), 
                                           ax=ax['pitch'], fontsize=10, zorder=4)
                        else:
                            pitch.scatter(row.x, row.y, alpha=0.3, s=row.shot_statsbomb_xg * 1000, 
                                         color="red", ax=ax['pitch'], zorder=2)
                    
                    # Plot away team shots
                    for i, row in shots_away_df.iterrows():
                        if row["outcome_name"] == 'Goal':
                            pitch.scatter(120 - row.x, 80 - row.y, alpha=1, s=row.shot_statsbomb_xg * 1000, 
                                         color="blue", ax=ax['pitch'], zorder=3)
                            pitch.annotate(row["player_name"], (120 - row.x + 1, 80 - row.y - 2), 
                                           ax=ax['pitch'], fontsize=10, zorder=4)
                        else:
                            pitch.scatter(120 - row.x, 80 - row.y, alpha=0.3, s=row.shot_statsbomb_xg * 1000, 
                                         color="blue", ax=ax['pitch'], zorder=2)
                    
                    fig.suptitle(f"{selected_match['label']} - Shot Map", fontsize=24, y=0.98)
                    
                    # Add legend
                    st.markdown("""
                    **Legend:**
                    - 🔴 Red circles = Home team shots (size = xG value)
                    - 🔵 Blue circles = Away team shots (size = xG value)
                    - **Bold circles with names** = Goals scored
                    - Faded circles = Shots that didn't result in goals
                    """)
                    
                    st.pyplot(fig)
                    plt.clf()
                    
                    # Display summary statistics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        home_xg = shots_home_df['shot_statsbomb_xg'].sum()
                        st.metric("Home Team xG", f"{home_xg:.2f}")
                    
                    with col2:
                        home_goals = (shots_home_df['outcome_name'] == 'Goal').sum()
                        st.metric("Home Team Goals", home_goals)
                    
                    with col3:
                        away_xg = shots_away_df['shot_statsbomb_xg'].sum()
                        st.metric("Away Team xG", f"{away_xg:.2f}")
                    
                    with col4:
                        away_goals = (shots_away_df['outcome_name'] == 'Goal').sum()
                        st.metric("Away Team Goals", away_goals)
                else:
                    st.warning("Match data could not be loaded. Please try selecting a different match.")
            else:
                st.info("Please select a match from the dropdown above.")
        else:
            st.warning(f"No matches available for {selected_team} in {selected_season}.")
    else:
        st.info(f"No matches found for {selected_team} in {selected_season}. Please select different filters.")
else:
    st.info("Please select a season and team from the sidebar to view shot maps.")

