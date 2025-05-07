import pandas as pd
import plotly.graph_objects as go
import os
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from . import ids
from . import data_utils  # Import shared data utilities

# Load data
DATA_PATH = os.path.join('data', 'cleaned') 
file_path = os.path.join(DATA_PATH, "team_performance_scores.csv")
TEAM_DATA = pd.read_csv(file_path)

# Radar chart dimensions (correct column names from the CSV file)
dimensions = ['Offensive', 'Defensive', 'Cohesion', 'Efficiency', 'Discipline']

# Colorblind-friendly palette (using Set2 from ColorBrewer)
COLORBLIND_PALETTE = [
    'rgba(102, 194, 165, 1)', # teal
    'rgba(252, 141, 98, 1)',  # salmon
    'rgba(141, 160, 203, 1)', # blue-purple
    'rgba(231, 138, 195, 1)', # pink
    'rgba(166, 216, 84, 1)',  # light green
    'rgba(255, 217, 47, 1)',  # yellow
    'rgba(229, 196, 148, 1)', # beige
    'rgba(179, 179, 179, 1)'  # gray
]

def render(app: Dash) -> html.Div:
    """Create a team radar chart component"""
    
    # Create component layout
    layout = html.Div([
        html.H4("Team Performance Radar Comparison", className="text-center mb-3"),
        html.Div([
            html.P(
                "Teams selected above will be displayed in this radar chart", 
                className="text-center fst-italic text-muted"
            )
        ], className="mb-2"),
        dbc.Spinner(
            dcc.Graph(
                id=ids.TEAM_RADAR_TASK2_CHART,
                config={'displayModeBar': True},
                className="border rounded"
            ),
            color="primary",
            type="grow",
            size="sm"
        )
    ])
    
    # Define callback for the radar chart to use the global team selector
    @app.callback(
        Output(ids.TEAM_RADAR_TASK2_CHART, 'figure'),
        Input(ids.TEAMS_DROPDOWN, 'value')
    )
    def update_radar_chart(selected_teams):
        fig = go.Figure()

        if not selected_teams or len(selected_teams) == 0:
            # If no teams selected, show a prompt
            fig.update_layout(
                title="Select teams above to display their radar chart",
                title_x=0.5,
                paper_bgcolor='rgba(250, 250, 250, 0.9)',
                height=500
            )
            return fig

        # Get the number of teams to display
        num_teams = len(selected_teams)
        
        # Create a list to store team data for ordering
        team_with_sizes = []
        
        # First, collect all team data and calculate radar size
        for team in selected_teams:
            team_data = TEAM_DATA[TEAM_DATA['team'] == team]
            if not team_data.empty:
                row = team_data.iloc[0]
                values = [row[dim] for dim in dimensions]
                # Calculate approximate "size" of radar by summing values
                size = sum(values)
                team_with_sizes.append((team, size, row))
        
        # Sort teams by radar size (smallest first, so they appear on top)
        team_with_sizes.sort(key=lambda x: x[1])
        
        # Now add traces in order from smallest to largest
        for idx, (team, size, row) in enumerate(team_with_sizes):
            values = [row[dim] for dim in dimensions]
            values.append(values[0])  # close the loop
            
            # Use colorblind-friendly palette with cycling
            color_idx = idx % len(COLORBLIND_PALETTE)
            base_color = COLORBLIND_PALETTE[color_idx]
            
            # Set very transparent fill (opacity 0.2) to match reference image
            fill_opacity = 0.2
            
            # Extract RGB components
            rgba_parts = base_color.replace('rgba(', '').replace(')', '').split(',')
            r, g, b = rgba_parts[0].strip(), rgba_parts[1].strip(), rgba_parts[2].strip()
            
            # Create fill and line colors
            fill_color = f"rgba({r},{g},{b},{fill_opacity})"
            line_color = f"rgba({r},{g},{b},1)"  # Full opacity for line
            
            # Add radar trace with visible lines and transparent fills
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=dimensions + [dimensions[0]],
                fill='toself',
                name=team,
                line=dict(
                    color=line_color,
                    width=1.5
                ),
                fillcolor=fill_color,
                text=[f"{dim}: {val:.1f}" for dim, val in zip(dimensions, values[:-1])] + [""],
                hoverinfo="text+name"
            ))
            
            # Add dots at each point for better readability
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=dimensions + [dimensions[0]],
                mode='markers',
                marker=dict(
                    symbol='circle',
                    size=6,
                    color=line_color,
                    line=dict(color='white', width=1)
                ),
                name=f"{team} (points)",
                showlegend=False,
                hoverinfo="skip"
            ))

        # Configure layout to match reference image
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True, 
                    range=[0, 10],
                    tickfont=dict(size=11),
                    gridcolor='rgba(0,0,0,0.07)',
                    linecolor='rgba(0,0,0,0.1)'
                ),
                angularaxis=dict(
                    tickfont=dict(size=12, color='black'),
                    linecolor='rgba(0,0,0,0.1)',
                    gridcolor='rgba(0,0,0,0.04)'
                ),
                bgcolor='rgba(255, 255, 255, 1)'
            ),
            showlegend=True,
            legend=dict(
                font=dict(size=11),
                orientation="h",
                yanchor="top",
                y=-0.25,
                xanchor="center",
                x=0.5,
                bgcolor='rgba(255, 255, 255, 0.9)',
                bordercolor='rgba(0, 0, 0, 0.1)',
                borderwidth=1
            ),
            title="Team Performance Radar Chart",
            title_x=0.5,
            title_font=dict(size=15),
            margin=dict(t=50, l=40, r=40, b=180),
            height=550,
            paper_bgcolor='rgba(250, 250, 250, 0.9)'
        )

        return fig
    
    return layout 