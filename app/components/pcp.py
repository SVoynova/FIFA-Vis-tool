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

def bin_column(series, bins=3, labels=None):
    # Bin a continuous column into categories
    if labels is None:
        labels = ["Low", "Medium", "High"][:bins]
    return pd.cut(series, bins=bins, labels=labels)

def bin_column_with_ranges(series, bins=3):
    # Bin a continuous column into value ranges (e.g., 10-20)
    binned, bin_edges = pd.cut(series, bins=bins, retbins=True)
    labels = []
    for i in range(len(bin_edges)-1):
        left = bin_edges[i]
        right = bin_edges[i+1]
        labels.append(f"{left:.1f}–{right:.1f}")
    return pd.cut(series, bins=bin_edges, labels=labels, include_lowest=True)

def render(app: Dash, x_axis_dropdown_id=None, y_axis_dropdown_id=None) -> html.Div:
    """Render the parallel coordinates plot and a parallel categories plot above it"""
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
            # PCP highlight style: prefix with '🔵' and bold using <b>...</b>
            highlight_style = '<b>🔵 {}</b>'
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
                    label_html = f'<b>🔵 {label_html.upper()}</b>'
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
        for team in selected_teams:
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
        
        return html.Div([
            html.H6(f"Selected Teams ({len(selected_teams)})", className="text-center mb-3"),
            html.Div(legend_items, style={
                "display": "flex", 
                "flexWrap": "wrap", 
                "justifyContent": "center",
                "maxWidth": "100%"
            })
        ], className="bg-light p-3 rounded shadow-sm")
    
    # --- Parallel Categories Plot ---
    @callback(
        Output('parcats-plot', 'figure'),
        [Input(ids.TEAMS_DROPDOWN, 'value')] +
        ([Input(x_axis_dropdown_id, "value")] if x_axis_dropdown_id else []) +
        ([Input(y_axis_dropdown_id, "value")] if y_axis_dropdown_id else [])
    )
    def update_parcats(selected_teams, x_axis=None, y_axis=None):
        df = load_team_data()
        if not selected_teams or len(selected_teams) == 0:
            return go.Figure()
        selected_df = df[df['team'].isin(selected_teams)].copy()
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
        # Use actual values (rounded) for each metric as categories
        def round_series(series):
            # Use 2 decimals for floats, int otherwise
            if pd.api.types.is_float_dtype(series):
                return series.round(2)
            return series
        # Build team-to-color mapping based on the order of selected_teams (same as PCP)
        colorblind_palette = team_radar_task2.COLORBLIND_PALETTE
        team_color_map = {team: colorblind_palette[i % len(colorblind_palette)] for i, team in enumerate(selected_teams)}
        team_color_list = [team_color_map[team] for team in selected_df['team']]
        # Build dimensions for parcats (convert all values to strings)
        dimensions = [
            dict(values=selected_df['team'].astype(str), label='Team', categoryorder='array', categoryarray=[str(t) for t in selected_df['team'].tolist()])
        ]
        for attr in attrs:
            rounded_vals = round_series(selected_df[attr]).astype(str)
            unique_vals = sorted(rounded_vals.unique())
            label_html = labels[attr]
            if (x_axis is not None and attr == x_axis) or (y_axis is not None and attr == y_axis):
                label_html = f'🔵 {label_html.upper()}'
            dimensions.append(dict(
                values=rounded_vals,
                label=label_html,
                categoryorder='array',
                categoryarray=unique_vals,
                ticktext=[str(v) for v in unique_vals]
            ))
        fig = go.Figure(
            go.Parcats(
                dimensions=dimensions,
                line=dict(color=team_color_list),
                hoveron='category',
                arrangement='freeform',
                labelfont=dict(size=14, family="Arial", color="#333333"),
                bundlecolors=False,
                domain=dict(y=[0, 1])
            )
        )
        fig.update_layout(
            title={
                'text': "Parallel Categories Plot (Binned Metrics)",
                'y': 0.98,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 22, 'color': '#333333'}
            },
            margin=dict(l=40, r=40, t=60, b=40),
            height=700,
            plot_bgcolor='rgba(255,255,255,1)',
            paper_bgcolor='rgba(255,255,255,1)'
        )
        return fig

    # --- Layout ---
    return html.Div([
        dcc.Graph(id='parcats-plot', className="mb-4 border rounded shadow-sm"),
        # (existing PCP legend, controls, and PCP plot below)
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