import pandas as pd
import numpy as np
from pathlib import Path

# Paths
DATA_DIR = Path("data")
CLEAN_DIR = DATA_DIR / "cleaned"
TEAM_DATA_PATH = DATA_DIR / "team_data" / "team_data.csv"
MATCH_DATA_PATH = DATA_DIR / "match_data.csv"
PLAYER_DATA_DIR = DATA_DIR / "player_data"

CLEAN_DIR.mkdir(parents=True, exist_ok=True)

# === Load Data ===
team_df = pd.read_csv(TEAM_DATA_PATH)
match_df = pd.read_csv(MATCH_DATA_PATH)
player_files = [
    "player_defense.csv", "player_gca.csv", "player_keepers.csv",
    "player_keepersadv.csv", "player_misc.csv", "player_passing.csv",
    "player_passing_types.csv", "player_playingtime.csv",
    "player_possession.csv", "player_shooting.csv", "player_stats.csv"
]

# === Clean and combine Player Data ===

# Load and combine all player data
player_dfs = []
for file in player_files:
    file_path = PLAYER_DATA_DIR / file
    df = pd.read_csv(file_path)
    df['source_file'] = file  # track where it came from
    player_dfs.append(df)

player_df = pd.concat(player_dfs, ignore_index=True)

# Replace -1 with NaN
player_df.replace(-1, np.nan, inplace=True)

# Drop columns that are entirely missing
player_df.dropna(axis=1, how='all', inplace=True)

# === Extract numerical age in years from 'age' column (e.g., "32-094" → 32)
if 'age' in player_df.columns:
    player_df['age_years'] = player_df['age'].astype(str).str.split('-').str[0].astype(float)

# === Clean Team Data ===

# Replace -1 with NaN (invalid data)
team_df.replace(-1, np.nan, inplace=True)

# Drop columns with all missing values
team_df.dropna(axis=1, how='all', inplace=True)

# Drop irrelevant columns as per their report
columns_to_drop = ['minutes_per_start', 'progressive_passes']
team_df.drop(columns=[col for col in columns_to_drop if col in team_df.columns], inplace=True)

# === Clean Match Data ===

if 'score' in match_df.columns:
    # Remove penalty shootout info
    match_df['score'] = match_df['score'].astype(str).str.replace(r'\(.*\)', '', regex=True)

    # Split score safely into home and away columns
    score_split = match_df['score'].str.split('-', expand=True)

    if score_split.shape[1] == 2:
        valid_scores = score_split[0].notnull() & score_split[1].notnull()
        match_df.loc[valid_scores, 'score_home'] = score_split.loc[valid_scores, 0].str.strip().astype(int)
        match_df.loc[valid_scores, 'score_away'] = score_split.loc[valid_scores, 1].str.strip().astype(int)

# Drop columns with all missing values
match_df.dropna(axis=1, how='all', inplace=True)

# Replace 'IR Iran' with 'Iran' across all datasets
team_df['team'] = team_df['team'].replace({'IR Iran': 'Iran'})
match_df.replace({'IR Iran': 'Iran'}, inplace=True)
player_df['team'] = player_df['team'].replace({'IR Iran': 'Iran'})

# === Save Cleaned Versions ===
team_df.to_csv(CLEAN_DIR / "team_data_clean.csv", index=False)
match_df.to_csv(CLEAN_DIR / "match_data_clean.csv", index=False)
player_df.to_csv(CLEAN_DIR / "player_data_clean.csv", index=False)

print("Cleaning complete.")
print(f"Cleaned team data saved to: {CLEAN_DIR / 'team_data_clean.csv'}")
print(f"Cleaned match data saved to: {CLEAN_DIR / 'match_data_clean.csv'}")
print(f"Cleaned player data saved to: {CLEAN_DIR / 'player_data_clean.csv'}")