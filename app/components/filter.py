from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from . import ids

def render(app: Dash) -> html.Div:
    # Define filter options with user-friendly labels
    filter_options = [
        {"label": "All Teams", "value": 0},
        {"label": "Group Stage", "value": 1},
        {"label": "Round of 16", "value": 2},
        {"label": "Quarter Finals", "value": 3},
        {"label": "Semi Finals", "value": 4},
        {"label": "Third Place", "value": 5},
        {"label": "Finals", "value": 6},
    ]
    
    return html.Div([
        dbc.Label("Filter by Tournament Stage", className="fw-bold mb-1"),
        dcc.Dropdown(
            id=ids.FILTER,
            options=filter_options,
            value=0,
            clearable=False,
            style={"width": "100%", "font-size": "14px"},
            className="custom-dropdown"
        )
    ])
