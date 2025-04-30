# FIFA World Cup 2022 – Visualization Tool
An interactive visualisation tool for analysing match-level performance and dynamics in the FIFA World Cup 2022, focusing on identifying patterns, upsets, and team behaviour across tournament stages.
This repository contains a data visualization project for the FIFA World Cup 2022, based on cleaned player, team, and match datasets.

## 📁 Project Structure

- `data/cleaned/` – Cleaned CSV files used in the project
- `scripts/clean_data.py` – Script used to clean raw datasets
- `app/` – Contains the Dash app (to be developed)
- `requirements.txt` – Python dependencies
- `setup.sh` – Optional setup script to configure environment

## ⚙️ Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/SVoynova/FIFA-Vis-tool
cd FIFA-Vis-tool
python3 -m venv envs/fifa-env
source envs/fifa-env/bin/activate
pip install -r requirements.txt
