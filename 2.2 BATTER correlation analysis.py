import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the data
df = pd.read_excel('BATTER_Merged_Data.xlsx')

# Select the features and target variable for analysis
selected_features = ['RUNS', 'BALLS', '4s', '6s', 'SR', 'Performance']
selected_df = df[selected_features]

# Calculate the correlation matrix between features
correlation_matrix = selected_df.corr()

# Visualize the correlation matrix using a heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Heatmap')
plt.show()

# Output the data of the correlation matrix
print("Correlation Matrix:")
print(correlation_matrix)
