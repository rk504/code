# %% [code] {"execution":{"iopub.status.busy":"2025-01-03T19:48:27.416706Z","iopub.execute_input":"2025-01-03T19:48:27.417102Z","iopub.status.idle":"2025-01-03T19:48:27.932731Z","shell.execute_reply.started":"2025-01-03T19:48:27.417072Z","shell.execute_reply":"2025-01-03T19:48:27.931721Z"}}
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# Load and prepare the data
file_path = '~/code/data/kaggle/input/basketball/csv/Games.csv'
game_data = pd.read_csv(file_path)
team_data = pd.read_csv('~/code/data/kaggle/input/basketball/csv/TeamHistories.csv')
# %%
# USE ID'S, NOT ABBREVIATIONS FOR ANALYSES. TEAMID'S REMAIN THE SAME OVER TIME AND TIE IN THE HISTORICAL RECORDS
# Reverse the rows of the DataFrame (to get the most recent team names)
team_data_reversed = team_data.iloc[::-1].reset_index(drop=True)

# Sort by 'yearFounded' in descending order
team_data_sorted = team_data_reversed.sort_values(by='yearFounded', ascending=False)
print(team_data.head())

# Drop duplicates based on 'teamId' to keep only the most recent for each team
team_data_filtered = team_data_sorted.drop_duplicates(subset='teamId')

# Replace 'NOH' with 'NOP' for New Orleans Pelicans
# Update 'teamAbbrev' and 'teamName' for the team with teamId == 1610612740
team_data_filtered.loc[team_data_filtered['teamId'] == 1610612740, 'teamAbbrev'] = 'NOP'
team_data_filtered.loc[team_data_filtered['teamId'] == 1610612740, 'teamName'] = 'Pelicans'

# Verify the result
print(team_data_filtered)
print("Length of filtered team data:", len(team_data_filtered))



# %%
# Let pandas infer the date format and convert 'gameDate' to datetime
game_data['gameDate'] = pd.to_datetime(game_data['gameDate'], errors='coerce')

# Now you can proceed with the rest of the operations
game_data['gameDate'] = game_data['gameDate'].dt.strftime('%Y-%m-%d')  # Convert to YYYY-MM-DD format
game_data['pointDifferential'] = game_data['homeScore'] - game_data['awayScore']

# Drop the last 5 columns
game_data_filtered = game_data.iloc[:, :-6]
game_data_filtered['pointDifferential'] = game_data_filtered['homeScore'] - game_data_filtered['awayScore']

# %%
# Assuming 'game_data' is your original DataFrame

# Filter the DataFrame for games where the point differential is less than 5
clutch = game_data_filtered[abs(game_data_filtered['pointDifferential']) < 5]


# %%
# Calculate the season column
def calculate_season(date):
    year = date.year
    if date.month <= 6:
        return f'{year - 1}-{str(year)[-2:]}'
    else:
        return f'{year}-{str(year + 1)[-2:]}'

clutch = clutch.copy()
clutch['gameDate'] = pd.to_datetime(clutch['gameDate'])
clutch['season'] = clutch['gameDate'].apply(calculate_season)

# Remove rows where 'season' is either NaN or 'nan-an'
clutch_cleaned = clutch[~clutch['season'].isna() & (clutch['season'] != 'nan-an')]

# Verify the result
print(clutch_cleaned.head())

# Verify the result
print(clutch_cleaned.tail())



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

# Create a pivot table for the heatmap
pt = table.pivot_table(index='hometeamAbbrev', columns='season', values='win', aggfunc='count', fill_value=0)

# Reverse the order of the seasons
pt = pt[sorted(pt.columns, reverse=True)]

# Check the result
print(pt)

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

# Example usage:
team_id = 1610612755  # Philadelphia's teamID
result = filter_team_head(table, team_id)
print(result)

# %%
# Sort the dictionary by the team abbreviation (value) alphabetically
sorted_team_id_to_abbrev = dict(sorted(team_id_to_abbrev.items(), key=lambda item: item[1]))

# Display the sorted dictionary
for team_id, abbrev in sorted_team_id_to_abbrev.items():
    print(f"{team_id}: '{abbrev}'")

# %%
def adjust_table_for_cha(table):
    """
    Adjusts a DataFrame so that CHA (1610612766) in 2003 and 2004 seasons is displayed as '-'
    but treated as NaN for calculations, handling both 'awayteamId' and 'hometeamId'.
    
    Parameters:
    table (pd.DataFrame): The input table containing team data.
    
    Returns:
    pd.DataFrame: The adjusted table.
    """
    # Define CHA team ID and target seasons
    cha_team_id = 1610612766
    target_seasons = ['2002-03', '2003-04']
    
    # Adjust for 'awayteamId'
    mask_away = (table['awayteamId'] == cha_team_id) & (table['season'].isin(target_seasons))
    table.loc[mask_away, 'awayteamId'] = np.nan  # Treat as NaN for calculations
    table.loc[mask_away, 'awayteamAbbrev'] = '-'  # Set display to '-'
    
    # Adjust for 'hometeamId'
    mask_home = (table['hometeamId'] == cha_team_id) & (table['season'].isin(target_seasons))
    table.loc[mask_home, 'hometeamId'] = np.nan  # Treat as NaN for calculations
    table.loc[mask_home, 'hometeamAbbrev'] = '-'  # Set display to '-'
    
    return table



# %%
# Apply the function
#adjusted_df = adjust_charlotte_data(pt)
# Add an average column at the end of the heatmap
pt['Average'] = pt.mean(axis=1).astype(int)

# Reorder columns to place 'Average' at the end
cols = pt.columns.tolist()
cols = [col for col in cols if col != 'Average'] + ['Average']
pt = pt[cols]
# Output the result
print(pt)
# Create the heatmap with seasons on the x-axis and home team abbreviations on the y-axis
plt.figure(figsize=(12, 10))
sns.heatmap(pt, annot=True, cmap="coolwarm", fmt="d", cbar=True)

# Add titles and labels
plt.title('NBA Team Clutch Home Wins (2004-05 to 2024-25, as of Jan 5)', fontsize=16)
plt.xlabel('Season')
plt.ylabel('Home Team Abbreviation')

plt.tight_layout()
plt.show()

plt.tight_layout()
plt.show()

#not bad. issues with DEN and NOP since rebranding...Why's it missing?? DEN and MIN since 2012? Can rly perfect this and then send it off. Got p far, but 2012 season is still fkn weird.
#fixed this thanks to data bogue - issue is now 2012-13 season is missing a serious amount of data from the table data. Need to fix this.
 # %%
# Check the 2012 data in the game_data
season_2012_data_game = game_data[game_data['season'] == '2012-13']

# Print the number of rows for the 2012 season
print(f"Number of rows for the 2012-13 season in game_data: {len(season_2012_data_game)}")

# Display the first few rows of the 2012-13 season data
print(season_2012_data_game.tail())

# Sum all of the team home wins for the 2012-13 season
total_home_wins_2012_game = season_2012_data_game['win'].sum()

# Print the total number of home wins for the 2012-13 season
print(f"Total home wins for the 2012-13 season in game_data: {total_home_wins_2012_game}")

# %%
# Check the 2012 data in the table
season_2012_data = table[table['season'] == '2012-13']

# Print the number of rows for the 2012 season
print(f"Number of rows for the 2012-13 season: {len(season_2012_data)}")

# Display the first few rows of the 2012-13 season data
print(season_2012_data.tail())

# Sum all of the team home wins for the 2012-13 season
total_home_wins_2012 = season_2012_data['win'].sum()

# Print the total number of home wins for the 2012-13 season
print(f"Total home wins for the 2012-13 season: {total_home_wins_2012}")

 # %% 