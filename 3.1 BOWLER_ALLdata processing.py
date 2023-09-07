import pandas as pd
import hashlib
import json

# Hash function for anonymizing, use only the first 6 characters
def hash_bowler(bowler_name):
    return hashlib.md5(bowler_name.encode()).hexdigest()[:6]

# Create a mapping from original name to hashed name
def create_mapping(df, column_name):
    unique_names = df[column_name].unique()
    mapping = {name: hash_bowler(name) for name in unique_names}
    return mapping

# 1. Load the datasets
df_all_teams = pd.read_excel('BOWLER_All_Data_Processied.xlsx')
df_performance_well = pd.read_excel('BOWLER_performance_well_Data.xlsx')

# Initial dataset sizes
print(f"Initial number of rows in df_all_teams: {len(df_all_teams)}")
print(f"Initial number of rows in df_performance_well: {len(df_performance_well)}")

# 2. Data Cleaning
df_all_teams.dropna(inplace=True)
df_performance_well.dropna(inplace=True)

# Dataset sizes after cleaning
print(f"Number of rows in df_all_teams after cleaning: {len(df_all_teams)}")
print(f"Number of rows in df_performance_well after cleaning: {len(df_performance_well)}")

# 3. Create and Save Mapping
mapping = create_mapping(df_all_teams, 'BOWLER')

# Save the mapping to a JSON file
with open('bowler_to_hash_mapping.json', 'w') as f:
    json.dump(mapping, f)

# 4. Feature Alignment
common_columns = list(set(df_all_teams.columns) & set(df_performance_well.columns))
df_all_teams = df_all_teams[common_columns]
df_performance_well = df_performance_well[common_columns]

# 5. Add Labels
df_performance_well['PERFORMANCE'] = 1
df_all_teams['PERFORMANCE'] = 0

# Update labels for well-performing players
df_all_teams.loc[df_all_teams['BOWLER'].isin(df_performance_well['BOWLER']), 'PERFORMANCE'] = 1

# 6. Merge Datasets
df_combined = pd.concat([df_all_teams, df_performance_well]).drop_duplicates().reset_index(drop=True)

# 7. Anonymize the 'BOWLER' column using the mapping
df_combined['BOWLER'] = df_combined['BOWLER'].map(mapping)

# Final dataset size and PERFORMANCE label counts
print(f"Final number of rows: {len(df_combined)}")
print(f"Number of rows where PERFORMANCE is 1: {len(df_combined[df_combined['PERFORMANCE'] == 1])}")
print(f"Number of rows where PERFORMANCE is 0: {len(df_combined[df_combined['PERFORMANCE'] == 0])}")

# 8. Save and Print the final dataset
df_combined.to_excel('BOWLER_Combined_Data.xlsx', index=False)
print("First 30 rows of the dataset:")
print(df_combined.head(30))

print("Data preprocessing, merging, and anonymization complete.")
