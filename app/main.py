import dash
import dash_bootstrap_components as dbc

from app.components.layout import create_layout

# Initialize the Dash app with Bootstrap styling
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

# Set the app layout
app.layout = create_layout(app)

# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=8052)