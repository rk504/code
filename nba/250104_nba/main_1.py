import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# %% [code] {"execution":{"iopub.status.busy":"2025-01-03T19:48:27.416706Z","iopub.execute_input":"2025-01-03T19:48:27.417102Z","iopub.status.idle":"2025-01-03T19:48:27.932731Z","shell.execute_reply.started":"2025-01-03T19:48:27.417072Z","shell.execute_reply":"2025-01-03T19:48:27.931721Z"}}

# Load and prepare the data
file_path = '~/code/data/kaggle/input/basketball/csv/Games.csv'
game_data = pd.read_csv(file_path)
team_data = pd.read_csv('~/code/data/kaggle/input/basketball/csv/TeamHistories.csv')
# Reverse the rows of the DataFrame (to get most recent team names)
team_data_reversed = team_data.iloc[::-1].reset_index(drop=True)

team_data = team_data_reversed
print(team_data.head())
# %% [code] {"execution":{"iopub.status.busy":"2025-01-03T19:48:27.416706Z","iopub.execute_input":"2025-01-03T19:48:27.417102Z","iopub.status.idle":"2025-01-03T19:48:27.932731Z","shell.execute_reply.started":"2025-01-03T19:48:27.417072Z","shell.execute_reply":"2025-01-03T19:48:27.931721Z"}}
# Clean and standardize teamAbbrev
team_data['teamAbbrev'] = team_data['teamAbbrev'].str.strip().str.upper()

# Replace abbreviations, but leave CHA (Charlotte Hornets) untouched
team_data['teamAbbrev'] = team_data['teamAbbrev'].replace({'SEA': 'OKC', 'NOH': 'NOP', 'NJN': 'BKN', 'NOK': 'NOP'})

# Print the first few rows to check if replacements worked
print(team_data.head())

# Allowed team abbreviations
allowed_teams = [
    'ATL', 'BOS', 'BKN', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL',
    'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS'
]

# Step 1: Filter team_data to only include teams in allowed_teams
team_data_filtered = team_data[team_data['teamAbbrev'].isin(allowed_teams)]

# Filter team_data to keep only rows where 'yearActiveTill' >= 2023
# team_data_filtered = team_data[(team_data['yearActiveTill'] >= 2023) | team_data['yearActiveTill'].isna()]

# Print the filtered data
print(team_data_filtered)

# Number of rows and columns in the DataFrame
print(f'Rows: {team_data_filtered.shape[0]}, Columns: {team_data_filtered.shape[1]}')

# Sort by 'yearFounded' to keep the most recent instance
team_data_sorted = team_data_filtered.sort_values(by='yearFounded', ascending=False)

# Drop duplicates based on 'teamAbbrev' to keep only the most recent for each team
team_data_filtered = team_data_sorted.drop_duplicates(subset='teamAbbrev')

# Check the result
print(team_data_filtered)
print("Length of filtered team data:", len(team_data_filtered))
