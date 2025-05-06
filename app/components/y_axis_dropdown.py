from dash import Dash, html, dcc
from . import ids

def render(app: Dash) -> html.Div:
    # Define options with user-friendly labels
    axis_options = [
        {"label": "Goals per 90 min", "value": "goals_per90"},
        {"label": "Assists per 90 min", "value": "assists_per90"},
        {"label": "Expected Assist (xA) per 90 min", "value": "xg_assist_per90"},
        {"label": "Shots per 90 min", "value": "shots_per90"}
    ]
    
    return html.Div([
        dcc.Dropdown(
            id=ids.Y_AXIS_DROPDOWN,
            options=axis_options,
            value="assists_per90",
            clearable=False,
            style={"width": "100%", "font-size": "14px"},
            className="custom-dropdown"
        )
    ])
