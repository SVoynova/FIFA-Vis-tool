import numpy as np
import pandas as pd
import plotly.express as px
import dash
from dash import Dash, dcc
from dash.dependencies import Input, Output
from . import ids

# Load cleaned team data
TEAM_DATA = pd.read_csv("data/cleaned/team_data_clean.csv")

# Add jitter to avoid overlapping points
JITTER_AMOUNT = 0.01
def add_jitter(series):
    return series + np.random.normal(0, JITTER_AMOUNT, len(series))

def render(app: Dash) -> dcc.Graph:
    @app.callback(
        Output(ids.SCATTER_PLOT, "figure"),
        Input(ids.X_AXIS_DROPDOWN, "value"),
        Input(ids.Y_AXIS_DROPDOWN, "value"),
        Input(ids.FILTER, "value"),
        Input(ids.SEARCH_BAR, "value"),
    )
    def update_scatter(x_col, y_col, filter_val, search_teams):
        df = TEAM_DATA.copy()
        df["x"] = add_jitter(df[x_col])
        df["y"] = add_jitter(df[y_col])

        use_symbols = "group" in df.columns

        fig = px.scatter(
            df,
            x="x",
            y="y",
            color="team",
            symbol="group" if use_symbols else None,
            hover_name="team",
            hover_data={x_col: True, y_col: True, "possession": False, "team": False},
            labels={"x": x_col, "y": y_col},
            color_discrete_sequence=px.colors.qualitative.Set2,
            title="Team Capability Comparison"
        )

        all_teams = TEAM_DATA["team"].unique().tolist()
        highlight = search_teams and len(search_teams) < len(all_teams)

        # Only enlarge if not all teams are selected
        for trace in fig.data:
            trace.marker.size = 18 if highlight and trace.name in search_teams else 10

        fig.update_layout(
            legend_title_text="Teams",
            title_x=0.5,
            margin=dict(t=50, l=20, r=20, b=40),
        )

        return fig

    return dcc.Graph(id=ids.SCATTER_PLOT)
