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
from . import data_utils  # Import shared data utilities
from . import team_radar_task2  # Import to use the same color palette

# Define the data path relative to the app root
DATA_PATH = os.path.join('data', 'cleaned')  # Path to the data folder

# Utility functions
def load_team_data():
    """Load and prepare team data"""
    DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'cleaned')
    file_path = os.path.join(DATA_PATH, "team_data_clean.csv")
    
    # Load data
    df = pd.read_csv(file_path)
    
    # Select columns for PCP - using columns that actually exist in the dataset
    selected_columns = [
        'team', 
        'possession',               # Possession %
        'shots_per90',              # Shots per 90
        'goals_per90',              # Goals per 90
        'assists_per90',            # Assists per 90
        'passes_pct',               # Pass Completion %
        'passes_pct_short',         # Short Pass %
        'passes_pct_medium',        # Medium Pass %
        'passes_pct_long',          # Long Pass %
        'tackles_interceptions',    # Tackles + Interceptions
        'gk_save_pct',              # Save %
        'games'                     # Keep games for potential calculations
    ]
    
    # Filter to selected columns and remove any rows with NaN values
    df = df[selected_columns].dropna()
    
    return df

def render(app: Dash) -> html.Div:
    """Render the parallel coordinates plot"""
    
    @callback(
        Output(ids.PCP, "figure"),
        [Input(ids.TEAMS_DROPDOWN, "value")]
    )
    def update_pcp(selected_teams):
        # Load the data
        df = load_team_data()
        
        # Get the colorblind-friendly palette from the radar chart
        colorblind_palette = team_radar_task2.COLORBLIND_PALETTE
        
        # Create the figure
        fig = go.Figure()
        
        # Select attributes for the parallel coordinates - using columns that exist
        attrs = [
            'possession',               # Possession %
            'shots_per90',              # Shots per 90
            'goals_per90',              # Goals per 90
            'assists_per90',            # Assists per 90
            'passes_pct',               # Pass Completion %
            'passes_pct_short',         # Short Pass %
            'passes_pct_medium',        # Medium Pass %
            'passes_pct_long',          # Long Pass %
            'tackles_interceptions',    # Tackles + Interceptions
            'gk_save_pct'               # Save %
        ]
        
        # Labels for better readability
        labels = {
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
        
        # Set tick formats with appropriate precision
        tick_formats = {
            'possession': '.1f',
            'shots_per90': '.2f',
            'goals_per90': '.2f',
            'assists_per90': '.2f',
            'passes_pct': '.1f',
            'passes_pct_short': '.1f',
            'passes_pct_medium': '.1f',
            'passes_pct_long': '.1f',
            'tackles_interceptions': '.1f',
            'gk_save_pct': '.1f'
        }
        
        # Process the data based on team selection
        if not selected_teams or len(selected_teams) == 0:
            # No teams selected - show empty plot with prompt
            fig.add_annotation(
                text="Select teams above to visualize their performance",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=18, color="#666666")
            )
        else:
            # Filter for selected teams
            selected_df = df[df['team'].isin(selected_teams)].copy()
            
            # Prepare team color mapping using the colorblind palette
            team_colors = {}
            for i, team in enumerate(selected_teams):
                color_idx = i % len(colorblind_palette)
                team_colors[team] = colorblind_palette[color_idx]
            
            # Create color array for PCP lines based on team index
            color_array = list(range(len(selected_df)))
            # Create colorscale mapping team indices to their colors
            colorscale = [[i/len(selected_df), team_colors[team]] 
                          for i, team in enumerate(selected_df['team'])]
            
            # Create dimensions for PCP
            dimensions = []
            for attr in attrs:
                min_val = max(0, selected_df[attr].min() * 0.9)  # Prevent negative values
                max_val = selected_df[attr].max() * 1.1  # Add buffer
                tick_format = tick_formats.get(attr, '.1f')
                
                # Step size calculation for nice ticks
                step = (max_val - min_val) / 5  # 5 ticks
                
                # Generate tick values
                tick_values = [min_val + i * step for i in range(6)]
                
                # Create dimension specification
                dimensions.append(
                    dict(
                        range=[min_val, max_val],
                        label=labels.get(attr, attr.replace('_', ' ').title()),
                        values=selected_df[attr].tolist(),
                        tickvals=tick_values,
                        ticktext=[f"{v:.1f}" for v in tick_values],
                        tickformat=tick_format  # Using tickformat instead of tickfont
                    )
                )
            
            # Add the parallel coordinates trace
            fig.add_trace(
                go.Parcoords(
                    line=dict(
                        color=color_array,
                        colorscale=colorscale,
                        showscale=False
                    ),
                    dimensions=dimensions,
                    labelangle=0,
                    labelfont=dict(size=14, family="Arial", color="#333333"),
                    rangefont=dict(size=11, family="Arial", color="#666666"),
                )
            )
            
            # Add hidden individual scatter traces for each attribute to enable hover
            # They'll be positioned at the bottom of the plot and invisible
            x_positions = list(range(len(attrs)))
            
            for i, team in enumerate(selected_df['team']):
                team_row = selected_df[selected_df['team'] == team].iloc[0]
                team_color = team_colors[team]
                
                # For each attribute, add a hidden marker with hover text
                for j, attr in enumerate(attrs):
                    # Format the value based on the attribute
                    format_str = tick_formats.get(attr, '.1f')
                    value = team_row[attr]
                    formatted_value = f"{value:{format_str}}"
                    
                    # Create hover text showing team and all values
                    hover_text = f"<b>{team}</b><br>{labels[attr]}: {formatted_value}"
                    
                    # Add invisible scatter point for hover
                    fig.add_trace(
                        go.Scatter(
                            x=[x_positions[j]],
                            y=[team_row[attr]],
                            mode="markers",
                            marker=dict(
                                color=team_color,
                                opacity=0,  # Invisible
                                size=15     # Large hit area for hover
                            ),
                            hoverinfo="text",
                            hovertext=hover_text,
                            showlegend=False
                        )
                    )
            
            # Create a separate legend showing teams
            for i, team in enumerate(selected_teams):
                color_idx = i % len(colorblind_palette)
                team_color = colorblind_palette[color_idx]
                
                # Add a scatter trace just for the legend
                fig.add_trace(
                    go.Scatter(
                        x=[None], 
                        y=[None],
                        mode='lines',
                        line=dict(
                            color=team_color,
                            width=4,  # Make lines thick in legend
                        ),
                        name=team,
                        showlegend=True
                    )
                )
        
        # Update layout with white background and improved styling
        fig.update_layout(
            title={
                'text': "Team Performance Comparison",
                'y': 0.98,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 24, 'color': '#333333'}
            },
            plot_bgcolor='rgba(255,255,255,1)',   # White background
            paper_bgcolor='rgba(255,255,255,1)',  # White background
            height=700,  # Taller for better visibility
            margin=dict(l=80, r=80, t=100, b=100),  # Margins
            
            # Move legend outside and below the plot
            legend=dict(
                font=dict(size=14, color="#333333"),  # Larger, darker font
                orientation="h",
                yanchor="top",
                y=-0.12,  # Place below the plot
                xanchor="center",
                x=0.5,
                bordercolor='rgba(0, 0, 0, 0.2)',
                borderwidth=2,
                bgcolor='rgba(255, 255, 255, 0.95)'
            ),
            hovermode="closest"  # For better hover interaction
        )
        
        return fig
    
    # Generate legend content for selected teams
    @callback(
        Output("pcp-legend", "children"),
        [Input(ids.TEAMS_DROPDOWN, "value")]
    )
    def update_legend(selected_teams):
        if not selected_teams or len(selected_teams) == 0:
            return html.Div([
                html.H6("No Teams Selected", className="mb-2 text-center"),
                html.P("Select teams above to visualize them in the plot.", className="text-center text-muted")
            ])
        
        # Build legend items using consistent team colors
        legend_items = []
        for team in selected_teams[:15]:  # Limit to 15 teams for display
            color = data_utils.get_team_color(team)
            legend_items.append(
                html.Div([
                    html.Div(style={
                        "backgroundColor": color,
                        "width": "16px",
                        "height": "16px",
                        "display": "inline-block",
                        "marginRight": "8px",
                        "verticalAlign": "middle",
                        "borderRadius": "3px"
                    }),
                    html.Span(team, style={"fontSize": "14px"})
                ], style={"marginBottom": "4px", "marginRight": "15px", "display": "inline-block"})
            )
        
        # Add indicator if more teams are selected than shown
        if len(selected_teams) > 15:
            legend_items.append(
                html.Div(f"... and {len(selected_teams) - 15} more teams", 
                         style={"fontSize": "14px", "marginTop": "10px", "fontStyle": "italic"})
            )
        
        return html.Div([
            html.H6(f"Selected Teams ({len(selected_teams)})", className="text-center mb-3"),
            html.Div(legend_items, style={
                "display": "flex", 
                "flexWrap": "wrap", 
                "justifyContent": "center",
                "maxWidth": "100%"
            })
        ], className="bg-light p-3 rounded shadow-sm")
    
    # Create the main component
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.Div(id="pcp-legend", className="mb-3")
            ], width=12),
        ]),
        html.Div([
            dbc.Button(
                "Clear Selection",
                id=ids.CLEAR_PCP_BUTTON,
                color="secondary",
                size="sm",
                className="mb-3",
                style={"fontWeight": "bold"}
            ),
        ], className="text-center"),
        dbc.Spinner(
            dcc.Graph(
                id=ids.PCP, 
                className="border rounded shadow",
                config={'displayModeBar': True}
            ),
            color="primary",
            type="border",
        )
    ])