"""
PCP Explanation Component

This component provides an explanation for the Parallel Coordinates Plot (PCP).
"""

from dash import Dash, html
import dash_bootstrap_components as dbc

def render(app: Dash) -> html.Div:
    """Render the PCP explanation component"""
    # Dictionary of metric descriptions
    metric_descriptions = {
        'possession': "Percentage of time a team controls the ball during matches",
        'shots_per90': "Average number of shots taken per 90 minutes of play",
        'goals_per90': "Average number of goals scored per 90 minutes of play",
        'assists_per90': "Average number of assists provided per 90 minutes of play",
        'passes_pct': "Percentage of successful passes out of all attempted passes",
        'passes_pct_short': "Percentage of successful short passes out of all attempted short passes",
        'passes_pct_medium': "Percentage of successful medium passes out of all attempted medium passes",
        'passes_pct_long': "Percentage of successful long passes out of all attempted long passes",
        'tackles_interceptions': "Combined total of tackles and interceptions per match",
        'gk_save_pct': "Percentage of shots on target saved by the goalkeeper"
    }
    
    # Create list items for each metric
    metric_items = []
    for metric, description in metric_descriptions.items():
        display_name = metric.replace('_', ' ').title()
        if 'pct' in metric:
            display_name = display_name.replace('Pct', '%')
        if 'gk' in metric:
            display_name = display_name.replace('Gk', 'Goalkeeper')
        
        metric_items.append(html.Li([
            html.Strong(display_name), ": ", description
        ]))
    
    return html.Div(
        children=[
            dbc.Card(
                dbc.CardBody([
                    html.H5("About Parallel Coordinates Plot", className="card-title"),
                    html.P([
                        "A parallel coordinates plot allows you to compare multiple teams across different performance metrics. ",
                        "Each vertical axis represents a different metric, and each line represents a team."
                    ]),
                    html.P(["How to use this visualization:"]),
                    html.Ul([
                        html.Li("Select teams from the dropdown to highlight them in different colors"),
                        html.Li("You can also select teams by clicking on points in the scatter plot above"),
                        html.Li("Hover over lines to see detailed values for each metric"),
                        html.Li("Compare the performance patterns of different teams across all metrics"),
                        html.Li("Use the clear button to reset team selection")
                    ]),
                    html.P(["Metrics explained:"]),
                    html.Ul(metric_items, className="small")
                ])
            )
        ],
        className="mt-4 mb-4"
    )