import dash
from dash import html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1("Test Dashboard"),
    html.P("If you can see this, Dash is working!")
])

if __name__ == "__main__":
    app.run(debug=True, port=8052) 