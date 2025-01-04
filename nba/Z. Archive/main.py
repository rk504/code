from nba_api.stats.endpoints import leaguegamefinder

# Example: Find games played by a specific player
gamefinder = leaguegamefinder.LeagueGameFinder(player_or_team_abbreviation='P')  
games = gamefinder.get_data_frames()[0]
print(games.head())

