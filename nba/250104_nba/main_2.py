# %% [code] {"execution":{"iopub.status.busy":"2025-01-03T19:48:27.416706Z","iopub.execute_input":"2025-01-03T19:48:27.417102Z","iopub.status.idle":"2025-01-03T19:48:27.932731Z","shell.execute_reply.started":"2025-01-03T19:48:27.417072Z","shell.execute_reply":"2025-01-03T19:48:27.931721Z"}}
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# Load and prepare the data
# would be nice to incorporate kaggle api so it is easier to refresh data.
file_path = '~/code/data/kaggle/input/basketball/csv/Games.csv'
game_data = pd.read_csv(file_path)
team_data = pd.read_csv('~/code/data/kaggle/input/basketball/csv/TeamHistories.csv')
# %%
# USE ID'S, NOT ABBREVIATIONS FOR ANALYSES. TEAMID'S REMAIN THE SAME OVER TIME AND TIE IN THE HISTORICAL RECORDS
# Reverse the rows of the DataFrame (to get the most recent team names)
team_data_reversed = team_data.iloc[::-1].reset_index(drop=True)

# Sort by 'yearFounded' in descending order
team_data_sorted = team_data_reversed.sort_values(by='yearFounded', ascending=False)

# Drop duplicates based on 'teamId' to keep only the most recent for each team
team_data_filtered = team_data_sorted.drop_duplicates(subset='teamId')

# Replace 'NOH' with 'NOP' for New Orleans Pelicans
# Update 'teamAbbrev' and 'teamName' for the team with teamId == 1610612740
team_data_filtered.loc[team_data_filtered['teamId'] == 1610612740, 'teamAbbrev'] = 'NOP'
team_data_filtered.loc[team_data_filtered['teamId'] == 1610612740, 'teamName'] = 'Pelicans'

# %%
# Let pandas infer the date format and convert 'gameDate' to datetime
game_data['gameDate'] = pd.to_datetime(game_data['gameDate'], errors='coerce')

# Now you can proceed with the rest of the operations
game_data['gameDate'] = game_data['gameDate'].dt.strftime('%Y-%m-%d')  # Convert to YYYY-MM-DD format

# Filter game_data for unique gameID values
game_data = game_data.drop_duplicates(subset='gameId')

# Drop the last 5 columns
game_data_filtered = game_data.iloc[:, :-5]
game_data_filtered['pointDifferential'] = game_data_filtered['homeScore'] - game_data_filtered['awayScore']

# Calculate the season column
def calculate_season(date):
    year = date.year
    if date.month <= 8:
        return f'{year - 1}-{str(year)[-2:]}'
    else:
        return f'{year}-{str(year + 1)[-2:]}'

game_data_filtered['gameDate'] = pd.to_datetime(game_data_filtered['gameDate'])
game_data_filtered['season'] = game_data_filtered['gameDate'].apply(calculate_season)

# %%
# Filter the DataFrame for games where the point differential is less than or equal to 5
clutch = game_data_filtered[abs(game_data_filtered['pointDifferential']) <= 5]
# Remove rows where 'season' is either NaN or 'nan-an'
clutch_cleaned = clutch[~clutch['season'].isna() & (clutch['season'] != 'nan-an')]
# %%
# Define the mapping from teamId to teamAbbrev
team_id_to_abbrev = {
    1610612737: 'ATL',  # Atlanta Hawks
    1610612738: 'BOS',  # Boston Celtics
    1610612739: 'CLE',  # Cleveland Cavaliers
    1610612740: 'NOP',  # New Orleans Pelicans
    1610612741: 'CHI',  # Chicago Bulls
    1610612742: 'DAL',  # Dallas Mavericks
    1610612743: 'DEN',  # Denver Nuggets
    1610612744: 'GSW',  # Golden State Warriors
    1610612745: 'HOU',  # Houston Rockets
    1610612746: 'LAC',  # Los Angeles Clippers
    1610612747: 'LAL',  # Los Angeles Lakers
    1610612748: 'MIA',  # Miami Heat
    1610612749: 'MIL',  # Milwaukee Bucks
    1610612750: 'MIN',  # Minnesota Timberwolves
    1610612751: 'BKN',  # Brooklyn Nets
    1610612752: 'NYK',  # New York Knicks
    1610612753: 'ORL',  # Orlando Magic
    1610612754: 'IND',  # Indiana Pacers
    1610612755: 'PHI',  # Philadelphia 76ers
    1610612756: 'PHX',  # Phoenix Suns
    1610612757: 'POR',  # Portland Trail Blazers
    1610612758: 'SAC',  # Sacramento Kings
    1610612759: 'SAS',  # San Antonio Spurs
    1610612760: 'OKC',  # Oklahoma City Thunder
    1610612761: 'TOR',  # Toronto Raptors
    1610612762: 'UTA',  # Utah Jazz
    1610612763: 'MEM',  # Memphis Grizzlies
    1610612764: 'WAS',  # Washington Wizards
    1610612765: 'DET',  # Detroit Pistons
    1610612766: 'CHA',  # Charlotte Hornets
}
# %%
# Filter for seasons since 2000
table = clutch_cleaned[clutch_cleaned['season'] >= "2004-05"]

# Add the 'teamAbbrev' column to your existing 'table' based on the 'teamId'
table = table.copy()
table['awayteamAbbrev'] = table['awayteamId'].map(team_id_to_abbrev)
table['hometeamAbbrev'] = table['hometeamId'].map(team_id_to_abbrev)

# Create a new column 'win' that is 1 if pointDifferential is positive (win), 0 if negative (loss)
table['win'] = (table['pointDifferential'] > 0).astype(int)
# %%
def filter_team_head(dataframe, team_id, n=5):
    """
    Filters a DataFrame for rows where teamID matches the specified team_id
    and returns the first n rows of the result.

    Parameters:
    - dataframe (pd.DataFrame): The DataFrame to filter.
    - team_id (int): The teamID to filter by.
    - n (int): Number of rows to display from the result. Default is 5.

    Returns:
    - pd.DataFrame: Filtered DataFrame with the first n rows.
    """
    filtered_df = dataframe[(dataframe['hometeamId'] == team_id) | (dataframe['awayteamId'] == team_id)]
    return filtered_df.head(n)
# %%
# Sort the dictionary by the team abbreviation (value) alphabetically
sorted_team_id_to_abbrev = dict(sorted(team_id_to_abbrev.items(), key=lambda item: item[1]))

# %% 
# next count games in 2012-13 season data - is this an issue for all data?
# Count unique game IDs in game_data_filtered by season
unique_game_ids_by_season = game_data_filtered.groupby('season')['gameId'].nunique()

# Print unique game IDs starting from the 2010-11 season to the end
print(unique_game_ids_by_season.loc['2010-11':])# fkn bogue - we're missing both the 12-13 season and the 23-24 season. Damn. At least the data is pulling through correctly.
# %%
# Filter the clutch table to include only home games
clutch_home_games = table[table['hometeamId'].notna()]

# Exclude the 2012-13 and 2024-25 seasons from clutch_home_games
clutch_home_games = clutch_home_games[(clutch_home_games['season'] != '2012-13') & (clutch_home_games['season'] != '2024-25')]

# Create a new column 'win' that is 1 if pointDifferential is greater than or equal to 1 (win), 0 otherwise
clutch_home_games['win'] = (clutch_home_games['pointDifferential'] >= 1).astype(int)

# Create a pivot table for the heatmap using only home games
pt_home_games = clutch_home_games.pivot_table(index='hometeamAbbrev', columns='season', values='win', aggfunc='sum', fill_value=0)
# Reverse the order of the seasons
pt_home_games = pt_home_games[sorted(pt_home_games.columns, reverse=True)]

# Add an average column at the end of the heatmap
pt_home_games['Average'] = pt_home_games.mean(axis=1).astype(int)

# Reorder columns to place 'Average' at the end
cols_home_games = pt_home_games.columns.tolist()
cols_home_games = [col for col in cols_home_games if col != 'Average'] + ['Average']
pt_home_games = pt_home_games[cols_home_games]

# Create the heatmap with seasons on the x-axis and home team abbreviations on the y-axis
plt.figure(figsize=(12, 10))
sns.heatmap(pt_home_games, annot=True, cmap="coolwarm", fmt="d", cbar=True)

# Add titles and labels
plt.title('NBA Team Clutch Home Wins (2004-05 to 2022-23, minus 2012-13)', fontsize=16)

plt.tight_layout()
plt.show()

# %%
# Create a pivot table for home clutch wins
home_clutch_wins = clutch_home_games.pivot_table(index='hometeamAbbrev', columns='season', values='win', aggfunc='sum', fill_value=0)
home_clutch_wins = home_clutch_wins[sorted(home_clutch_wins.columns, reverse=True)]

# Create a pivot table for home clutch losses
clutch_home_games['loss'] = (clutch_home_games['pointDifferential'] < 1).astype(int)
home_clutch_losses = clutch_home_games.pivot_table(index='hometeamAbbrev', columns='season', values='loss', aggfunc='sum', fill_value=0)
home_clutch_losses = home_clutch_losses[sorted(home_clutch_losses.columns, reverse=True)]

# Create a difference table
home_clutch_diff = home_clutch_wins - home_clutch_losses

# Plot heatmaps for each table
fig, axes = plt.subplots(3, 1, figsize=(12, 30))

# Heatmap for home clutch wins
sns.heatmap(home_clutch_wins, annot=True, cmap="coolwarm", fmt="d", cbar=True, ax=axes[0])
axes[0].set_title('NBA Team Clutch Home Wins (2004-05 to 2022-23, minus 2012-13)', fontsize=16)

# Heatmap for home clutch losses
sns.heatmap(home_clutch_losses, annot=True, cmap="coolwarm", fmt="d", cbar=True, ax=axes[1])
axes[1].set_title('NBA Team Clutch Home Losses (2004-05 to 2022-23, minus 2012-13)', fontsize=16)

# Heatmap for home clutch win-loss difference
sns.heatmap(home_clutch_diff, annot=True, cmap="coolwarm", fmt="d", cbar=True, ax=axes[2])
axes[2].set_title('NBA Team Clutch Home Win-Loss Difference (2004-05 to 2022-23, minus 2012-13)', fontsize=16)

plt.tight_layout()
plt.show()
# %%
