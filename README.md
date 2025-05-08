# FIFA World Cup 2022 – Visualization Tool

An interactive visualization tool for analyzing match-level performance and dynamics in the FIFA World Cup 2022, focusing on identifying patterns, upsets, and team behavior across tournament stages.

## Project Structure

- `data/cleaned/` – Cleaned CSV files used in the project
- `scripts/` – Data cleaning and preparation scripts
- `app/` – Contains the Dash app and all components
- `requirements.txt` – Python dependencies
- `setup.sh` – Optional setup script to configure environment

## Python Version

This project requires **Python 3.11.5**.
It is recommended to use a virtual environment (e.g., `venv` or `conda`).

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SVoynova/FIFA-Vis-tool
   cd FIFA-Vis-tool
   ```

2. **Create and activate a virtual environment (recommended):**
   - Using `venv`:
     ```bash
     python3.11 -m venv env
     source env/bin/activate  # On Windows: env\Scripts\activate
     ```
   - Or using `conda`:
     ```bash
     conda create -n fifa-env python=3.11.5
     conda activate fifa-env
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare the data:**
   - Ensure the cleaned data files are present in `data/cleaned/`.
   - If not, run the scripts in the `scripts/` directory to generate them.

5. **Run the dashboard:**
   ```bash
   python app/main.py
   ```
   - The dashboard will be available at [http://127.0.0.1:8052/](http://127.0.0.1:8052/)

## Notes

- The dashboard uses Dash and Plotly for interactive visualizations.
- For best results, use the latest version of Chrome or Firefox.
- If you encounter issues with missing data, check the `data/cleaned/` directory and the scripts in `scripts/`.

## Final Checklist for GitHub

- [x] All code is committed and pushed.
- [x] `requirements.txt` is up to date.
- [x] README is clear and comprehensive.
- [x] No sensitive data or credentials are present.
- [x] The app runs without errors using the above instructions.
