import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split

# Read the data
df = pd.read_excel('BATTER_Merged_Data.xlsx')

# Features and labels
X = df[['RUNS', 'BALLS', '4s']]
y = df['Performance']

# Use data containing only players with Performance equal to 1 to train the model
X_train_pos = X[y == 1]

# Create and train the Isolation Forest model
clf = IsolationForest(contamination=0.1)
clf.fit(X_train_pos)

# Predict on the entire dataset
y_pred = clf.predict(X)

# Store the prediction results and true labels
results_df = pd.DataFrame({'Prediction': y_pred, 'True_Label': y})

# Filter out players who are actually Performance 0 but are marked as anomalies by the model
ignored_players_df = results_df[(results_df['Prediction'] == -1) & (results_df['True_Label'] == 0)]

# Merge the filtering results with the original data to get complete information for the ignored players
ignored_players_info = ignored_players_df.merge(df, left_index=True, right_index=True)

print("Ignored Players' Information:")
print(ignored_players_info)

# Save the results to an Excel file
ignored_players_info.to_excel('ignored_players1.xlsx', index=False)
