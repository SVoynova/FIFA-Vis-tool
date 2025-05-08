"""
Enhanced Parallel Coordinates Plot (PCP) Component

This component creates a visually appealing parallel coordinates plot
to visualize and compare team performance across multiple metrics.
"""

from dash import Dash, dcc, html, Input, Output, callback, ctx, clientside_callback
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
                # Calculate actual data range for each attribute
                min_val = selected_df[attr].min()
                max_val = selected_df[attr].max()
                
                # Add padding to the range
                range_padding = (max_val - min_val) * 0.1
                range_min = max(0, min_val - range_padding)
                range_max = max_val + range_padding
                
                tick_format = tick_formats.get(attr, '.1f')
                
                # Create exactly 5 nicely spaced ticks using the actual data range
                tick_values = []
                for i in range(5):
                    tick_val = range_min + (range_max - range_min) * (i / 4)
                    tick_values.append(tick_val)
                
                # Format tick labels with appropriate precision
                formatted_ticks = [f"{v:.1f}" for v in tick_values]
                
                # Highlight label if matches x_axis or y_axis
                label_html = labels.get(attr, attr.replace('_', ' ').title())
                if (x_axis and attr == x_axis) or (y_axis and attr == y_axis):
                    label_html = f'<b>🔵 {label_html.upper()}</b>'
                
                dimensions.append(
                    dict(
                        range=[range_min, range_max],
                        label=label_html,
                        values=selected_df[attr].tolist(),
                        tickvals=tick_values,
                        ticktext=formatted_ticks,
                        tickformat=None
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
                    tickfont=dict(size=10, family="Arial", color="#333333")
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
            height=900,  # Taller for better visibility
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
        ([Input(y_axis_dropdown_id, "value")] if y_axis_dropdown_id else []) +
        [Input('parcats-plot', 'clickData')]
    )
    def update_parcats(selected_teams, x_axis=None, y_axis=None, click_data=None):
        df = load_team_data()
        if not selected_teams or len(selected_teams) == 0:
            return go.Figure()
            
        selected_df = df[df['team'].isin(selected_teams)].copy()
        
        # Define the attributes and their labels
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

        # Define meaningful categories for each metric
        def create_categories(series, metric):
            # Use quantile-based binning instead of fixed thresholds
            # This creates more evenly distributed categories based on actual data
            try:
                # Calculate quartiles (25%, 50%, 75%) to create 4 categories
                q1 = series.quantile(0.25)
                q2 = series.quantile(0.50) # median
                q3 = series.quantile(0.75)
                
                bins = [series.min() - 0.001, q1, q2, q3, series.max() + 0.001]
                
                # Create descriptive labels with actual value ranges
                labels = [
                    f'Low (<{q1:.1f})',
                    f'Below Avg ({q1:.1f}-{q2:.1f})',
                    f'Above Avg ({q2:.1f}-{q3:.1f})',
                    f'High (>{q3:.1f})'
                ]
                
                # Special formatting for percentage metrics
                if "pct" in metric or metric == "possession":
                    labels = [
                        f'Low (<{q1:.1f}%)',
                        f'Below Avg ({q1:.1f}%-{q2:.1f}%)',
                        f'Above Avg ({q2:.1f}%-{q3:.1f}%)',
                        f'High (>{q3:.1f}%)'
                    ]
                
                return pd.cut(series, bins=bins, labels=labels, include_lowest=True)
            except:
                # Fallback in case of error (e.g., all identical values)
                return series.astype(str)
        
        # STEP 1: Collect all category data first
        all_category_data = []
        category_names = []
        dimensions = []
        
        # Process the team dimension
        dimensions.append(dict(
            values=selected_df['team'].astype(str), 
            label='Team', 
            categoryorder='array', 
            categoryarray=[str(t) for t in selected_df['team'].tolist()]
        ))
        
        # Process each attribute dimension
        for attr in attrs:
            categorized_vals = create_categories(selected_df[attr], attr)
            all_category_data.append(categorized_vals)
            
            # Convert values to strings for Plotly
            str_vals = categorized_vals.astype(str)
            unique_vals = sorted([str(v) for v in categorized_vals.unique()])
            category_names.append(unique_vals)
            
            # Set the dimension label
            label_html = labels[attr]
            if (x_axis is not None and attr == x_axis) or (y_axis is not None and attr == y_axis):
                label_html = f'🔵 {label_html.upper()}'
            
            dimensions.append(dict(
                values=str_vals,
                label=label_html,
                categoryorder='array',
                categoryarray=unique_vals
            ))
        
        # STEP 2: Process click data to determine highlighting
        # Default: no highlighting - all teams get their normal colors
        colorblind_palette = team_radar_task2.COLORBLIND_PALETTE
        team_color_list = [colorblind_palette[i % len(colorblind_palette)] for i, team in enumerate(selected_df['team'])]
        
        # Get the clicked category info from click_data if it exists
        highlight_paths = False
        if click_data and 'points' in click_data and len(click_data['points']) > 0:
            point = click_data['points'][0]
            if 'curveNumber' in point and 'pointNumber' in point:
                # Get dimension index (subtract 1 because first dimension is team names)
                dim_idx = point['curveNumber'] - 1
                if dim_idx >= 0 and dim_idx < len(all_category_data):
                    # Get the category data for this dimension
                    cat_data = all_category_data[dim_idx]
                    cat_unique = category_names[dim_idx]
                    if 'label' in point:
                        clicked_category = point['label']
                    elif 'pointNumber' in point and point['pointNumber'] < len(cat_unique):
                        clicked_category = cat_unique[point['pointNumber']]
                    else:
                        clicked_category = None
                        
                    if clicked_category:
                        highlight_paths = True
                        # Create a high contrast effect instead of outlining
                        team_color_list = []
                        
                        # Create color list with highlighted and almost invisible paths
                        for i, (team, cat) in enumerate(zip(selected_df['team'], cat_data)):
                            base_color = colorblind_palette[i % len(colorblind_palette)]
                            if str(cat) == clicked_category:
                                # Keep vivid colors for highlighted paths
                                team_color_list.append(base_color)
                            else:
                                # Make non-highlighted paths almost invisible
                                team_color_list.append('rgba(220, 220, 220, 0.15)')
        
        # STEP 3: Create the Parcats plot
        parcats_trace = go.Parcats(
            dimensions=dimensions,
            line=dict(
                color=team_color_list, 
                shape='hspline'
            ),
            hoveron='category',
            arrangement='perpendicular',
            labelfont=dict(size=12, family="Courier New, monospace", color="#222"),
            bundlecolors=False,
            domain=dict(y=[0, 1])
        )
        
        # Create the figure with the parcats trace
        fig = go.Figure(parcats_trace)
        
        # Add explanation and reset button for highlighting
        if highlight_paths:
            # Add explanation annotation
            fig.add_annotation(
                text=f"<b>Showing paths through {clicked_category}</b> - Click anywhere to reset",
                xref="paper", yref="paper",
                x=0.5, y=1.08,
                showarrow=False,
                font=dict(size=12, color="#222"),
                bgcolor="rgba(255, 253, 150, 0.95)",
                bordercolor="#555",
                borderwidth=1,
                borderpad=4
            )
        else:
            # Add instruction annotation
            fig.add_annotation(
                text="Click on any category box to highlight related paths",
                xref="paper", yref="paper",
                x=0.5, y=1.08,
                showarrow=False,
                font=dict(size=12, color="#222"),
                bgcolor="rgba(220, 220, 255, 0.95)",
                bordercolor="#555",
                borderwidth=1,
                borderpad=4
            )
        
        # STEP 4: Update layout and add instructions
        fig.update_layout(
            title={
                'text': "Parallel Categories Plot (Binned Metrics)",
                'y': 0.98,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 22, 'color': '#333333'}
            },
            margin=dict(l=100, r=100, t=80, b=60),  # Increased left and right margins
            height=700,
            plot_bgcolor='#f5f5f5',
            paper_bgcolor='#f5f5f5',
            # Add padding between axes
            xaxis=dict(
                tickangle=45,  # Angle the labels
                automargin=True  # Automatically adjust margins
            ),
            # Enable click events
            clickmode='event'
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