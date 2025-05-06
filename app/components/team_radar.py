import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html
import dash_bootstrap_components as dbc
import os

from . import ids

def render(app):
    DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'cleaned')
    file_path = os.path.join(DATA_PATH, "team_performance_scores.csv")
    df = pd.read_csv(file_path)

    # Radar chart dimensions
    dimensions = ['Offensive', 'Defensive', 'Cohesion', 'Efficiency', 'Discipline']

    return html.Div([
        html.Div([
            html.H2("Team Performance Radar", className="text-center mb-4"),
            html.P("Compare team performances across different aspects of the game. Select multiple teams to see their performance profiles side by side.", 
                  className="text-center text-muted mb-4")
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                html.Label("Select Teams to Compare:", className="mb-2"),
                dcc.Dropdown(
                    id=ids.TEAM_RADAR_DROPDOWN,
                    options=[{'label': team, 'value': team} for team in sorted(df['team'])],
                    multi=True,
                    value=[df['team'][0], df['team'][1]],  # Default: first two teams
                    style={'width': '100%', 'margin-bottom': '20px'},
                    className="mb-3"
                ),
                html.Div([
                    html.Small("Tip: Select multiple teams to compare their performance profiles", 
                             className="text-muted")
                ])
            ], width=12)
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id=ids.TEAM_RADAR_CHART,
                    style={'height': '600px'},
                    config={'displayModeBar': True, 'displaylogo': False}
                )
            ], width=12)
        ])
    ], className="p-4 border rounded shadow-sm") 