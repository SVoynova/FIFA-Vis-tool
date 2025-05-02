from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from . import x_axis_dropdown, y_axis_dropdown, filter, search_bar, scatter_plot
from . import ids

def create_layout(app: Dash) -> dbc.Container:
    return dbc.Container(
        fluid=True,
        children=[
            dbc.Row([
                dbc.Col(html.H1("FIFA Visual Analysis", className="text-center my-4"), width=12)
            ]),

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
            ])
        ]
    )
