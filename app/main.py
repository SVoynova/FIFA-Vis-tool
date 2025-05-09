import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import os

from dash import dcc, html
from dash.dependencies import Input, Output
from app.components.layout import create_layout

# Initialize the Dash app with Bootstrap styling
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://use.fontawesome.com/releases/v5.15.4/css/all.css"
    ],
    suppress_callback_exceptions=True
)

# Set the app title
app.title = "FIFA World Cup 2022 Dashboard"

# Set the layout using the create_layout function from components/layout.py
app.layout = create_layout(app)

# Only run the server if this file is run directly
if __name__ == "__main__":
    app.run_server(debug=True, port=8052)