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

def render(app: Dash, x_axis_dropdown_id=None, y_axis_dropdown_id=None) -> html.Div:
    """Render the parallel coordinates plot"""
    
    @callback(
        Output(ids.PCP, "figure"),
        [Input(ids.TEAMS_DROPDOWN, "value")] +
        ([Input(x_axis_dropdown_id, "value")] if x_axis_dropdown_id else []) +
        ([Input(y_axis_dropdown_id, "value")] if y_axis_dropdown_id else [])
    )
    def update_pcp(selected_teams, x_axis=None, y_axis=None):
        # Load the data
        df = load_team_data()
        colorblind_palette = team_radar_task2.COLORBLIND_PALETTE
        fig = go.Figure()
        attrs = [
            'possession', 'shots_per90', 'goals_per90', 'assists_per90',
            'passes_pct', 'passes_pct_short', 'passes_pct_medium', 'passes_pct_long',
            'tackles_interceptions', 'gk_save_pct'
        ]
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
        tick_formats = {
            'possession': '.1f', 'shots_per90': '.2f', 'goals_per90': '.2f',
            'assists_per90': '.2f', 'passes_pct': '.1f', 'passes_pct_short': '.1f',
            'passes_pct_medium': '.1f', 'passes_pct_long': '.1f', 'tackles_interceptions': '.1f', 'gk_save_pct': '.1f'
        }
        if not selected_teams or len(selected_teams) == 0:
            fig.add_annotation(
                text="Select teams above to visualize their performance",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=18, color="#666666")
            )
        else:
            selected_df = df[df['team'].isin(selected_teams)].copy()
            team_colors = {team: colorblind_palette[i % len(colorblind_palette)] for i, team in enumerate(selected_teams)}
            color_array = [i for i, team in enumerate(selected_df['team'])]
            colorscale = [[i / max(1, len(selected_df) - 1), team_colors[team]] for i, team in enumerate(selected_df['team'])]
            # Highlight style
            highlight_style = '<span style="color:#1a237e;font-weight:bold;text-shadow:0 0 6px #bbdefb;">{}</span>'
            # Create dimensions for PCP
            dimensions = []
            for attr in attrs:
                min_val = max(0, selected_df[attr].min() * 0.9)
                max_val = selected_df[attr].max() * 1.1
                tick_format = tick_formats.get(attr, '.1f')
                step = (max_val - min_val) / 5
                tick_values = [min_val + i * step for i in range(6)]
                # Highlight label if matches x_axis or y_axis
                label_html = labels.get(attr, attr.replace('_', ' ').title())
                if (x_axis and attr == x_axis) or (y_axis and attr == y_axis):
                    label_html = highlight_style.format(label_html)
                dimensions.append(
                    dict(
                        range=[min_val, max_val],
                        label=label_html,
                        values=selected_df[attr].tolist(),
                        tickvals=tick_values,
                        ticktext=[f"{v:.1f}" for v in tick_values],
                        tickformat=tick_format
                    )
                )
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
            x_positions = list(range(len(attrs)))
            for i, team in enumerate(selected_df['team']):
                team_row = selected_df[selected_df['team'] == team].iloc[0]
                team_color = team_colors[team]
                for j, attr in enumerate(attrs):
                    format_str = tick_formats.get(attr, '.1f')
                    value = team_row[attr]
                    formatted_value = f"{value:{format_str}}"
                    hover_text = f"<b>{team}</b><br>{labels[attr]}: {formatted_value}"
                    fig.add_trace(
                        go.Scatter(
                            x=[x_positions[j]],
                            y=[team_row[attr]],
                            mode="markers",
                            marker=dict(
                                color=team_color,
                                opacity=0,  # Invisible
                                size=15
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
                fig.add_trace(
                    go.Scatter(
                        x=[None],
                        y=[None],
                        mode='lines',
                        line=dict(
                            color=team_color,
                            width=4,
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