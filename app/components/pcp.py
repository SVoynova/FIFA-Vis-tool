"""
Enhanced Parallel Coordinates Plot (PCP) Component

This component creates a visually appealing parallel coordinates plot
to visualize and compare team performance across multiple metrics.
"""

from dash import Dash, dcc, html, Input, Output, callback, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os
import colorsys

from . import ids

# Define the data path relative to the app root
DATA_PATH = os.path.join('data', 'cleaned')  # Path to the data folder

# Utility functions
def load_team_data():
    """Load team data from CSV file"""
    try:
        file_path = os.path.join(DATA_PATH, "team_data_clean.csv")
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error loading team data: {e}")
        return None

def generate_distinct_colors(n):
    """Generate n visually distinct colors"""
    hsv_colors = [(i/n, 0.9, 0.9) for i in range(n)]
    rgb_colors = [colorsys.hsv_to_rgb(h, s, v) for h, s, v in hsv_colors]
    # Convert to rgba with 0.85 alpha
    rgba_colors = [f'rgba({int(r*255)},{int(g*255)},{int(b*255)},0.85)' for r, g, b in rgb_colors]
    return rgba_colors

def render(app: Dash) -> html.Div:
    @callback(
        Output(ids.PCP, "figure"),
        [Input(ids.TEAMS_DROPDOWN, "value"),
         Input(ids.SCATTER_PLOT, "selectedData"),
         Input(ids.CLEAR_PCP_BUTTON, "n_clicks")]
    )
    def update_pcp(selected_teams, selected_data, n_clicks):
        # Load the data
        df = load_team_data()
        
        if df is None:
            return go.Figure().update_layout(
                title="Error loading data",
                xaxis_title="Error",
                yaxis_title="Error"
            )
            
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
        
        # Define the attributes for the PCP - ordered by logical flow
        attributes = [
            'possession', 
            'passes_pct',
            'passes_pct_short', 
            'passes_pct_medium', 
            'passes_pct_long',
            'shots_per90', 
            'goals_per90', 
            'assists_per90', 
            'tackles_interceptions', 
            'gk_save_pct'
        ]
        
        # Nice labels for attributes with units
        labels = {
            'possession': 'Possession (%)',
            'passes_pct': 'Pass Completion (%)',
            'passes_pct_short': 'Short Pass (%)',
            'passes_pct_medium': 'Medium Pass (%)',
            'passes_pct_long': 'Long Pass (%)',
            'shots_per90': 'Shots per 90',
            'goals_per90': 'Goals per 90',
            'assists_per90': 'Assists per 90',
            'tackles_interceptions': 'Tackles + Int.',
            'gk_save_pct': 'Save (%)'
        }
        
        # Filter data to only include columns we need
        available_attrs = [col for col in attributes if col in df.columns]
        if len(available_attrs) == 0:
            return go.Figure().update_layout(
                title="Error: No matching columns found in dataset",
                height=600
            )
            
        # Create a filtered dataframe
        plot_df = df[['team'] + available_attrs].copy()
        plot_df = plot_df.fillna(0)
        
        # Create a color array for teams
        if combined_teams:
            # Generate distinct colors for selected teams
            team_colors = generate_distinct_colors(len(combined_teams))
            color_dict = {team: team_colors[i] for i, team in enumerate(combined_teams)}
            
            # Set color values - numerical 0 for non-selected teams, 1-len for selected (for color mapping)
            color_array = []
            for team in plot_df['team']:
                if team in combined_teams:
                    # Index in the combined_teams list + 1 (to start at 1, not 0)
                    color_array.append(combined_teams.index(team) + 1)
                else:
                    color_array.append(0)  # 0 for non-selected teams
                    
            # Create a colorscale that maps 0 to very light gray
            # and 1 through len(combined_teams) to distinct colors
            colorscale = [[0, 'rgba(220,220,220,0.1)']]  # Very light gray for non-selected
            for i, team in enumerate(combined_teams):
                # Map (i+1)/len(combined_teams) to the team color
                colorscale.append([(i+1)/len(combined_teams), color_dict[team]])
        else:
            # Default color array - all teams medium gray
            color_array = [1] * len(plot_df)
            colorscale = [[0, 'rgba(80,80,80,0.7)'], [1, 'rgba(80,80,80,0.7)']]
        
        # Create dimensions list for the parallel coordinates
        dimensions = []
        for attr in available_attrs:
            min_val = plot_df[attr].min()
            max_val = plot_df[attr].max()
            
            # Add a small buffer to the range
            buffer = (max_val - min_val) * 0.05 if max_val > min_val else 0.1
            
            # Use a format appropriate for the metric
            tick_format = '.0f'  # Default format
            if 'pct' in attr:
                tick_format = '.0f'  # Integer percentage
            elif 'per90' in attr:
                tick_format = '.2f'  # Two decimal places for per90 stats
                
            dimensions.append(
                dict(
                    range=[min_val - buffer, max_val + buffer],
                    label=labels.get(attr, attr.replace('_', ' ').title()),
                    values=plot_df[attr].tolist(),
                    tickformat=tick_format
                )
            )
        
        # Create the figure with a single trace
        fig = go.Figure(data=
            go.Parcoords(
                line=dict(
                    color=color_array,
                    colorscale=colorscale,
                    showscale=False,
                ),
                dimensions=dimensions,
                labelangle=30,
                labelfont=dict(size=14, family="Arial", color="#ffffff"),
                tickfont=dict(size=11, family="Arial", color="#dddddd")
            )
        )
        
        # Add a team selector legend
        legend_items = []
        if combined_teams:
            legend_items = []
            for i, team in enumerate(combined_teams[:15]):  # Limit to 15 teams
                color = color_dict[team]
                legend_items.append(
                    html.Div([
                        html.Div(style={
                            "backgroundColor": color,
                            "width": "15px",
                            "height": "15px",
                            "display": "inline-block",
                            "marginRight": "5px",
                            "verticalAlign": "middle"
                        }),
                        html.Span(team, style={"color": "white", "fontSize": "12px"})
                    ], style={"marginBottom": "3px", "marginRight": "10px", "display": "inline-block"})
                )
                
            if len(combined_teams) > 15:
                legend_items.append(
                    html.Div(f"... and {len(combined_teams) - 15} more teams", 
                             style={"color": "white", "fontSize": "12px", "marginTop": "5px"})
                )
        
        # Create legend title
        if combined_teams:
            legend_title = f"Selected Teams ({len(combined_teams)})"
        else:
            legend_title = "All Teams"
            
        # Update layout with improved styling
        fig.update_layout(
            title={
                'text': "Team Performance Comparison",
                'y': 0.98,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 24, 'color': 'white'}
            },
            plot_bgcolor='rgba(25,25,25,1)',   # Dark background
            paper_bgcolor='rgba(25,25,25,1)',  # Dark background
            height=750,  # Taller for better visibility
            margin=dict(l=100, r=100, t=120, b=80),
        )
        
        return fig
        
    @callback(
        Output("pcp-info", "children"),
        [Input(ids.TEAMS_DROPDOWN, "value"),
         Input(ids.SCATTER_PLOT, "selectedData")]
    )
    def update_pcp_info(selected_teams, selected_data):
        # Count teams from dropdown
        dropdown_count = len(selected_teams) if selected_teams else 0
        
        # Count teams from scatter plot
        scatter_count = 0
        unique_teams = set()
        if selected_data and 'points' in selected_data:
            for point in selected_data['points']:
                if 'customdata' in point and len(point['customdata']) > 0:
                    team = point['customdata'][0]
                    if team not in unique_teams:
                        unique_teams.add(team)
                        scatter_count += 1
        
        # Determine total unique teams
        total_unique = 0
        if dropdown_count > 0 and scatter_count > 0:
            # Calculate overlap
            if selected_teams:
                scatter_teams = list(unique_teams)
                total_unique = len(set(selected_teams).union(set(scatter_teams)))
            else:
                total_unique = scatter_count
        else:
            total_unique = dropdown_count + scatter_count
            
        # Create info text
        if total_unique == 0:
            return "No teams selected. Use the dropdown above or click points on the scatter plot to select teams."
        elif total_unique == 1:
            return f"1 team selected"
        else:
            return f"{total_unique} teams selected"
    
    # Callback to generate the legend display
    @callback(
        Output("pcp-legend", "children"),
        [Input(ids.TEAMS_DROPDOWN, "value"),
         Input(ids.SCATTER_PLOT, "selectedData")]
    )
    def update_legend(selected_teams, selected_data):
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
                
        # Generate distinct colors for teams
        if combined_teams:
            team_colors = generate_distinct_colors(len(combined_teams))
            
            # Build legend items
            legend_items = []
            for i, team in enumerate(combined_teams[:15]):  # Limit to 15 teams
                color = team_colors[i]
                legend_items.append(
                    html.Div([
                        html.Div(style={
                            "backgroundColor": color,
                            "width": "15px",
                            "height": "15px",
                            "display": "inline-block",
                            "marginRight": "5px",
                            "verticalAlign": "middle"
                        }),
                        html.Span(team, style={"fontSize": "12px"})
                    ], style={"marginBottom": "3px", "marginRight": "10px", "display": "inline-block"})
                )
                
            if len(combined_teams) > 15:
                legend_items.append(
                    html.Div(f"... and {len(combined_teams) - 15} more teams", 
                             style={"fontSize": "12px", "marginTop": "5px"})
                )
                
            return html.Div([
                html.H6(f"Selected Teams ({len(combined_teams)})", className="mb-2"),
                html.Div(legend_items, style={
                    "display": "flex", 
                    "flexWrap": "wrap", 
                    "maxWidth": "100%"
                })
            ])
        else:
            return html.Div([
                html.H6("No Teams Selected", className="mb-2"),
                html.P("Use the dropdown above or click points on the scatter plot to select teams.")
            ])
    
    return html.Div(
        children=[
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        id=ids.PCP, 
                        figure={},
                        config={'displayModeBar': False},
                        style={"backgroundColor": "#191919"}
                    ),
                ], width=12),
                dbc.Col([
                    dbc.Button("Clear Selection", id=ids.CLEAR_PCP_BUTTON, 
                              color="danger", className="mt-3 mb-2"),
                    html.Div(id="pcp-info", className="text-muted mt-2", 
                            style={"fontSize": "0.9rem"})
                ], width=12, className="text-center"),
                dbc.Col([
                    html.Div(id="pcp-legend", className="mt-3 mb-2",
                            style={"backgroundColor": "#f8f9fa", 
                                  "padding": "10px",
                                  "borderRadius": "5px"})
                ], width=12)
            ])
        ],
        style={"backgroundColor": "#191919", "padding": "15px", "borderRadius": "10px"}
    )