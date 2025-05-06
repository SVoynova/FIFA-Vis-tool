"""
Main layout for the FIFA Visual Analysis dashboard
"""

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from . import x_axis_dropdown, y_axis_dropdown, filter, scatter_plot
from . import pcp, teams_dropdown, pcp_explanation, stats_summary
from . import player_radar_task2, team_radar_task2
from . import ids

def create_layout(app: Dash) -> dbc.Container:
    """Create the main layout for the dashboard"""
    return dbc.Container(
        fluid=True,
        children=[
            # Title section with FIFA World Cup branding
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Img(
                            src="https://digitalhub.fifa.com/transform/3a170fb3-b359-4bf7-840d-7427d51b7c0b/FWC22_Horizontal_WHITE?io=transform:fill&quality=75", 
                            height="60px",
                            className="me-3 d-inline-block"
                        ),
                        html.H1("FIFA World Cup 2022 Visual Analysis", className="text-center my-4 d-inline-block")
                    ], className="d-flex justify-content-center align-items-center")
                ], width=12)
            ], className="bg-fifa-primary py-3 mb-4 rounded shadow"),
            
            # Sticky team selector that follows the user when scrolling
            html.Div(
                dbc.Row([
                    dbc.Col([
                        html.H4("Select Teams to Analyze", className="text-center mb-2"),
                        html.Div(
                            teams_dropdown.render(app),
                            className="p-3 border rounded shadow bg-light"
                        )
                    ], width={"size": 10, "offset": 1})
                ], className="py-2"),
                className="sticky-top bg-white shadow-sm mb-4 py-2 border-bottom",
                style={
                    "position": "sticky",
                    "top": "0",
                    "zIndex": "1000"
                },
                id="sticky-header"
            ),
            
            # Horizontal divider
            dbc.Row([
                dbc.Col(html.Hr(), width=12)
            ], className="my-2"),

            # First section: Scatter plot and controls
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H2("Team Capability Comparison", className="text-center mb-3"),
                        html.P(
                            "Compare how teams perform across different metrics with this interactive scatter plot.",
                            className="text-muted text-center mb-4"
                        )
                    ], className="p-2")
                ], width=12)
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.H5("X-Axis", className="text-center"),
                    html.Div(
                    x_axis_dropdown.render(app),
                        className="p-2 border rounded shadow-sm bg-light"
                    )
                ], width=6),

                dbc.Col([
                    html.H5("Y-Axis", className="text-center"),
                    html.Div(
                        y_axis_dropdown.render(app),
                        className="p-2 border rounded shadow-sm bg-light"
                    )
                ], width=6),
            ], className="mb-3"),

            dbc.Row([
                dbc.Col([
                    html.H5("Filter", className="text-center"),
                    html.Div(
                        filter.render(app),
                        className="p-2 border rounded shadow-sm bg-light"
                    )
                ], width={"size": 6, "offset": 3}),
            ], className="mb-3"),

            dbc.Row([
                dbc.Col([
                    html.Div(
                        scatter_plot.render(app),
                        className="dash-graph"
                    )
                ], width=12)
            ]),
            
            # Horizontal divider
            dbc.Row([
                dbc.Col(html.Hr(), width=12)
            ], className="my-4"),
            
            # Second section: Parallel Coordinates Plot
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H2("Team Performance Comparison", className="text-center mb-3"),
                        html.P(
                            "Analyze multiple performance metrics simultaneously with this parallel coordinates plot.",
                            className="text-muted text-center mb-4"
                        )
                    ], className="p-2")
                ], width=12)
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.Div(
                        pcp_explanation.render(app),
                        className="d-flex justify-content-center"
                    )
                ], width=12, className="mb-3")
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.Div(
                        pcp.render(app),
                        className="dash-graph"
                    )
                ], width=12)
            ]),
            
            # Horizontal divider
            dbc.Row([
                dbc.Col(html.Hr(), width=12)
            ], className="my-4"),
            
            # Radar Charts section header
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H2("Performance Radar Comparisons", className="text-center mb-3"),
                        html.P(
                            "Visualize team and player performance with these detailed radar charts.",
                            className="text-muted text-center mb-4"
                        )
                    ], className="p-2")
                ], width=12)
            ]),
            
            # Team and Player Radar Charts side by side
            dbc.Row([
                # Team Radar Chart (left)
                dbc.Col([
                    html.Div(
                        team_radar_task2.render(app),
                        className="border rounded shadow-sm p-3 h-100 bg-light dash-graph"
                    )
                ], width=6),
                
                # Player Radar Chart (right)
                dbc.Col([
                    html.Div(
                        player_radar_task2.render(app),
                        className="border rounded shadow-sm p-3 h-100 bg-light dash-graph"
                    )
                ], width=6)
            ]),
            
            # Horizontal divider
            dbc.Row([
                dbc.Col(html.Hr(), width=12)
            ], className="my-4"),
            
            # Stats summary
            dbc.Row([
                dbc.Col([
                    html.Div(
                        stats_summary.render(app),
                        className="dash-graph"
                    )
                ], width=12)
            ]),
            
            # Footer with FIFA branding
            dbc.Row([
                dbc.Col([
                    html.Footer([
                        html.P("FIFA World Cup 2022™ Data Visualization Dashboard", className="text-center text-muted mb-1"),
                        html.P("Created for educational purposes only. Not affiliated with FIFA.", className="text-center text-muted small")
                    ], className="py-3 mt-3")
                ], width=12)
            ], className="mt-5 pt-3 border-top")
        ]
    )