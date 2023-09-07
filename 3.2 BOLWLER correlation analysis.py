import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
# Note: Make sure your data file path is correct
df_combined = pd.read_excel('BOWLER_Combined_Data.xlsx')

# Remove columns not needed for analysis
df_combined.drop(['CLUB', 'BOWLER'], axis=1, inplace=True)

# Descriptive statistics
print("Descriptive Statistics:")
desc_stats = df_combined.describe()
desc_stats.to_excel('Descriptive_Statistics.xlsx')

# Correlation analysis
print("\nCorrelation Analysis:")
correlation_matrix = df_combined.corr()
print(correlation_matrix['PERFORMANCE'].sort_values(ascending=False))

# Select features for analysis
# Note: Here, it is assumed that the dataset contains columns like 'WICKETS', 'MAIDENS', 'NO BALLS', 'RUNS', 'ECON', 'OVERS', 'WIDES', 'PERFORMANCE'
# If the actual column names are different, please adjust accordingly
selected_features = ['WICKETS', 'MAIDENS', 'NO BALLS', 'RUNS', 'ECON', 'OVERS', 'WIDES', 'PERFORMANCE']

# Create a heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(df_combined[selected_features].corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.title("Correlation Heatmap")
plt.show()
