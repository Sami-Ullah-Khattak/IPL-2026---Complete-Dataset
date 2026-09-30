import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- Page Config ---
st.set_page_config(
    page_title="IPL 2026 Analytics Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS for Styling ---
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0E1117;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #F8F9FA !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1A1C23;
        border-right: 1px solid #2D3039;
    }
    
    /* Metrics */
    div[data-testid="stMetricValue"] {
        color: #00D2D3;
        font-size: 2rem !important;
        font-weight: 700;
    }
    
    /* Dataframes */
    [data-testid="stDataFrame"] {
        border-radius: 8px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data
def load_data(filename):
    file_path = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return pd.DataFrame()

# Load all datasets
df_points = load_data('points_table.csv')
df_matches = load_data('matches.csv')
df_batting = load_data('batting_stats.csv')
df_bowling = load_data('bowling_stats.csv')

# --- Sidebar Navigation ---
st.sidebar.title("🏏 IPL 2026")
st.sidebar.markdown("### Dashboard Navigation")
page = st.sidebar.radio(
    "",
    ["Overview & Points Table", "Match Analysis", "Batting Statistics", "Bowling Statistics"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "Welcome to the interactive IPL 2026 Data Visualization Dashboard. "
    "Select a page above to explore different aspects of the tournament."
)

# --- Color Palette ---
primary_color = "#00D2D3"
secondary_color = "#FF9F43"
accent_color = "#EE5A24"
chart_template = "plotly_dark"

# --- 1. Overview & Points Table ---
if page == "Overview & Points Table":
    st.title("🏆 Tournament Overview & Points Table")
    st.markdown("A comprehensive look at the current standings of all teams.")
    
    if not df_points.empty:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Points Table")
            # Format the dataframe for better display
            display_df = df_points[['position', 'team', 'matches', 'wins', 'defeats', 'points', 'nrr']]
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                height=400
            )
            
        with col2:
            st.subheader("Points vs Net Run Rate")
            
            # Create interactive scatter/bubble chart
            fig = px.scatter(
                df_points, 
                x="points", 
                y="nrr", 
                color="team",
                size="wins",
                hover_name="team",
                text="team",
                title="Team Performance Matrix",
                template=chart_template,
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            fig.update_traces(textposition='top center')
            fig.update_layout(
                xaxis_title="Total Points",
                yaxis_title="Net Run Rate (NRR)",
                showlegend=False,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
            
        st.markdown("---")
        st.subheader("Team Points Distribution")
        
        fig_bar = px.bar(
            df_points.sort_values('points', ascending=False),
            x='team',
            y='points',
            color='nrr',
            title='Points by Team (Color represents NRR)',
            template=chart_template,
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.error("Points table data not found.")

# --- 2. Match Analysis ---
elif page == "Match Analysis":
    st.title("🏟️ Match Analysis")
    st.markdown("Insights into match results, toss decisions, and venues.")
    
    if not df_matches.empty:
        # Top level metrics
        total_matches = len(df_matches)
        completed = len(df_matches[df_matches['match_result'] == 'completed'])
        super_overs = len(df_matches[df_matches['super_over_match'] == 'Yes'])
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Matches", total_matches)
        m2.metric("Completed", completed)
        m3.metric("Super Overs", super_overs)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Toss Decisions")
            toss_counts = df_matches['toss_decision'].value_counts().reset_index()
            toss_counts.columns = ['Decision', 'Count']
            
            fig_toss = px.pie(
                toss_counts, 
                values='Count', 
                names='Decision',
                title="Bat vs Bowl Decision at Toss",
                hole=0.4,
                template=chart_template,
                color_discrete_sequence=[primary_color, secondary_color]
            )
            fig_toss.update_traces(textinfo='percent+label')
            st.plotly_chart(fig_toss, use_container_width=True)
            
        with col2:
            st.subheader("Top Venues")
            venue_counts = df_matches['venue'].value_counts().head(8).reset_index()
            venue_counts.columns = ['Venue', 'Matches']
            
            fig_venue = px.bar(
                venue_counts,
                x='Matches',
                y='Venue',
                orientation='h',
                title="Most Matches Played by Venue",
                template=chart_template,
                color='Matches',
                color_continuous_scale="Blues"
            )
            fig_venue.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_venue, use_container_width=True)
            
        st.subheader("First Innings vs Second Innings Score")
        # Ensure we don't have NaN values for scores
        score_df = df_matches.dropna(subset=['first_ings_score', 'second_ings_score'])
        
        fig_scores = go.Figure()
        fig_scores.add_trace(go.Scatter(
            x=score_df.index, y=score_df['first_ings_score'],
            mode='lines+markers', name='First Innings',
            line=dict(color=primary_color, width=2)
        ))
        fig_scores.add_trace(go.Scatter(
            x=score_df.index, y=score_df['second_ings_score'],
            mode='lines+markers', name='Second Innings',
            line=dict(color=accent_color, width=2)
        ))
        
        fig_scores.update_layout(
            title="Scores Progression Over Matches",
            xaxis_title="Match Index",
            yaxis_title="Runs Scored",
            template=chart_template,
            hovermode="x unified"
        )
        st.plotly_chart(fig_scores, use_container_width=True)
        
    else:
        st.error("Matches data not found.")

# --- 3. Batting Statistics ---
elif page == "Batting Statistics":
    st.title("🏏 Batting Statistics")
    st.markdown("Analyzing the most impactful and explosive batters of the tournament.")
    
    if not df_batting.empty:
        # Convert numeric columns to ensure proper plotting
        cols_to_numeric = ['runs', 'strike_rate', 'average', 'sixes', 'fours', 'highest_score' if 'highest_score' in df_batting.columns else 'high_score']
        for col in cols_to_numeric:
            if col in df_batting.columns:
                df_batting[col] = pd.to_numeric(df_batting[col], errors='coerce')
        
        # Top run scorers
        st.subheader("Top 10 Run Scorers")
        top_batsmen = df_batting.sort_values('runs', ascending=False).head(10)
        
        fig_runs = px.bar(
            top_batsmen,
            x='batsman',
            y='runs',
            color='team',
            hover_data=['average', 'strike_rate', 'sixes', 'fours'],
            title="Highest Run Getters",
            template=chart_template,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_runs, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Impact Matrix: Runs vs Strike Rate")
            # Filter for players with decent amount of runs to avoid clutter
            impact_batsmen = df_batting[df_batting['runs'] > 100]
            
            fig_impact = px.scatter(
                impact_batsmen,
                x='strike_rate',
                y='runs',
                color='team',
                size='sixes',
                hover_name='batsman',
                title="Runs vs Strike Rate (Bubble size = Sixes)",
                template=chart_template,
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            st.plotly_chart(fig_impact, use_container_width=True)
            
        with col2:
            st.subheader("Boundary Kings (Fours & Sixes)")
            
            fig_boundaries = go.Figure()
            fig_boundaries.add_trace(go.Bar(
                x=top_batsmen['batsman'],
                y=top_batsmen['fours'],
                name='Fours',
                marker_color=secondary_color
            ))
            fig_boundaries.add_trace(go.Bar(
                x=top_batsmen['batsman'],
                y=top_batsmen['sixes'],
                name='Sixes',
                marker_color=primary_color
            ))
            
            fig_boundaries.update_layout(
                barmode='stack',
                title="Boundary Distribution for Top Scorers",
                template=chart_template,
                xaxis_title="Batsman",
                yaxis_title="Count"
            )
            st.plotly_chart(fig_boundaries, use_container_width=True)
            
        st.subheader("Detailed Batting Stats")
        st.dataframe(df_batting.drop('position', axis=1, errors='ignore'), use_container_width=True, hide_index=True)
        
    else:
        st.error("Batting data not found.")

# --- 4. Bowling Statistics ---
elif page == "Bowling Statistics":
    st.title("🎯 Bowling Statistics")
    st.markdown("Discovering the most lethal and economical bowlers.")
    
    if not df_bowling.empty:
        # Convert numeric columns
        cols_to_numeric = ['wickets', 'economy', 'avg', 'dot_balls', 'overs']
        for col in cols_to_numeric:
            if col in df_bowling.columns:
                df_bowling[col] = pd.to_numeric(df_bowling[col], errors='coerce')
                
        # Top Wicket Takers
        st.subheader("Top 10 Wicket Takers")
        top_bowlers = df_bowling.sort_values('wickets', ascending=False).head(10)
        
        fig_wickets = px.bar(
            top_bowlers,
            x='bowler',
            y='wickets',
            color='team',
            hover_data=['economy', 'avg', 'dot_balls'],
            title="Purple Cap Contenders",
            template=chart_template,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_wickets, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Efficiency: Wickets vs Economy Rate")
            # Filter bowlers with min wickets to avoid outliers
            regular_bowlers = df_bowling[df_bowling['wickets'] > 2]
            
            fig_eff = px.scatter(
                regular_bowlers,
                x='economy',
                y='wickets',
                color='team',
                size='dot_balls',
                hover_name='bowler',
                title="Wickets vs Economy (Bubble Size = Dot Balls)",
                template=chart_template,
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            # Invert X axis so lower economy (better) is on the right
            fig_eff.update_xaxes(autorange="reversed")
            st.plotly_chart(fig_eff, use_container_width=True)
            
        with col2:
            st.subheader("Pressure Creators: Dot Balls")
            top_dots = df_bowling.sort_values('dot_balls', ascending=False).head(10)
            
            fig_dots = px.bar(
                top_dots,
                x='dot_balls',
                y='bowler',
                orientation='h',
                color='economy',
                title="Most Dot Balls Bowled (Color = Economy)",
                template=chart_template,
                color_continuous_scale="Teal"
            )
            fig_dots.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_dots, use_container_width=True)
            
        st.subheader("Detailed Bowling Stats")
        st.dataframe(df_bowling.drop('position', axis=1, errors='ignore'), use_container_width=True, hide_index=True)
        
    else:
        st.error("Bowling data not found.")
