from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP
from components.layout import create_layout

app = Dash(__name__, external_stylesheets=[BOOTSTRAP])
app.title = "FIFA Visual Analysis"
app.layout = create_layout(app)

if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
