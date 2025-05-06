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

# Add jitter to avoid overlapping points
JITTER_AMOUNT = 0.01
def add_jitter(series):
    return series + np.random.normal(0, JITTER_AMOUNT, len(series))

def render(app: Dash) -> dcc.Graph:
    @app.callback(
        Output(ids.SCATTER_PLOT, "figure"),
        Input(ids.X_AXIS_DROPDOWN, "value"),
        Input(ids.Y_AXIS_DROPDOWN, "value"),
        Input(ids.FILTER, "value"),
        Input(ids.TEAMS_DROPDOWN, "value"),
    )
    def update_scatter(x_col, y_col, filter_val, selected_teams):
        # Start with a copy of the data
        df = TEAM_DATA.copy()
        
        # Apply tournament stage filter if selected (filter_val > 0)
        # This was missing and caused the filter not to work
        if filter_val > 0 and 'stage' in df.columns:
            df = df[df['stage'] == filter_val]
        
        # Add jitter to avoid point overlap
        df["x"] = add_jitter(df[x_col])
        df["y"] = add_jitter(df[y_col])

        # Create a figure with custom traces for better accessibility
        fig = go.Figure()
        
        # Get all teams and determine which ones to highlight
        all_teams = df["team"].unique().tolist()
        should_highlight = selected_teams and len(selected_teams) < len(all_teams)
        
        # Define teams to show (all or selected)
        # Filter by the selected teams AND the tournament stage
        teams_to_show = []
        if selected_teams and should_highlight:
            # Show only teams that are both selected AND exist in the filtered data
            teams_to_show = [team for team in selected_teams if team in all_teams]
        else:
            teams_to_show = all_teams
        
        # Create one trace per team for better control of appearance
        for team in teams_to_show:
            team_df = df[df["team"] == team]
            if team_df.empty:
                continue
                
            # Get consistent color and symbol for the team
            color = data_utils.get_team_color(team)
            symbol = data_utils.get_team_symbol(team)
            
            # Set size based on whether team is selected
            size = 16 if should_highlight and team in selected_teams else 12
            
            # Add trace with distinctive color and symbol
            fig.add_trace(go.Scatter(
                x=team_df["x"],
                y=team_df["y"],
                mode="markers",
                marker=dict(
                    color=color,
                    symbol=symbol,
                    size=size,
                    line=dict(width=2, color='#000000')  # Add thicker black outline for better visibility
                ),
                name=team,
                text=team,
                hovertemplate=f"<b>{team}</b><br>{x_col}: %{{x:.2f}}<br>{y_col}: %{{y:.2f}}<extra></extra>"
            ))
        
        # If no teams are available after filtering, show an empty plot with a message
        if len(teams_to_show) == 0:
            fig.add_annotation(
                text="No teams available for the selected tournament stage",
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

        return fig

    return dcc.Graph(
        id=ids.SCATTER_PLOT,
        config={'displayModeBar': True, 'scrollZoom': True},
        className="shadow-sm border rounded"
    )
