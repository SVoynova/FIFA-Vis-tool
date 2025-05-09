# FIFA World Cup 2022 Visualization Dashboard

An interactive data visualization dashboard for analyzing team and player performance during the FIFA World Cup 2022. This tool provides multiple coordinated views including scatter plots, parallel coordinates plots, and radar charts to explore patterns and insights across different tournament stages.

## Features

- **Interactive Scatter Plot**: Compare team metrics with customizable X and Y axes
- **Tournament Stage Filtering**: Filter teams by their progression in the tournament
- **Parallel Coordinates Plot**: Analyze multiple performance metrics simultaneously
- **Radar Charts**: Visualize team and player performance across standardized dimensions
- **Team Selection**: Select and compare specific teams across all visualizations

## Requirements

- Python 3.8 or higher
- Libraries: dash, dash-bootstrap-components, pandas, numpy, plotly

## Quick Start

1. **Clone or download the repository**

2. **Create and activate a virtual environment (optional but recommended)**
   ```
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install the required packages**
   ```
   pip install -r requirements.txt
   ```

4. **Run the dashboard using one of these methods:**
   
   - **Using the provided scripts:**
     - Windows: Double-click `run_dashboard.bat` or run it from the command line
     - macOS/Linux: Open terminal and run `./run_dashboard.sh` (you may need to make it executable with `chmod +x run_dashboard.sh`)
   
   - **Using Python directly:**
     ```
     python -m app.main
     ```

5. **Open your browser and navigate to**
   ```
   http://127.0.0.1:8052/
   ```

## Project Structure

- `app/` - Dashboard application code
  - `main.py` - Main entry point for the Dash application
  - `components/` - Modular dashboard components
    - `scatter_plot.py` - Team capability comparison scatter plot
    - `pcp.py` - Parallel coordinates plot for multi-dimensional comparison
    - `team_radar_task2.py` - Team performance radar chart
    - `player_radar_task2.py` - Player performance radar chart
    - `filter.py` - Tournament stage filter
    - Other component files...

- `data/cleaned/` - Preprocessed datasets
  - `team_data_clean.csv` - Team statistics and metrics
  - `player_performance_scores.csv` - Player performance data
  - `team_performance_scores.csv` - Team performance data

- `run_dashboard.bat` - Windows script to launch the dashboard
- `run_dashboard.sh` - macOS/Linux script to launch the dashboard

## Usage Guide

1. **Filter by Tournament Stage**: Use the dropdown to select tournament stages (Group Stage through Finals)
2. **Select Teams to Analyze**: Choose specific teams to focus on across all visualizations
3. **Explore Team Metrics**: Use the scatter plot's X and Y axis dropdowns to compare different metrics
4. **Compare Multi-dimensional Data**: Examine the parallel coordinates plot to see patterns across multiple metrics
5. **Analyze Radar Charts**: View standardized team and player performance dimensions

## Troubleshooting

- If you see a "No teams available" message, try changing the tournament stage filter to include more teams.
- Ensure all data files are present in the `data/cleaned/` directory.
- Package version conflicts can be resolved by using a clean virtual environment and installing from requirements.txt.
- For Windows users: If you get "ModuleNotFoundError", make sure you're running from the project root directory.

## Data Sources

The data is derived from official FIFA World Cup 2022 statistics and has been preprocessed for visualization purposes.

## License

This project is available under the MIT License - see the LICENSE file for details.

---

*Project created for Data Visualization course, TU Eindhoven, 2023-2024*
