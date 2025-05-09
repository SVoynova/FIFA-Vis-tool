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
        [
            Input(ids.TEAMS_DROPDOWN, 'value'),
            Input(ids.FILTERED_TEAMS_STORE, 'data')
        ]
    )
    def update_player_dropdown(selected_teams, filtered_teams):
        # Start with all teams
        available_teams = set(PLAYER_DATA['team'].unique())
        
        # Filter by tournament stage if applicable
        if filtered_teams:
            available_teams = set(filtered_teams)
        
        # If no teams selected, show only players from teams that pass the tournament stage filter
        if not selected_teams or len(selected_teams) == 0:
            # Filter by tournament stage
            filtered_players = PLAYER_DATA[PLAYER_DATA['team'].isin(available_teams)]
            options = [
                {'label': f"{row['player']} ({row['team']})", 'value': row['player']}
                for _, row in filtered_players.iterrows()
            ]
            # Default value: empty selection
            value = []
        else:
            # Filter by selected teams AND tournament stage filter
            filtered_selected_teams = [team for team in selected_teams if team in available_teams]
            filtered_players = PLAYER_DATA[PLAYER_DATA['team'].isin(filtered_selected_teams)]
            options = [
                {'label': f"{row['player']} ({row['team']})", 'value': row['player']}
                for _, row in filtered_players.iterrows()
            ]
            # Default value: empty selection
            value = []
        
        return options, value
    
    # Define callback for the radar chart
    @app.callback(
        Output(ids.PLAYER_RADAR_TASK2_CHART, 'figure'),
        [
            Input(ids.PLAYER_RADAR_TASK2_DROPDOWN, 'value'),
            Input(ids.TEAMS_DROPDOWN, 'value'),
            Input(ids.FILTERED_TEAMS_STORE, 'data')
        ]
    )
    def update_radar(selected_players, selected_teams, filtered_teams):
        fig = go.Figure()
        
        # Start with a base filter of all teams
        available_teams = set(PLAYER_DATA['team'].unique())
        
        # Apply tournament stage filter if present
        if filtered_teams:
            available_teams = set(filtered_teams)
        
        # If there are teams selected, further filter to those teams
        if selected_teams and len(selected_teams) > 0:
            # Filter selected teams to only include those that match tournament stage
            filtered_team_selection = [team for team in selected_teams if team in available_teams]
            if filtered_team_selection:
                # If we have teams remaining after filtering
                available_teams = set(filtered_team_selection)
            else:
                # All selected teams were filtered out
                fig.add_annotation(
                    text="No selected teams available for the current tournament stage filter",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5,
                    showarrow=False,
                    font=dict(size=16, color="#666666")
                )
                fig.update_layout(
                    title="Tournament Stage Filter Applied",
                    title_x=0.5,
                    paper_bgcolor='rgba(250, 250, 250, 0.9)',
                    height=500
                )
                return fig
                
        # Check if we have players selected from the dropdown
        if selected_players and len(selected_players) > 0:
            # Filter to only include players from teams that match tournament stage
            filtered_player_data = PLAYER_DATA[PLAYER_DATA['team'].isin(available_teams)]
            
            # Further filter to selected players
            filtered_selected_players = filtered_player_data[filtered_player_data['player'].isin(selected_players)]
            
            # If we have matching players
            if not filtered_selected_players.empty:
                # Process players for radar chart
                radar_players = []
                for _, player_row in filtered_selected_players.iterrows():
                    values = [player_row[dim] for dim in dimensions]
                    radar_players.append((player_row['player'], sum(values), player_row, values))
                
                # Sort by radar size (smallest first)
                radar_players.sort(key=lambda x: x[1])
                
                # Add traces for each player
                for idx, (player_name, size, row, values) in enumerate(radar_players):
                    # Close the loop
                    radar_values = values + [values[0]]
                    
                    # Get color
                    color_idx = idx % len(COLORBLIND_PALETTE)
                    base_color = COLORBLIND_PALETTE[color_idx]
                    
                    # Set transparency
                    fill_opacity = 0.2
                    
                    # Extract RGB components
                    rgba_parts = base_color.replace('rgba(', '').replace(')', '').split(',')
                    r, g, b = rgba_parts[0].strip(), rgba_parts[1].strip(), rgba_parts[2].strip()
                    
                    # Create fill and line colors
                    fill_color = f"rgba({r},{g},{b},{fill_opacity})"
                    line_color = f"rgba({r},{g},{b},1)"
                    
                    # Create display name
                    team = row['team']
                    display_name = f"{player_name} ({team})"
                    
                    # Add radar trace
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
            else:
                # No players match both the selection and the tournament stage filter
                fig.add_annotation(
                    text="No players available for the selected teams and tournament stage",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5,
                    showarrow=False,
                    font=dict(size=16, color="#666666")
                )
        else:
            # Show a default message if no players selected
            fig.add_annotation(
                text="Select players from the dropdown to view radar chart",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=16, color="#666666")
            )
        
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