from dash import Dash, html, dcc
from . import ids
import pandas as pd

# Load team data once for dropdown values
TEAM_DATA = pd.read_csv("data/cleaned/team_data_clean.csv")

def render(app: Dash) -> html.Div:
    return html.Div([
        html.Label("Search teams to highlight:"),
        dcc.Dropdown(
            id=ids.SEARCH_BAR,
            options=[{"label": team, "value": team} for team in sorted(TEAM_DATA["team"].unique())],
            value=[],
            multi=True,
            placeholder="Select teams to highlight..."
        )
    ])
