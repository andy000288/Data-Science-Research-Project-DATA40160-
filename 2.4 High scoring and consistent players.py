import pandas as pd
import webbrowser

# Read the data
df = pd.read_excel('BATTER_Merged_Data.xlsx')

# Calculate the players' average strike rate (SR)
player_avg_sr = df.groupby('ID')['SR'].mean()

# Calculate descriptive statistics for players' SR
player_sr_distribution = df.groupby('ID')['SR'].describe().reset_index()

# Merge player's club information into the statistical data
player_sr_distribution = player_sr_distribution.merge(df[['ID', 'CLUB']].drop_duplicates(), on='ID')

# Filter players with SR higher than the average
high_sr_players = player_sr_distribution[player_sr_distribution['mean'] > df['SR'].mean()]

# Filter players with consistent SR (standard deviation lower than the median)
consistent_sr_players = player_sr_distribution[player_sr_distribution['std'] < player_sr_distribution['std'].median()]

# Filter players who have both high SR and consistent SR
high_and_consistent_sr_players = high_sr_players[high_sr_players['ID'].isin(consistent_sr_players['ID'])]

# Calculate the total number of samples
total_samples = len(df)

# Calculate the number and percentage of players with high SR
num_high_sr_players = len(high_sr_players)
percentage_high_sr_players = (num_high_sr_players / total_samples) * 100

# Calculate the number and percentage of players with stable SR
num_stable_sr_players = len(consistent_sr_players)
percentage_stable_sr_players = (num_stable_sr_players / total_samples) * 100

# Calculate the number and percentage of players with high and stable SR
num_high_and_stable_sr_players = len(high_and_consistent_sr_players)
percentage_high_and_stable_sr_players = (num_high_and_stable_sr_players / total_samples) * 100

# Calculate the number and percentage of players with high and stable SR and performance as 0
high_and_stable_sr_performance_zero = high_and_consistent_sr_players[high_and_consistent_sr_players['mean'] == 0]
num_high_stable_sr_performance_zero = len(high_and_stable_sr_performance_zero)
percentage_high_stable_sr_performance_zero = (num_high_stable_sr_performance_zero / total_samples) * 100

# Output the statistics
print(f"Total samples: {total_samples}")
print(f"Number of players with high SR: {num_high_sr_players} ({percentage_high_sr_players:.2f}%)")
print(f"Number of players with stable SR: {num_stable_sr_players} ({percentage_stable_sr_players:.2f}%)")
print(f"Number of players with high and stable SR: {num_high_and_stable_sr_players} ({percentage_high_and_stable_sr_players:.2f}%)")
print(f"Number of players with high and stable SR and performance as 0: {num_high_stable_sr_performance_zero} ({percentage_high_stable_sr_performance_zero:.2f}%)")

# Select player information from the original dataset for the chosen players
selected_players_info = df[df['ID'].isin(high_and_consistent_sr_players['ID'])]
selected_columns = ['ID', 'BATTER', "SR", 'RUNS', 'BALLS', '4s', '6s', 'Performance', 'CLUB']

# Output the information for the selected players
print(selected_players_info[selected_columns])

# Save the information for selected players as a CSV file
output_csv_filename = 'selected_players_info.csv'
selected_players_info[selected_columns].to_csv(output_csv_filename, index=False)

# Open the CSV file
webbrowser.open(output_csv_filename)
