import pandas as pd

# Load all relevant datasets
shooting = pd.read_csv("C:/Users/zoli/Documents/Vis RESIT/JBI100 Data (2024-2025) RESIT/Data/FIFA World Cup 2022 Player Data/player_shooting.csv")
gca = pd.read_csv("C:/Users/zoli/Documents/Vis RESIT/JBI100 Data (2024-2025) RESIT/Data/FIFA World Cup 2022 Player Data/player_gca.csv")
passing = pd.read_csv("C:/Users/zoli/Documents/Vis RESIT/JBI100 Data (2024-2025) RESIT/Data/FIFA World Cup 2022 Player Data/player_passing.csv")
misc = pd.read_csv("C:/Users/zoli/Documents/Vis RESIT/JBI100 Data (2024-2025) RESIT/Data/FIFA World Cup 2022 Player Data/player_misc.csv")
defense = pd.read_csv("C:/Users/zoli/Documents/Vis RESIT/JBI100 Data (2024-2025) RESIT/Data/FIFA World Cup 2022 Player Data/player_defense.csv")
stats = pd.read_csv("C:/Users/zoli/Documents/Vis RESIT/JBI100 Data (2024-2025) RESIT/Data/FIFA World Cup 2022 Player Data/player_stats.csv")
possession = pd.read_csv("C:/Users/zoli/Documents/Vis RESIT/JBI100 Data (2024-2025) RESIT/Data/FIFA World Cup 2022 Player Data/player_possession.csv")

# Extract age as numeric from format like "31-123"
stats['age_clean'] = stats['age'].str.extract(r'(\d+)', expand=False).astype(float)

# Filter out goalkeepers
stats = stats[stats['position'] != 'GK']

# Start from core stats
df = stats[['player', 'team', 'age_clean', 'goals_per90', 'assists_per90', 'xg_per90', 'cards_yellow']].copy()

# Merge all other relevant metrics
df = df.merge(shooting[['player', 'team', 'shots_on_target_per90']], on=['player', 'team'], how='left')
df = df.merge(gca[['player', 'team', 'gca_per90', 'sca_per90']], on=['player', 'team'], how='left')
df = df.merge(passing[['player', 'team', 'passes_pct', 'progressive_passes', 'passes_into_final_third']], on=['player', 'team'], how='left')
df = df.merge(possession[['player', 'team', 'touches']], on=['player', 'team'], how='left')
df = df.merge(defense[['player', 'team', 'tackles', 'interceptions', 'clearances', 'blocks']], on=['player', 'team'], how='left')
df = df.merge(misc[['player', 'team', 'fouls', 'aerials_won_pct']], on=['player', 'team'], how='left')

# Rename age column
df.rename(columns={'age_clean': 'age'}, inplace=True)

# Drop players with less than 80% data availability across selected metrics
radar_metrics = [
    'goals_per90', 'xg_per90', 'shots_on_target_per90',
    'assists_per90', 'gca_per90', 'sca_per90', 'passes_into_final_third',
    'passes_pct', 'progressive_passes', 'touches',
    'tackles', 'interceptions', 'clearances', 'blocks',
    'cards_yellow', 'fouls', 'aerials_won_pct', 'age'
]
df = df[df[radar_metrics].notna().mean(axis=1) >= 0.8]

# Define radar dimensions
categories = {
    'Scoring Threat': ['goals_per90', 'xg_per90', 'shots_on_target_per90'],
    'Chance Creation': ['assists_per90', 'gca_per90', 'sca_per90', 'passes_into_final_third'],
    'Build-up Play': ['passes_pct', 'progressive_passes', 'touches'],
    'Defensive Workrate': ['tackles', 'interceptions', 'clearances', 'blocks'],
    'Discipline & Physical': ['cards_yellow', 'fouls', 'aerials_won_pct', 'age']
}

# Calculate scores on 1–10 scale
scores = df[['player', 'team']].copy()
for category, metrics in categories.items():
    normed = df[metrics].apply(pd.to_numeric, errors='coerce')
    normed = normed.apply(lambda x: (x - x.min()) / (x.max() - x.min()) if x.max() > x.min() else 0.5)
    scores[category] = normed.mean(axis=1) * 9 + 1

# Save output
scores.to_csv("C:/Users/zoli/Documents/Vis RESIT/player_performance_scores2.csv", index=False)
print("✅ player_performance_scores.csv has been created.")