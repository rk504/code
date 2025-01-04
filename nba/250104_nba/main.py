# %% [code] {"execution":{"iopub.status.busy":"2025-01-03T19:48:27.416706Z","iopub.execute_input":"2025-01-03T19:48:27.417102Z","iopub.status.idle":"2025-01-03T19:48:27.932731Z","shell.execute_reply.started":"2025-01-03T19:48:27.417072Z","shell.execute_reply":"2025-01-03T19:48:27.931721Z"}}
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# Download latest version - run this in AM if doing daily refresh
#import kagglehub

#path = kagglehub.dataset_download("eoinamoore/historical-nba-data-and-player-box-scores")
#data = /Users/reese/.cache/kagglehub/datasets/eoinamoore/historical-nba-data-and-player-box-scores/versions/45
#print("Path to dataset files:", path)

# %% [code] {"execution":{"iopub.status.busy":"2025-01-03T19:48:27.416706Z","iopub.execute_input":"2025-01-03T19:48:27.417102Z","iopub.status.idle":"2025-01-03T19:48:27.932731Z","shell.execute_reply.started":"2025-01-03T19:48:27.417072Z","shell.execute_reply":"2025-01-03T19:48:27.931721Z"}}

# Load and prepare the data
file_path = '~/code/data/kaggle/input/basketball/csv/Games.csv'
game_data = pd.read_csv(file_path)
team_data = pd.read_csv('~/code/data/kaggle/input/basketball/csv/TeamHistories.csv')
# Reverse the rows of the DataFrame (to get most recent team names)
team_data_reversed = team_data.iloc[::-1].reset_index(drop=True)

team_data = team_data_reversed


# %% [code] {"execution":{"iopub.status.busy":"2025-01-03T19:48:27.416706Z","iopub.execute_input":"2025-01-03T19:48:27.417102Z","iopub.status.idle":"2025-01-03T19:48:27.932731Z","shell.execute_reply.started":"2025-01-03T19:48:27.417072Z","shell.execute_reply":"2025-01-03T19:48:27.931721Z"}}
# Clean and standardize teamAbbrev
team_data['teamAbbrev'] = team_data['teamAbbrev'].str.strip().str.upper()

# Replace abbreviations
team_data['teamAbbrev'] = team_data['teamAbbrev'].replace({'SEA': 'OKC', 'NOH': 'NOP', 'NJN': 'BKN', 'NOK': 'NOP', 'GS': 'GSW'})

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
#team_data_filtered = team_data[(team_data['yearActiveTill'] >= 2023) | team_data['yearActiveTill'].isna()]
# Print the filtered data
print(team_data_filtered)
# Number of rows and columns in the DataFrame
print(f'Rows: {team_data_filtered.shape[0]}, Columns: {team_data_filtered.shape[1]}')


# %% [code] {"execution":{"iopub.status.busy":"2025-01-03T19:48:27.416706Z","iopub.execute_input":"2025-01-03T19:48:27.417102Z","iopub.status.idle":"2025-01-03T19:48:27.932731Z","shell.execute_reply.started":"2025-01-03T19:48:27.417072Z","shell.execute_reply":"2025-01-03T19:48:27.931721Z"}}
# Sort by 'yearFounded' to keep the most recent instance
team_data_sorted = team_data_filtered.sort_values(by='yearFounded', ascending=False)

# Drop duplicates based on 'teamAbbrev' to keep only the most recent for each team
team_data_filtered = team_data_sorted.drop_duplicates(subset='teamAbbrev')

# Check the result
print(team_data_filtered)

# %% [code] {"execution":{"iopub.status.busy":"2025-01-03T19:48:27.416706Z","iopub.execute_input":"2025-01-03T19:48:27.417102Z","iopub.status.idle":"2025-01-03T19:48:27.932731Z","shell.execute_reply.started":"2025-01-03T19:48:27.417072Z","shell.execute_reply":"2025-01-03T19:48:27.931721Z"}}

# Sort by 'yearFounded' to keep the most recent instance
team_data_sorted = team_data_filtered.sort_values(by='yearFounded', ascending=False)

# Drop duplicates based on 'teamAbbrev' to keep only the most recent for each team
team_data_filtered = team_data_sorted.drop_duplicates(subset='teamAbbrev')

# Show the length of the new DataFrame
print("Length of filtered team data:", len(team_data_filtered))

# Optionally, you can also print the shape (rows, columns) of the DataFrame
print("Shape of filtered team data:", team_data_filtered.shape)

# Check the result (optional)
print(team_data_filtered)


# %% [code] {"execution":{"iopub.status.busy":"2025-01-03T19:48:27.416706Z","iopub.execute_input":"2025-01-03T19:48:27.417102Z","iopub.status.idle":"2025-01-03T19:48:27.932731Z","shell.execute_reply.started":"2025-01-03T19:48:27.417072Z","shell.execute_reply":"2025-01-03T19:48:27.931721Z"}}
# Replace 'New Orleans Hornets' with 'New Orleans Pelicans'
team_data_filtered['teamAbbrev'] = team_data_filtered['teamAbbrev'].replace({'NOP': 'NOP'})

# Sort by 'yearFounded' to keep the most recent instance
team_data_sorted = team_data_filtered.sort_values(by='yearFounded', ascending=False)

# Drop duplicates based on 'teamAbbrev' to keep only the most recent for each team
team_data_filtered = team_data_sorted.drop_duplicates(subset='teamAbbrev')

# Show the length of the new DataFrame
print("Length of filtered team data:", len(team_data_filtered))

# Optionally, you can also print the shape (rows, columns) of the DataFrame
print("Shape of filtered team data:", team_data_filtered.shape)

# Check the result (optional)
print(team_data_filtered)

# Check unique team abbreviations in the filtered data
print("Unique team abbreviations in filtered data:", team_data_filtered['teamAbbrev'].unique())

# %% [code] {"execution":{"iopub.status.busy":"2025-01-03T19:48:27.416706Z","iopub.execute_input":"2025-01-03T19:48:27.417102Z","iopub.status.idle":"2025-01-03T19:48:27.932731Z","shell.execute_reply.started":"2025-01-03T19:48:27.417072Z","shell.execute_reply":"2025-01-03T19:48:27.931721Z"}}

# %% [code] {"execution":{"iopub.status.busy":"2025-01-03T19:48:27.416706Z","iopub.execute_input":"2025-01-03T19:48:27.417102Z","iopub.status.idle":"2025-01-03T19:48:27.932731Z","shell.execute_reply.started":"2025-01-03T19:48:27.417072Z","shell.execute_reply":"2025-01-03T19:48:27.931721Z"}}


# Convert 'gameDate' column to datetime, with errors='coerce' to handle invalid date formats
game_data['gameDate'] = pd.to_datetime(game_data['gameDate'], errors='coerce')

# Drop rows with invalid 'gameDate' (NaT values)
game_data = game_data.dropna(subset=['gameDate'])

# Extract only the date (year-month-day) part
game_data['gameDate'] = game_data['gameDate'].dt.date

# Filter games from the 2000-01 season onwards (year >= 2000)
game_data_filtered = game_data[game_data['gameDate'].apply(lambda x: x.year >= 2000)]

# Check the filtered data
print(game_data_filtered[['gameId', 'gameDate', 'hometeamCity', 'hometeamName', 'awayteamCity', 'awayteamName']])
# %% [code] {"execution":{"iopub.status.busy":"2025-01-03T19:48:27.416706Z","iopub.execute_input":"2025-01-03T19:48:27.417102Z","iopub.status.idle":"2025-01-03T19:48:27.932731Z","shell.execute_reply.started":"2025-01-03T19:48:27.417072Z","shell.execute_reply":"2025-01-03T19:48:27.931721Z"}}

# Convert game_date to datetime and select relevant columns
game_data_filtered['game_date'] = pd.to_datetime(game_data_filtered['gameDate'])
""" new_table = game_data[['team_abbreviation_home', 'game_date', 'plus_minus_home', 
                  'matchup_home', 'team_abbreviation_away', 'plus_minus_away']]
 """
# %% [code] {"execution":{"iopub.status.busy":"2025-01-03T19:48:27.416706Z","iopub.execute_input":"2025-01-03T19:48:27.417102Z","iopub.status.idle":"2025-01-03T19:48:27.932731Z","shell.execute_reply.started":"2025-01-03T19:48:27.417072Z","shell.execute_reply":"2025-01-03T19:48:27.931721Z"}}

# Merge home team abbreviations
game_data_filtered = pd.merge(game_data_filtered, team_data[['teamId', 'teamAbbrev']], left_on='hometeamId', right_on='teamId', how='left')
game_data_filtered = game_data_filtered.rename(columns={'teamAbbrev': 'hometeamAbbrev'}).drop(columns=['teamId'])

# Merge away team abbreviations
game_data_filtered = pd.merge(game_data_filtered, team_data[['teamId', 'teamAbbrev']], left_on='awayteamId', right_on='teamId', how='left')
game_data_filtered = game_data_filtered.rename(columns={'teamAbbrev': 'awayteamAbbrev'}).drop(columns=['teamId'])

print(game_data_filtered[['gameId', 'hometeamCity', 'hometeamName', 'hometeamAbbrev', 'awayteamCity', 'awayteamName', 'awayteamAbbrev']])

# %% [code] {"execution":{"iopub.status.busy":"2025-01-03T19:48:27.416706Z","iopub.execute_input":"2025-01-03T19:48:27.417102Z","iopub.status.idle":"2025-01-03T19:48:27.932731Z","shell.execute_reply.started":"2025-01-03T19:48:27.417072Z","shell.execute_reply":"2025-01-03T19:48:27.931721Z"}}

# Assuming team_data and game_data_filtered are already loaded


# Step 2: Merge home team abbreviations with filtered team data
game_data_filtered = pd.merge(
    game_data_filtered, 
    team_data_filtered[['teamId', 'teamAbbrev']], 
    left_on='hometeamId', 
    right_on='teamId', 
    how='left'
)
game_data_filtered = game_data_filtered.rename(columns={'teamAbbrev': 'team_abbreviation_home'}).drop(columns=['teamId'])

# Step 3: Merge away team abbreviations with filtered team data
game_data_filtered = pd.merge(
    game_data_filtered, 
    team_data_filtered[['teamId', 'teamAbbrev']], 
    left_on='awayteamId', 
    right_on='teamId', 
    how='left'
)
game_data_filtered = game_data_filtered.rename(columns={'teamAbbrev': 'team_abbreviation_away'}).drop(columns=['teamId'])

# Check the result
print(game_data_filtered[['gameId', 'gameDate', 'hometeamCity', 'hometeamName', 'team_abbreviation_home', 
                          'awayteamCity', 'awayteamName', 'team_abbreviation_away']])

# %% [code] {"execution":{"iopub.status.busy":"2025-01-03T19:48:27.416706Z","iopub.execute_input":"2025-01-03T19:48:27.417102Z","iopub.status.idle":"2025-01-03T19:48:27.932731Z","shell.execute_reply.started":"2025-01-03T19:48:27.417072Z","shell.execute_reply":"2025-01-03T19:48:27.931721Z"}}

# Filter to include only rows where both home and away team abbreviations are in the allowed_teams list
game_data_filtered = game_data_filtered[
    game_data_filtered['team_abbreviation_home'].isin(allowed_teams) &
    game_data_filtered['team_abbreviation_away'].isin(allowed_teams)
]

# Check the result
print(game_data_filtered[['gameId', 'gameDate', 'hometeamCity', 'hometeamName', 'team_abbreviation_home', 
                          'awayteamCity', 'awayteamName', 'team_abbreviation_away']])












# %% [code] {"execution":{"iopub.status.busy":"2025-01-03T19:48:27.416706Z","iopub.execute_input":"2025-01-03T19:48:27.417102Z","iopub.status.idle":"2025-01-03T19:48:27.932731Z","shell.execute_reply.started":"2025-01-03T19:48:27.417072Z","shell.execute_reply":"2025-01-03T19:48:27.931721Z"}}

# Calculate the season column
def calculate_season(date):
    year = date.year
    if date.month <= 6:
        return f'{year - 1}-{str(year)[-2:]}'
    else:
        return f'{year}-{str(year + 1)[-2:]}'

new_table = new_table.copy()
new_table['season'] = new_table['game_date'].apply(calculate_season)

# Filter data for valid seasons and teams
my_data = new_table[new_table['season'] >= '2002-03']
allowed_teams = [
    'ATL', 'BOS', 'BKN', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL',
    'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS'
]
my_data_filtered = my_data[my_data['team_abbreviation_home'].isin(allowed_teams) | 
                           my_data['team_abbreviation_away'].isin(allowed_teams)]
my_data_filtered = my_data_filtered.copy()
my_data_filtered['team_abbreviation_home'] = my_data_filtered['team_abbreviation_home'].replace({'SEA': 'OKC', 'NOH': 'NOP', 'NJN': 'BKN', 'NOK': 'NOP', 'GS': 'GSW'})
my_data_filtered['team_abbreviation_away'] = my_data_filtered['team_abbreviation_away'].replace({'SEA': 'OKC', 'NOH': 'NOP', 'NJN': 'BKN', 'NOK': 'NOP', 'GS': 'GSW'})

# Filter for clutch games
clutch_games = my_data_filtered[
    ((my_data_filtered['plus_minus_home'] >= -5) & (my_data_filtered['plus_minus_home'] <= 5)) |
    ((my_data_filtered['plus_minus_away'] >= -5) & (my_data_filtered['plus_minus_away'] <= 5))
]

# Add results column for clutch games
def clutch_result(row):
    if row['plus_minus_home'] > 0:
        return 'win_home'
    elif row['plus_minus_home'] < 0:
        return 'loss_home'
    elif row['plus_minus_away'] > 0:
        return 'win_away'
    elif row['plus_minus_away'] < 0:
        return 'loss_away'
    return None

clutch_games['result'] = clutch_games.apply(clutch_result, axis=1)

# Split into wins and losses
wins = clutch_games[clutch_games['result'].str.contains('win')]
losses = clutch_games[clutch_games['result'].str.contains('loss')]

# Create pivot tables
wins_matrix_home = pd.pivot_table(
    wins[wins['result'] == 'win_home'],
    values='game_date',
    index='season',
    columns='team_abbreviation_home',
    aggfunc='count',
    fill_value=0
)

wins_matrix_away = pd.pivot_table(
    wins[wins['result'] == 'win_away'],
    values='game_date',
    index='season',
    columns='team_abbreviation_away',
    aggfunc='count',
    fill_value=0
)

losses_matrix_home = pd.pivot_table(
    losses[losses['result'] == 'loss_home'],
    values='game_date',
    index='season',
    columns='team_abbreviation_home',
    aggfunc='count',
    fill_value=0
)

losses_matrix_away = pd.pivot_table(
    losses[losses['result'] == 'loss_away'],
    values='game_date',
    index='season',
    columns='team_abbreviation_away',
    aggfunc='count',
    fill_value=0
)

# Combine home and away results
wins_matrix_combined = wins_matrix_home.add(wins_matrix_away, fill_value=0)
losses_matrix_combined = losses_matrix_home.add(losses_matrix_away, fill_value=0)

# Filter for allowed teams and sort by average
wins_matrix_combined = wins_matrix_combined[allowed_teams]
losses_matrix_combined = losses_matrix_combined[allowed_teams]

# Add average row
wins_matrix_combined.loc['Average'] = wins_matrix_combined.mean(axis=0).round(1)
losses_matrix_combined.loc['Average'] = losses_matrix_combined.mean(axis=0).round(1)

# Sort columns by average
wins_matrix_combined = wins_matrix_combined.sort_values(by='Average', axis=1, ascending=False)
losses_matrix_combined = losses_matrix_combined.sort_values(by='Average', axis=1, ascending=False)

# Display results
print("Wins Matrix (Combined):\n", wins_matrix_combined)
print("\nLosses Matrix (Combined):\n", losses_matrix_combined)

# Optional: Heatmap visualization
plt.figure(figsize=(10, 6))
sns.heatmap(wins_matrix_combined.T, annot=True, cmap='Blues', cbar_kws={'label': 'Wins'}, fmt='.0f')
plt.title('Heatmap of Wins by Season and Team')
plt.xlabel('Season')
plt.ylabel('Team')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
sns.heatmap(losses_matrix_combined.T, annot=True, cmap='Reds', cbar_kws={'label': 'Losses'}, fmt='.0f')
plt.title('Heatmap of Losses by Season and Team')
plt.xlabel('Season')
plt.ylabel('Team')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

