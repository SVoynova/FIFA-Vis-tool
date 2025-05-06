import pandas as pd

# Load the cleaned team data
team_df = pd.read_csv("C:/Users/zoli/Documents/Vis RESIT/Clean Data/team_data_clean.csv")

# Define metric groups for each dimension
categories = {
    'Offensive': ['goals_per90', 'xg_per90'],
    'Defensive': ['tackles', 'interceptions'],
    'Cohesion': ['possession', 'passes_pct'],
    'Efficiency': ['xg_net', 'xg_assist_per90'],
    'Discipline': ['cards_yellow', 'fouls', 'avg_age']
}

# Create a new DataFrame to store scores
team_scores = pd.DataFrame()
team_scores['team'] = team_df['team']

# Normalize metrics and compute average score per dimension
for category, metrics in categories.items():
    normalized = team_df[metrics].copy()
    for col in normalized.columns:
        col_min = team_df[col].min()
        col_max = team_df[col].max()
        if col_max > col_min:
            normalized[col] = (team_df[col] - col_min) / (col_max - col_min)
        else:
            normalized[col] = 0.5  # fallback if no variation
    team_scores[category] = normalized.mean(axis=1) * 9 + 1  # scale to 1–10

# Save the result
team_scores.to_csv("C:/Users/zoli/Documents/Vis RESIT/Clean Data/team_performance_scores.csv", index=False)
print("✅ team_performance_scores.csv has been created.")
