from dash import Dash, html, dcc
from . import ids

def render(app: Dash) -> html.Div:
    options = ['goals_per90', 'assists_per90', 'xg_per90', 'npxg_per90', 'shots_per90']
    return html.Div([
        html.Label("X axis"),
        dcc.Dropdown(
            id=ids.X_AXIS_DROPDOWN,
            options=[{"label": opt, "value": opt} for opt in options],
            value="goals_per90"
        )
    ])
