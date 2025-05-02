"""
Main layout for the FIFA Visual Analysis dashboard
"""

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from . import x_axis_dropdown, y_axis_dropdown, filter, search_bar, scatter_plot
from . import pcp, teams_dropdown, pcp_explanation, stats_summary
from . import ids

def create_layout(app: Dash) -> dbc.Container:
    """Create the main layout for the dashboard"""
    return dbc.Container(
        fluid=True,
        children=[
            dbc.Row([
                dbc.Col(html.H1("FIFA Visual Analysis", className="text-center my-4"), width=12)
            ]),

            # First section: Scatter plot and controls
            dbc.Row([
                dbc.Col([
                    html.H5("Axis Selection"),
                    x_axis_dropdown.render(app),
                    y_axis_dropdown.render(app),
                ], width=3),

                dbc.Col([
                    html.H5("Highlight Teams"),
                    search_bar.render(app)
                ], width=5),

                dbc.Col([
                    html.H5("Filter"),
                    filter.render(app)
                ], width=4),
            ], className="mb-4"),

            dbc.Row([
                dbc.Col([
                    scatter_plot.render(app)
                ], width=12)
            ]),
            
            # Horizontal divider
            dbc.Row([
                dbc.Col(html.Hr(), width=12)
            ], className="my-4"),
            
            # Second section: Parallel Coordinates Plot
            dbc.Row([
                dbc.Col(html.H2("Team Performance Comparison", className="text-center mb-4"), width=12)
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.H5("Select Teams to Compare"),
                    teams_dropdown.render(app)
                ], width=8),
                dbc.Col([
                    pcp_explanation.render(app)
                ], width=4)
            ], className="mb-4"),
            
            dbc.Row([
                dbc.Col([
                    pcp.render(app)
                ], width=12)
            ]),
            
            # Stats summary
            dbc.Row([
                dbc.Col([
                    stats_summary.render(app)
                ], width=12)
            ])
        ]
    )