import pandas as pd

# Check player data
player_data = pd.read_csv('data/cleaned/player_performance_scores.csv')
print("Player performance columns:")
print(player_data.columns.tolist())
print("\nSample player data:")
print(player_data.head(3))

# Check team data
team_data = pd.read_csv('data/cleaned/team_performance_scores.csv')
print("\nTeam performance columns:")
print(team_data.columns.tolist())
print("\nSample team data:")
print(team_data.head(3)) 