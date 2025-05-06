"""
PCP Explanation Component

This component provides an explanation for the Parallel Coordinates Plot (PCP).
"""

from dash import Dash, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from . import ids

def render(app: Dash) -> html.Div:
    """Create a collapsible explanation widget for the PCP chart"""
    
    explanation_text = html.Div([
        html.P([
            "A ", html.Strong("Parallel Coordinates Plot"), " visualizes multivariate data across several dimensions."
        ], className="lead"),
        html.P([
            "Each vertical axis represents a different metric, and each colored line represents a team. "
            "This allows us to compare multiple aspects of team performance at once."
        ]),
        html.P([
            html.Strong("How to read:"), 
            html.Ul([
                html.Li("Each axis shows a different performance metric"),
                html.Li("Lines represent teams, with each color corresponding to a specific team"),
                html.Li("Position along each axis represents the team's performance in that metric"),
                html.Li("Observe patterns by comparing how lines flow across axes"),
                html.Li("Crossing lines indicate different relative performance across metrics")
            ], className="mt-2")
        ])
    ])
    
    component = html.Div([
        dbc.Button(
            [
                html.I(className="fas fa-info-circle me-2"),
                "About Parallel Coordinates Plot"
            ],
            id=ids.PCP_EXPLANATION_BUTTON,
            color="info",
            outline=True,
            className="mb-2",
            style={"font-weight": "bold"}
        ),
        dbc.Collapse(
            dbc.Card(
                dbc.CardBody(explanation_text, className="text-dark"),
                className="border shadow-sm"
            ),
            id=ids.PCP_EXPLANATION_COLLAPSE,
            is_open=False,
        )
    ])
    
    @app.callback(
        Output(ids.PCP_EXPLANATION_COLLAPSE, "is_open"),
        Input(ids.PCP_EXPLANATION_BUTTON, "n_clicks"),
        State(ids.PCP_EXPLANATION_COLLAPSE, "is_open"),
    )
    def toggle_collapse(n_clicks, is_open):
        if n_clicks:
            return not is_open
        return is_open
    
    return component