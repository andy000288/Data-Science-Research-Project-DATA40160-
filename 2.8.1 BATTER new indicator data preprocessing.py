import pandas as pd
import pickle

# Read two Excel files
all_teams_df = pd.read_excel('BATTER_All_Teams_Data.xlsx')
performance_well_df = pd.read_excel('BATTER_Performance well_Data.xlsx')

# Add a 'Performance' column in 'all_teams_df' and set its value to 0
all_teams_df['Performance'] = 0

# Add a 'Performance' column in 'performance_well_df' and set its value to 1
performance_well_df['Performance'] = 1

# Merge two datasets
merged_df = pd.concat([all_teams_df, performance_well_df], ignore_index=True)

# Find 'BATTER' values that appear in both datasets and set their 'Performance' value to 1
common_batters = set(all_teams_df['BATTER']).intersection(set(performance_well_df['BATTER']))
merged_df.loc[merged_df['BATTER'].isin(common_batters), 'Performance'] = 1

# Record the original data count
original_data_count = len(merged_df)

# Remove rows where 'RUNS', '4s', '6s', and 'SR' are all 0
merged_df = merged_df[~((merged_df['RUNS'] == 0) & (merged_df['4s'] == 0) & (merged_df['6s'] == 0) & (merged_df['SR'] == 0))]
# Remove rows where 'RUNS', '4s', '6s', and 'SR' are all NaN
merged_df.dropna(subset=['RUNS', '4s', '6s', 'SR'], how='all', inplace=True)
# Remove duplicate rows
merged_df = merged_df.drop_duplicates()

# Create mappings and reverse mappings
id_mapping = {original: f'ID_{i}' for i, original in enumerate(merged_df['ID'].unique())}
batter_mapping = {original: f'BATTER_{i}' for i, original in enumerate(merged_df['BATTER'].unique())}

# Create reverse mappings for future lookup
id_reverse_mapping = {v: k for k, v in id_mapping.items()}
batter_reverse_mapping = {v: k for k, v in batter_mapping.items()}

# Replace original ID and BATTER columns with new anonymous identifiers
merged_df['ID'] = merged_df['ID'].map(id_mapping)
merged_df['BATTER'] = merged_df['BATTER'].map(batter_mapping)

# Group by BATTER and perform aggregation
grouped_df = merged_df.groupby('BATTER').agg({
    'RUNS': ['sum', 'count', 'max'],
    'BALLS': 'sum',
    'Performance': 'max',
    'ID': 'first',
    'CLUB': 'first'
}).reset_index()

# Rename aggregated columns
grouped_df.columns = ['BATTER', 'Total_RUNS', 'Innings', 'Highest_Score', 'Total_BALLS', 'Performance', 'ID', 'CLUB']

# Calculate additional new metrics
grouped_df['Batting_Average'] = grouped_df['Total_RUNS'] / grouped_df['Innings']
grouped_df['Centuries'] = merged_df.groupby('BATTER').apply(lambda x: (x['RUNS'] >= 100).sum()).reset_index(name='Centuries')['Centuries']
grouped_df['Fifties'] = merged_df.groupby('BATTER').apply(lambda x: ((x['RUNS'] >= 50) & (x['RUNS'] < 100)).sum()).reset_index(name='Fifties')['Fifties']
grouped_df['Zeroes'] = merged_df.groupby('BATTER').apply(lambda x: (x['RUNS'] == 0).sum()).reset_index(name='Zeroes')['Zeroes']
grouped_df['Strike_Rate'] = (grouped_df['Total_RUNS'] / grouped_df['Total_BALLS']) * 100

# Set Strike_Rate to 0 when Total_RUNS is 0 and Total_BALLS is 0
grouped_df.loc[(grouped_df['Total_RUNS'] == 0) & (grouped_df['Total_BALLS'] == 0), 'Strike_Rate'] = 0

# Set Strike_Rate to 2000 when Total_RUNS is not 0 and Total_BALLS is 0
grouped_df.loc[(grouped_df['Total_RUNS'] != 0) & (grouped_df['Total_BALLS'] == 0), 'Strike_Rate'] = 2000

# Save mappings and reverse mappings
with open('id_mapping.pkl', 'wb') as f:
    pickle.dump(id_mapping, f)
with open('id_reverse_mapping.pkl', 'wb') as f:
    pickle.dump(id_reverse_mapping, f)
with open('batter_mapping.pkl', 'wb') as f:
    pickle.dump(batter_mapping, f)
with open('batter_reverse_mapping.pkl', 'wb') as f:
    pickle.dump(batter_reverse_mapping, f)

# Save the dataframe with new metrics and 'Performance', 'ID', 'CLUB' to a new Excel file
grouped_df.to_excel('BATTER_Enhanced_Anonymized_Data.xlsx', index=False)


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the enhanced anonymized dataset
enhanced_df = pd.read_excel('BATTER_Enhanced_Anonymized_Data.xlsx')

# Exclude columns that are not needed for analysis
columns_to_exclude = ['ID', 'BATTER', 'CLUB']
enhanced_df.drop(columns=columns_to_exclude, inplace=True)

# Calculate the correlation matrix
correlation_matrix = enhanced_df.corr()

# Plot a heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Heatmap')
plt.show()

# Find correlations with the 'Performance' column
performance_correlation = correlation_matrix['Performance'].drop('Performance').sort_values(ascending=False)

# Output correlation results
print("Features with the highest correlation with 'Performance':")
print(performance_correlation)
