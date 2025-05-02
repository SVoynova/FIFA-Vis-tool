"""
Teams Dropdown Component

This component provides a dropdown menu for selecting teams to highlight
in the Parallel Coordinates Plot (PCP).
"""

from dash import Dash, dcc, html, Input, Output, callback, ctx
import dash_bootstrap_components as dbc
import pandas as pd
import os

from . import ids

# Define the data path relative to the app root
DATA_PATH = os.path.join('data', 'cleaned')  # Path to the data folder

def load_teams():
    """Load teams from the team data CSV file"""
    try:
        file_path = os.path.join(DATA_PATH, "team_data_clean.csv")
        df = pd.read_csv(file_path)
        teams = df["team"].unique().tolist()
        teams.sort()
        return teams
    except Exception as e:
        print(f"Error loading teams from team_data_clean.csv: {e}")
        return []

def render(app: Dash) -> html.Div:
    """Render the teams dropdown component"""
    teams = load_teams()
    
    @callback(
        Output(ids.TEAMS_DROPDOWN, "value"),
        [Input(ids.SELECT_ALL_TEAMS, "n_clicks"),
         Input(ids.DESELECT_ALL_TEAMS, "n_clicks"),
         Input(ids.CLEAR_PCP_BUTTON, "n_clicks")]
    )
    def update_teams_selection(select_all_clicks, deselect_all_clicks, clear_clicks):
        if not ctx.triggered:
            return []
        
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        
        if button_id == ids.SELECT_ALL_TEAMS:
            return teams
        elif button_id == ids.DESELECT_ALL_TEAMS or button_id == ids.CLEAR_PCP_BUTTON:
            return []
        
        return []
    
    return html.Div(
        children=[
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id=ids.TEAMS_DROPDOWN,
                        options=[{"label": team, "value": team} for team in teams],
                        multi=True,
                        placeholder="Select teams to highlight",
                        value=[],
                        searchable=True,
                        clearable=True,
                        style={"width": "100%"}
                    )
                ], width=8),
                dbc.Col([
                    dbc.Button("Select All", id=ids.SELECT_ALL_TEAMS, color="primary", size="sm", className="me-2"),
                    dbc.Button("Deselect All", id=ids.DESELECT_ALL_TEAMS, color="secondary", size="sm")
                ], width=4, className="d-flex align-items-center")
            ])
        ]
    )