import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# Load player performance data
df = pd.read_csv("C:/Users/zoli/Documents/Vis RESIT/player_performance_scores2.csv")

# Radar dimensions (should match column names in your CSV)
dimensions = [
    "Scoring Threat",
    "Chance Creation",
    "Build-up Play",
    "Defensive Workrate",
    "Discipline & Physical"
]

# Initialize Dash app
app = Dash(__name__)
app.title = "FIFA 2022 Player Radar Chart"

# Layout
app.layout = html.Div([
    html.H1("FIFA World Cup 2022 - Player Radar Comparison"),

    html.Label("Select Players:"),
    dcc.Dropdown(
        id='player-dropdown',
        options=[
            {'label': f"{row['player']} ({row['team']})", 'value': row['player']}
            for _, row in df.iterrows()
        ],
        multi=True,
        value=[df['player'].iloc[0]],
        style={'width': '80%', 'margin-bottom': '20px'}
    ),

    dcc.Graph(id='radar-chart')
])

# Radar chart callback
@app.callback(
    Output('radar-chart', 'figure'),
    Input('player-dropdown', 'value')
)
def update_radar(selected_players):
    fig = go.Figure()

    for player in selected_players:
        row = df[df['player'] == player].iloc[0]
        values = [row[dim] for dim in dimensions]
        values.append(values[0])  # Close the radar loop

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=dimensions + [dimensions[0]],
            fill='toself',
            name=f"{row['player']} ({row['team']})"
        ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=True,
        title="Player Radar Chart"
    )

    return fig

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
