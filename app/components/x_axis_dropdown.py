from dash import Dash, html, dcc
from . import ids

def render(app: Dash) -> html.Div:
    # Define options with user-friendly labels
    axis_options = [
        {"label": "Goals per 90 min", "value": "goals_per90"},
        {"label": "Assists per 90 min", "value": "assists_per90"},
        {"label": "Expected Goals (xG) per 90 min", "value": "xg_per90"},
        {"label": "Non-Penalty xG per 90 min", "value": "npxg_per90"},
        {"label": "Shots per 90 min", "value": "shots_per90"}
    ]
    
    return html.Div([
        dcc.Dropdown(
            id=ids.X_AXIS_DROPDOWN,
            options=axis_options,
            value="goals_per90",
            clearable=False,
            style={"width": "100%", "font-size": "14px"},
            className="custom-dropdown"
        )
    ])
