import pandas as pd

# Check team data only
team_data = pd.read_csv('data/cleaned/team_performance_scores.csv')
print("Team performance columns:")
for col in team_data.columns:
    print(f"- {col}")

print("\nFirst two rows of team data:")
for i, row in team_data.head(2).iterrows():
    print(f"Row {i}:")
    for col in team_data.columns:
        print(f"  {col}: {row[col]}") 