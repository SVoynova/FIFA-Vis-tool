"""
Teams Dropdown Component

This component provides a dropdown menu for selecting teams to highlight
in the Parallel Coordinates Plot (PCP).
"""

from dash import Dash, dcc, html, Input, Output, callback, ctx, no_update, callback_context, State
import dash_bootstrap_components as dbc
import pandas as pd
import os

from . import ids

# Define the data path relative to the app root
DATA_PATH = os.path.join('data', 'cleaned')  # Path to the data folder

# Keep track of previously filtered teams for comparison
previous_filtered_teams = []

def load_teams():
    """Load teams from the team data CSV file"""
    try:
        file_path = os.path.join(DATA_PATH, "team_data_clean.csv")
        df = pd.read_csv(file_path)
        teams = df["team"].unique().tolist()
        teams.sort()
        return teams
    except Exception as e:
        print(f"Error loading teams from team_data_clean.csv: {e}")
        return []

def render(app: Dash) -> html.Div:
    """Render the teams dropdown component"""
    all_teams = load_teams()
    
    # Main callback to update dropdown based on filtering
    @callback(
        [Output(ids.TEAMS_DROPDOWN, "options"),
         Output(ids.TEAMS_DROPDOWN, "value")],
        [Input(ids.FILTERED_TEAMS_STORE, "data"),
         Input(ids.DESELECT_ALL_TEAMS, "n_clicks"),
         Input(ids.CLEAR_PCP_BUTTON, "n_clicks")],
        [State(ids.TEAMS_DROPDOWN, "value")]
    )
    def update_teams_dropdown(filtered_teams, deselect_all_clicks, clear_clicks, current_selection):
        global previous_filtered_teams
        
        # Get the ID of what triggered this callback
        trigger = callback_context.triggered[0]['prop_id'].split('.')[0] if callback_context.triggered else None
        
        # Always update options to show current filtered teams 
        # (or all teams if no filter)
        teams_to_show = filtered_teams if filtered_teams else all_teams
        options = [{"label": team, "value": team} for team in teams_to_show]
        
        # If this was triggered by the filter changing
        if trigger == ids.FILTERED_TEAMS_STORE:
            # Check if we're going from a more restrictive to a less restrictive filter
            # (more teams in the new filter than the previous one)
            if len(filtered_teams) > len(previous_filtered_teams) and len(previous_filtered_teams) > 0:
                # We're showing more teams now - expand selection if "Select All" was previously used
                # Check if all previously available teams were selected
                all_selected = len(current_selection) > 0 and all(team in current_selection for team in previous_filtered_teams)
                if all_selected:
                    # If user had everything selected before, select everything now
                    previous_filtered_teams = filtered_teams.copy()
                    return options, filtered_teams
                else:
                    # Otherwise, just keep current selections that are still valid
                    previous_filtered_teams = filtered_teams.copy()
                    valid_selection = [team for team in current_selection if team in filtered_teams] 
                    return options, valid_selection
            else:
                # Filter became more restrictive or stayed the same
                previous_filtered_teams = filtered_teams.copy()
                valid_selection = [team for team in current_selection if team in filtered_teams]
                return options, valid_selection
        
        # Handle button actions
        elif trigger == ids.DESELECT_ALL_TEAMS or trigger == ids.CLEAR_PCP_BUTTON:
            previous_filtered_teams = filtered_teams.copy() if filtered_teams else all_teams.copy()
            return options, []
        
        # Initial load or other trigger
        previous_filtered_teams = filtered_teams.copy() if filtered_teams else all_teams.copy()
        valid_selection = [team for team in (current_selection or []) if team in teams_to_show]
        return options, valid_selection
    
    # Separate callback just for the "Select All" button to update filter and select all teams
    @callback(
        [Output(ids.FILTER, "value"),
         Output(ids.TEAMS_DROPDOWN, "value", allow_duplicate=True)],
        [Input(ids.SELECT_ALL_TEAMS, "n_clicks")],
        prevent_initial_call=True
    )
    def handle_select_all(n_clicks):
        return 0, all_teams
    
    return html.Div(
        children=[
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id=ids.TEAMS_DROPDOWN,
                        options=[{"label": team, "value": team} for team in all_teams],
                        multi=True,
                        placeholder="Select teams to display in the scatter plot and other visualizations",
                        value=[],
                        searchable=True,
                        clearable=True,
                        style={
                            "width": "100%",
                            "font-size": "16px",
                        },
                        className="custom-dropdown"
                    )
                ], width=12),
            ], className="mb-2"),
            dbc.Row([
                dbc.Col([
                    dbc.ButtonGroup([
                        dbc.Button(
                            "Select All", 
                            id=ids.SELECT_ALL_TEAMS, 
                            color="primary", 
                            size="sm", 
                            className="me-2",
                            style={"width": "120px", "font-weight": "bold"}
                        ),
                        dbc.Button(
                            "Deselect All", 
                            id=ids.DESELECT_ALL_TEAMS, 
                            color="secondary", 
                            size="sm",
                            style={"width": "120px", "font-weight": "bold"}
                        ),
                    ], className="d-flex justify-content-center")
                ], width=12, className="text-center")
            ])
        ]
    )