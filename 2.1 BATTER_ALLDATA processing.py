import pandas as pd
import pickle

# Read two Excel files
all_teams_df = pd.read_excel('BATTER_All_Teams_Data.xlsx')
performance_well_df = pd.read_excel('BATTER_Performance_Well_Data.xlsx')

# Add a 'Performance' column in 'all_teams_df' and set its value to 0
all_teams_df['Performance'] = 0

# Add a 'Performance' column in 'performance_well_df' and set its value to 1
performance_well_df['Performance'] = 1

# Merge the two datasets
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

# Remove duplicate rows using the drop_duplicates method
merged_df = merged_df.drop_duplicates()

# Remove rows where 'SR' is 0
# merged_df = merged_df[merged_df['SR'] != 0]

# Set 'SR' to 0 when 'RUNS' is 0 and 'BALLS' is 0
merged_df.loc[(merged_df['RUNS'] == 0) & (merged_df['BALLS'] == 0), 'SR'] = 0

# Set 'SR' to the maximum value of 300 when 'RUNS' is not 0 and 'BALLS' is 0
merged_df.loc[(merged_df['RUNS'] != 0) & (merged_df['BALLS'] == 0), 'SR'] = 300

# Calculate the deleted data count
deleted_data_count = original_data_count - len(merged_df)

# Calculate the count of PERFORMANCE equal to 1
performance_1_count = merged_df['Performance'].sum()

# Calculate the count of PERFORMANCE equal to 0
performance_0_count = len(merged_df) - performance_1_count

# Create mapping tables
id_mapping = {original: f'ID_{i}' for i, original in enumerate(merged_df['ID'].unique())}
batter_mapping = {original: f'BATTER_{i}' for i, original in enumerate(merged_df['BATTER'].unique())}

# Create reverse mapping tables for future lookup
id_reverse_mapping = {v: k for k, v in id_mapping.items()}
batter_reverse_mapping = {v: k for k, v in batter_mapping.items()}

# Replace the original ID and BATTER columns with new anonymous identifiers
merged_df['ID'] = merged_df['ID'].map(id_mapping)
merged_df['BATTER'] = merged_df['BATTER'].map(batter_mapping)

# Save the mapping and reverse mapping tables for future use
with open('id_mapping.pkl', 'wb') as f:
    pickle.dump(id_mapping, f)
with open('id_reverse_mapping.pkl', 'wb') as f:
    pickle.dump(id_reverse_mapping, f)
with open('batter_mapping.pkl', 'wb') as f:
    pickle.dump(batter_mapping, f)
with open('batter_reverse_mapping.pkl', 'wb') as f:
    pickle.dump(batter_reverse_mapping, f)

# Save the processed data to a new Excel file
merged_df.to_excel('BATTER_Merged_Data.xlsx', index=False)

print("Original Data Count:", original_data_count)
print("Deleted Data Count:", deleted_data_count)
print("Performance 1 Count:", performance_1_count)
print("Performance 0 Count:", performance_0_count)
print("Merged and cleaned data has been saved to 'BATTER_Merged_Data.xlsx'.")
