"""
Stats Summary Component

This component displays a table of statistics for the selected teams.
"""

from dash import Dash, html, dcc, Input, Output, callback, ctx
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import os

from . import ids

# Define the data path relative to the app root
DATA_PATH = os.path.join('data', 'cleaned')  # Path to the data folder

def load_team_data():
    """Load team data from CSV file"""
    try:
        file_path = os.path.join(DATA_PATH, "team_data_clean.csv")
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error loading team data: {e}")
        return None

def get_attribute_labels():
    """Get user-friendly labels for attributes"""
    return {
        'possession': 'Possession %',
        'shots_per90': 'Shots per 90',
        'goals_per90': 'Goals per 90',
        'assists_per90': 'Assists per 90',
        'passes_pct': 'Pass Completion %',
        'passes_pct_short': 'Short Pass %',
        'passes_pct_medium': 'Medium Pass %',
        'passes_pct_long': 'Long Pass %',
        'tackles_interceptions': 'Tackles + Interceptions',
        'gk_save_pct': 'Save %'
    }

def render(app: Dash) -> html.Div:
    @callback(
        Output("stats-summary", "children"),
        [Input(ids.TEAMS_DROPDOWN, "value"),
         Input(ids.SCATTER_PLOT, "selectedData")]
    )
    def update_stats_summary(selected_teams, selected_data):
        # Load data
        df = load_team_data()
        if df is None:
            return html.Div("Error loading data")
            
        # Process teams selected from scatter plot
        scatter_selected_teams = []
        if selected_data and 'points' in selected_data:
            for point in selected_data['points']:
                if 'customdata' in point and len(point['customdata']) > 0:
                    team = point['customdata'][0]
                    if team not in scatter_selected_teams:
                        scatter_selected_teams.append(team)
        
        # Combine teams from dropdown and scatter plot
        if selected_teams:
            combined_teams = list(selected_teams)
        else:
            combined_teams = []
            
        # Add scatter plot selected teams
        for team in scatter_selected_teams:
            if team not in combined_teams:
                combined_teams.append(team)
                
        if not combined_teams:
            return html.Div("Select teams to see comparative statistics")
            
        # Define key metrics for comparison
        metrics = [
            'possession', 
            'shots_per90', 
            'goals_per90', 
            'assists_per90', 
            'passes_pct', 
            'passes_pct_short', 
            'passes_pct_medium', 
            'passes_pct_long', 
            'tackles_interceptions', 
            'gk_save_pct'
        ]
        
        # Filter metrics based on what's available in the dataframe
        available_metrics = [metric for metric in metrics if metric in df.columns]
        
        # Get labels
        label_map = get_attribute_labels()
        
        # Create summary table
        table_header = [
            html.Thead(html.Tr([html.Th("Metric")] + [html.Th(team) for team in combined_teams]))
        ]
        
        table_rows = []
        for metric in available_metrics:
            row_cells = [html.Td(label_map.get(metric, metric.replace('_', ' ').title()))]
            for team in combined_teams:
                if team in df['team'].values:
                    value = df.loc[df['team'] == team, metric].values[0]
                    # Format based on metric type
                    if 'pct' in metric:
                        formatted_value = f"{value:.1f}%" if not pd.isna(value) else "N/A"
                    else:
                        formatted_value = f"{value:.2f}" if not pd.isna(value) else "N/A"
                    row_cells.append(html.Td(formatted_value))
                else:
                    row_cells.append(html.Td("N/A"))
            table_rows.append(html.Tr(row_cells))
                
        table_body = [html.Tbody(table_rows)]
        
        return dbc.Table(table_header + table_body, bordered=True, hover=True, striped=True, size="sm")
        
    return html.Div(
        children=[
            html.H5("Team Statistics Comparison", className="mt-4 mb-3"),
            html.Div(id="stats-summary")
        ]
    )