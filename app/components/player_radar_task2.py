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
file_path = os.path.join(DATA_PATH, "player_performance_scores.csv")
PLAYER_DATA = pd.read_csv(file_path)

# Radar dimensions (correct column names from the CSV file)
dimensions = [
    "Scoring Threat",
    "Chance Creation",
    "Build-up Play",
    "Defensive Workrate",
    "Discipline & Physical"
]

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
    """Create a player radar chart component"""
    
    # Create component layout
    layout = html.Div([
        html.H4("Player Performance Radar Comparison", className="text-center mb-3"),
        html.Div([
            html.Label("Select Players:", className="fw-bold mb-1"),
            dcc.Dropdown(
                id=ids.PLAYER_RADAR_TASK2_DROPDOWN,
                options=[],  # Empty options initially, will be populated by callback
                multi=True,
                value=[],
                style={'width': '100%', 'font-size': '14px'},
                placeholder="Select players to compare (filtered by selected teams)",
                className="custom-dropdown mb-2"
            ),
        ], className="px-2"),
        dbc.Spinner(
            dcc.Graph(
                id=ids.PLAYER_RADAR_TASK2_CHART,
                config={'displayModeBar': True},
                className="border rounded"
            ),
            color="primary",
            type="grow",
            size="sm"
        )
    ])
    
    # Callback to update player dropdown options based on selected teams
    @app.callback(
        Output(ids.PLAYER_RADAR_TASK2_DROPDOWN, 'options'),
        Output(ids.PLAYER_RADAR_TASK2_DROPDOWN, 'value'),
        Input(ids.TEAMS_DROPDOWN, 'value')
    )
    def update_player_dropdown(selected_teams):
        if not selected_teams or len(selected_teams) == 0:
            # If no teams selected, show all players
            options = [
                {'label': f"{row['player']} ({row['team']})", 'value': row['player']}
                for _, row in PLAYER_DATA.iterrows()
            ]
            # Default value: first player
            value = [PLAYER_DATA['player'].iloc[0]] if not PLAYER_DATA.empty else []
        else:
            # Filter players from selected teams
            filtered_players = PLAYER_DATA[PLAYER_DATA['team'].isin(selected_teams)]
            options = [
                {'label': f"{row['player']} ({row['team']})", 'value': row['player']}
                for _, row in filtered_players.iterrows()
            ]
            # Default value: first player from the filtered list
            value = [filtered_players['player'].iloc[0]] if not filtered_players.empty else []
        
        return options, value
    
    # Define callback for the radar chart
    @app.callback(
        Output(ids.PLAYER_RADAR_TASK2_CHART, 'figure'),
        Input(ids.PLAYER_RADAR_TASK2_DROPDOWN, 'value')
    )
    def update_radar(selected_players):
        fig = go.Figure()

        if not selected_players or len(selected_players) == 0:
            # Return empty figure if no players selected
            fig.update_layout(
                title="Select players to display their radar chart",
                title_x=0.5,
                paper_bgcolor='rgba(250, 250, 250, 0.9)',
                height=500
            )
            return fig

        # Number of players to display
        num_players = len(selected_players)
        
        # Create a list to store player data for ordering
        players_with_sizes = []
        
        # First, collect all player data and calculate radar size
        for player_name in selected_players:
            player_rows = PLAYER_DATA[PLAYER_DATA['player'] == player_name]
            
            if not player_rows.empty:
                row = player_rows.iloc[0]
                
                # Get the actual values from the dataframe for each dimension
                values = []
                for dim in dimensions:
                    if dim in row:
                        # Make sure data is numeric
                        val = pd.to_numeric(row[dim], errors='coerce')
                        if pd.isna(val):
                            val = 1.0  # Default if value is missing
                        values.append(val)
                    else:
                        # If dimension is missing, use default value
                        values.append(1.0)
                
                # Calculate approximate "size" of radar by summing values
                size = sum(values)
                players_with_sizes.append((player_name, size, row, values))
        
        # Sort players by radar size (smallest first, so they appear on top)
        players_with_sizes.sort(key=lambda x: x[1])
                
        # Add traces
        for idx, (player_name, size, row, values) in enumerate(players_with_sizes):
            # Close the loop by adding the first value again
            radar_values = values + [values[0]]
            
            # Use colorblind-friendly palette with cycling
            color_idx = idx % len(COLORBLIND_PALETTE)
            base_color = COLORBLIND_PALETTE[color_idx]
            
            # Set very transparent fill (opacity 0.2) to match reference image
            fill_opacity = 0.2
            
            # Create a display name that includes team in parentheses
            team = row['team']
            display_name = f"{player_name} ({team})"
            
            # Extract RGB components
            rgba_parts = base_color.replace('rgba(', '').replace(')', '').split(',')
            r, g, b = rgba_parts[0].strip(), rgba_parts[1].strip(), rgba_parts[2].strip()
            
            # Create fill and line colors
            fill_color = f"rgba({r},{g},{b},{fill_opacity})"
            line_color = f"rgba({r},{g},{b},1)"  # Full opacity for line
            
            # Add radar trace with visible lines and transparent fills
            fig.add_trace(go.Scatterpolar(
                r=radar_values,
                theta=dimensions + [dimensions[0]],
                fill='toself',
                name=display_name,
                line=dict(
                    color=line_color,
                    width=1.5
                ),
                fillcolor=fill_color,
                text=[f"{dim}: {val:.1f}" for dim, val in zip(dimensions, values)] + [""],
                hoverinfo="text+name"
            ))
            
            # Add dots at each point for better readability
            fig.add_trace(go.Scatterpolar(
                r=radar_values,
                theta=dimensions + [dimensions[0]],
                mode='markers',
                marker=dict(
                    symbol='circle',
                    size=6,
                    color=line_color,
                    line=dict(color='white', width=1)
                ),
                name=f"{display_name} (points)",
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
                yanchor="bottom", 
                y=-0.15,
                xanchor="center",
                x=0.5,
                bgcolor='rgba(255, 255, 255, 0.9)',
                bordercolor='rgba(0, 0, 0, 0.1)',
                borderwidth=1
            ),
            title="Player Performance Radar Chart",
            title_x=0.5,
            title_font=dict(size=15),
            margin=dict(t=50, l=40, r=40, b=100),
            height=550,
            paper_bgcolor='rgba(250, 250, 250, 0.9)'
        )

        return fig
    
    return layout 