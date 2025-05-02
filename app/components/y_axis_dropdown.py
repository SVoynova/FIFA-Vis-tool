from dash import Dash, html, dcc
from . import ids

def render(app: Dash) -> html.Div:
    options = ['goals_per90', 'assists_per90', 'xg_assist_per90', 'shots_per90']
    return html.Div([
        html.Label("Y axis"),
        dcc.Dropdown(
            id=ids.Y_AXIS_DROPDOWN,
            options=[{"label": opt, "value": opt} for opt in options],
            value="assists_per90"
        )
    ])
