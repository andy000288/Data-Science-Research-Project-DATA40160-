import pandas as pd
import webbrowser

# Read the data
df = pd.read_excel('BATTER_Merged_Data.xlsx')

# Calculate the total number of samples
total_samples = df.shape[0]

# Calculate the average 'BALLS' for each team
team_avg_balls = df.groupby('CLUB')['BALLS'].mean().round(3)

# Add the average 'BALLS' for each team to the player's data
df_with_team_avg_balls = df.merge(team_avg_balls, left_on='CLUB', right_index=True, suffixes=('', '_team'))

# Find players with 'BALLS' higher than their team's average
outstanding_players_balls = df_with_team_avg_balls[df_with_team_avg_balls['BALLS'] > df_with_team_avg_balls['BALLS_team']].copy()
outstanding_players_balls['BALLS_difference'] = (outstanding_players_balls['BALLS'] - outstanding_players_balls['BALLS_team']).round(3)

# Calculate the number of players above the average 'BALLS'
above_avg_count = outstanding_players_balls.shape[0]

# Calculate the ratio of players above the average 'BALLS'
above_avg_ratio = (above_avg_count / total_samples) * 100

# Calculate the number of players with 'Performance' equal to 0
performance_zero_count = df[df['Performance'] == 0].shape[0]

# Calculate the ratio of players with 'Performance' equal to 0
performance_zero_ratio = (performance_zero_count / total_samples) * 100

# Find players with 'Performance' equal to 0 but 'BALLS' higher than average (potential overlooked players)
potential_overlooked_players = outstanding_players_balls[outstanding_players_balls['Performance'] == 0]

# Calculate the ratio of such players among those above the average 'BALLS'
if above_avg_count > 0:  # Avoid division by zero
    overlooked_ratio = (potential_overlooked_players.shape[0] / above_avg_count) * 100
else:
    overlooked_ratio = 0

# Print the analysis results
print(f"Total number of samples: {total_samples}")
print(f"Number of players above average 'BALLS': {above_avg_count}, Ratio: {above_avg_ratio:.2f}%")
print(f"Number of players with 'Performance' equal to 0: {performance_zero_count}, Ratio: {performance_zero_ratio:.2f}%")
print(f"Among players above average 'BALLS', number of players with 'Performance' equal to 0: {potential_overlooked_players.shape[0]}, Ratio: {overlooked_ratio:.2f}%")

# Find players with 'BALLS' higher than their team's average but 'Performance' equal to 1
performance_one_and_above_avg_balls = outstanding_players_balls[outstanding_players_balls['Performance'] == 0]

# Print information about such players
print("Players with average 'BALLS' higher than their team's average but 'Performance' equal to 0:")
print(performance_one_and_above_avg_balls)

# Output the results to an Excel file
excel_path = "Potential_Overlooked_Players.xlsx"
performance_one_and_above_avg_balls.to_excel(excel_path, index=False)

# Open the Excel file with the default application
webbrowser.open(excel_path)
