import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html
import dash_bootstrap_components as dbc
import os

from . import ids

def render(app):
    DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'cleaned')
    file_path = os.path.join(DATA_PATH, "player_performance_scores.csv")
    df = pd.read_csv(file_path)

    # Radar dimensions
    dimensions = [
        "Scoring Threat",
        "Chance Creation",
        "Build-up Play",
        "Defensive Workrate",
        "Discipline & Physical"
    ]

    return html.Div([
        html.Div([
            html.H2("Player Performance Radar", className="text-center mb-4"),
            html.P("Compare player performances across different attributes. Select multiple players to see their performance profiles side by side.", 
                  className="text-center text-muted mb-4")
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                html.Label("Select Players:", className="mb-2"),
                dcc.Dropdown(
                    id=ids.PLAYER_RADAR_DROPDOWN,
                    options=[
                        {'label': f"{row['player']} ({row['team']})", 'value': row['player']}
                        for _, row in df.iterrows()
                    ],
                    multi=True,
                    value=[df['player'].iloc[0]],
                    style={'width': '100%', 'margin-bottom': '20px'},
                    className="mb-3"
                ),
                html.Div([
                    html.Small("Tip: Select multiple players to compare their performance profiles", 
                             className="text-muted")
                ])
            ], width=12)
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id=ids.PLAYER_RADAR_CHART,
                    style={'height': '600px'},
                    config={'displayModeBar': True, 'displaylogo': False}
                )
            ], width=12)
        ])
    ], className="p-4 border rounded shadow-sm") 