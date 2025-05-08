from dash import Dash, html, dcc
from . import ids

def render(app: Dash) -> html.Div:
    # Define options with user-friendly labels
    axis_options = [
        {"label": "Goals per 90 min", "value": "goals_per90"},
        {"label": "Assists per 90 min", "value": "assists_per90"},
        {"label": "Expected Goals (xG) per 90 min", "value": "xg_per90"},
        {"label": "Non-Penalty xG per 90 min", "value": "npxg_per90"},
        {"label": "Expected Assists (xA) per 90 min", "value": "xg_assist_per90"},
        {"label": "Shots per 90 min", "value": "shots_per90"},
        {"label": "Shots on Target per 90 min", "value": "shots_on_target_per90"},
        {"label": "Possession %", "value": "possession"},
        {"label": "Pass Completion %", "value": "passes_pct"},
        {"label": "Short Pass %", "value": "passes_pct_short"},
        {"label": "Medium Pass %", "value": "passes_pct_medium"},
        {"label": "Long Pass %", "value": "passes_pct_long"},
        {"label": "Tackles + Interceptions", "value": "tackles_interceptions"},
        {"label": "Save %", "value": "gk_save_pct"},
        {"label": "Tackle Success %", "value": "dribble_tackles_pct"},
        {"label": "Dribble Success %", "value": "dribbles_completed_pct"},
        {"label": "Aerial Duels Won %", "value": "aerials_won_pct"},
        {"label": "Penalty Save %", "value": "gk_pens_save_pct"}
    ]
    
    return html.Div([
        dcc.Dropdown(
            id=ids.X_AXIS_DROPDOWN,
            options=axis_options,
            value="goals_per90",
            clearable=False,
            style={"width": "100%", "font-size": "14px"},
            className="custom-dropdown"
        )
    ])
