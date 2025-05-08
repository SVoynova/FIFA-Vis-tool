import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

DATA_PATH = os.path.join('data', 'cleaned') 
file_path = os.path.join(DATA_PATH, "team_performance_scores.csv")
df = pd.read_csv(file_path)

# Radar chart dimensions
dimensions = ['Offensive', 'Defensive', 'Cohesion', 'Efficiency', 'Discipline']

# Dash app setup
app = Dash(__name__)
app.title = "FIFA 2022 Multi-Team Radar Comparison"

# App layout
app.layout = html.Div([
    html.H1("FIFA World Cup 2022 - Team Performance Radar Comparison"),

    html.Label("Select Teams to Compare"),
    dcc.Dropdown(
        id='team-dropdown',
        options=[{'label': team, 'value': team} for team in sorted(df['team'])],
        multi=True,
        value=[df['team'][0], df['team'][1]],  # Default: first two teams
        style={'width': '70%', 'margin-bottom': '30px'}
    ),

    dcc.Graph(id='radar-chart', style={'width': '100%', 'height': '700px'})
])

# Radar chart update callback
@app.callback(
    Output('radar-chart', 'figure'),
    Input('team-dropdown', 'value')
)
def update_radar_chart(selected_teams):
    fig = go.Figure()

    for team in selected_teams:
        row = df[df['team'] == team].iloc[0]
        values = [row[dim] for dim in dimensions]
        values.append(values[0])  # close the loop
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=dimensions + [dimensions[0]],
            fill='toself',
            name=team
        ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=True,
        title="Team Performance Radar Chart"
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
