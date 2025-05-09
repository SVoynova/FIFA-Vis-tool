import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import Dash, dcc
from dash.dependencies import Input, Output
from . import ids
from . import data_utils

# Load cleaned team data
TEAM_DATA = pd.read_csv("data/cleaned/team_data_clean.csv")

# -----------------------------------------------------------------------------
# Add tournament stage information if it is missing
# The stage values correspond to the dropdown in `filter.py`:
#   1 = Group Stage (all teams)
#   2 = Round of 16
#   3 = Quarter Finals
#   4 = Semi Finals
#   5 = Third Place
#   6 = Finals
# We derive the stage reached for each team based on the number of games played
# (and a small manual mapping for the last four teams that all played 7 games).
# -----------------------------------------------------------------------------
if "stage" not in TEAM_DATA.columns:
    finals_teams = {"Argentina", "France"}
    third_place_teams = {"Croatia", "Morocco"}

    def _determine_stage(row):
        team = row["team"]
        if team in finals_teams:
            return 6  # Finals (Champion / Runner-up)
        if team in third_place_teams:
            return 5  # Third-place match contestants

        games = int(row["games"])
        if games >= 6:
            # Safety fallback – should not happen for 2022 World Cup data
            return 4  # Semi Finals
        if games == 5:
            return 3  # Quarter Finals
        if games == 4:
            return 2  # Round of 16
        # Default: eliminated in the group stage
        return 1

    TEAM_DATA["stage"] = TEAM_DATA.apply(_determine_stage, axis=1)

# Add jitter to avoid overlapping points
JITTER_AMOUNT = 0.01
def add_jitter(series):
    return series + np.random.normal(0, JITTER_AMOUNT, len(series))

def render(app: Dash) -> dcc.Graph:
    @app.callback(
        [
            Output(ids.SCATTER_PLOT, "figure"),
            Output(ids.FILTERED_TEAMS_STORE, "data")
        ],
        [
            Input(ids.X_AXIS_DROPDOWN, "value"),
            Input(ids.Y_AXIS_DROPDOWN, "value"),
            Input(ids.FILTER, "value")
        ],
        # Remove teams_dropdown as input to avoid circular dependency
    )
    def update_scatter(x_col, y_col, filter_val):
        # Start with a copy of the data
        df = TEAM_DATA.copy()
        
        # Apply tournament stage filter – show teams that reached AT LEAST the
        # selected stage. 0 = All teams (no filtering).
        filtered_df = df.copy()
        if filter_val > 0:
            filtered_df = df[df["stage"] >= filter_val]
        
        # Store the list of filtered teams for other components to use
        filtered_teams = filtered_df["team"].unique().tolist()
        
        # Create a figure with custom traces for better accessibility
        fig = go.Figure()
        
        # Instead of showing all teams, show a message to select teams
        fig.add_annotation(
            text="Select teams from the dropdown to display them on the scatter plot",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="#666666")
        )
        
        # Update layout
        fig.update_layout(
            xaxis_title=x_col,
            yaxis_title=y_col,
            legend_title_text="Teams",
            title={
                'text': "Team Capability Comparison",
                'x': 0.5,
                'xanchor': 'center'
            },
            margin=dict(t=50, l=20, r=20, b=40),
            height=600,  # Set fixed height
            plot_bgcolor='rgba(250, 250, 250, 0.9)',  # Light background
            font=dict(size=12),  # Larger font
            legend=dict(
                itemsizing='constant',  # Make legend symbols consistent size
                borderwidth=1,  # Add border to legend
                bordercolor='rgba(0,0,0,0.1)',
                bgcolor='rgba(255, 255, 255, 0.9)',  # Semi-transparent background
                font=dict(size=12)
            )
        )

        return fig, filtered_teams
        
    # Add a separate callback to update the scatter plot based on team selection
    @app.callback(
        Output(ids.SCATTER_PLOT, "figure", allow_duplicate=True),
        [
            Input(ids.TEAMS_DROPDOWN, "value"),
            Input(ids.FILTERED_TEAMS_STORE, "data"),
            Input(ids.X_AXIS_DROPDOWN, "value"),
            Input(ids.Y_AXIS_DROPDOWN, "value")
        ],
        prevent_initial_call=True
    )
    def update_scatter_team_selection(selected_teams, filtered_teams, x_col, y_col):
        # Start with a copy of the data for teams that pass the filter
        df = TEAM_DATA.copy()
        filtered_df = df[df["team"].isin(filtered_teams)].copy()
        
        # Add jitter to avoid point overlap
        filtered_df["x"] = add_jitter(filtered_df[x_col])
        filtered_df["y"] = add_jitter(filtered_df[y_col])

        # Create a figure with custom traces for better accessibility
        fig = go.Figure()
        
        # Get all teams from filtered data
        all_teams = filtered_df["team"].unique().tolist()
        
        # Always show only selected teams if any are selected
        teams_to_show = []
        if selected_teams:
            # Show only teams that are both selected AND exist in the filtered data
            teams_to_show = [team for team in selected_teams if team in all_teams]
        
        # If no teams are selected, show a message instead of all teams
        if not teams_to_show:
            fig.add_annotation(
                text="Select teams from the dropdown to display them on the scatter plot",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=16, color="#666666")
            )
            
            # Update layout for empty plot
            fig.update_layout(
                xaxis_title=x_col,
                yaxis_title=y_col,
                legend_title_text="Teams",
                title={
                    'text': "Team Capability Comparison",
                    'x': 0.5,
                    'xanchor': 'center'
                },
                margin=dict(t=50, l=20, r=20, b=40),
                height=600,  # Set fixed height
                plot_bgcolor='rgba(250, 250, 250, 0.9)',  # Light background
                font=dict(size=12)  # Larger font
            )
            return fig
        
        # Create one trace per team for better control of appearance
        for team in teams_to_show:
            team_df = filtered_df[filtered_df["team"] == team]
            if team_df.empty:
                continue
                
            # Get consistent color and symbol for the team
            color = data_utils.get_team_color(team)
            symbol = data_utils.get_team_symbol(team)
            
            # Add trace with distinctive color and symbol
            fig.add_trace(go.Scatter(
                x=team_df["x"],
                y=team_df["y"],
                mode="markers",
                marker=dict(
                    color=color,
                    symbol=symbol,
                    size=14,  # Slightly larger size for better visibility
                    line=dict(width=2, color='#000000')  # Add thicker black outline for better visibility
                ),
                name=team,
                text=team,
                hovertemplate=f"<b>{team}</b><br>{x_col}: %{{x:.2f}}<br>{y_col}: %{{y:.2f}}<extra></extra>"
            ))
        
        # Update layout
        fig.update_layout(
            xaxis_title=x_col,
            yaxis_title=y_col,
            legend_title_text="Teams",
            title={
                'text': "Team Capability Comparison",
                'x': 0.5,
                'xanchor': 'center'
            },
            margin=dict(t=50, l=20, r=20, b=40),
            height=600,  # Set fixed height
            plot_bgcolor='rgba(250, 250, 250, 0.9)',  # Light background
            font=dict(size=12),  # Larger font
            legend=dict(
                itemsizing='constant',  # Make legend symbols consistent size
                borderwidth=1,  # Add border to legend
                bordercolor='rgba(0,0,0,0.1)',
                bgcolor='rgba(255, 255, 255, 0.9)',  # Semi-transparent background
                font=dict(size=12)
            )
        )

        return fig

    return dcc.Graph(
        id=ids.SCATTER_PLOT,
        config={'displayModeBar': True, 'scrollZoom': True},
        className="shadow-sm border rounded"
    )
