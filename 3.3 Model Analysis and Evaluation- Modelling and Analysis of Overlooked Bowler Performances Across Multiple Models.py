import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load and merge the datasets
df_combined = pd.read_excel('BOWLER_Combined_Data.xlsx')

# Address the class imbalance issue
selected_features = ['RUNS', 'OVERS', 'ECON', 'MAIDENS']
X = df_combined[selected_features]
y = df_combined['PERFORMANCE']

smote = SMOTE(sampling_strategy='auto')
X_balanced, y_balanced = smote.fit_resample(X, y)

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X_balanced, y_balanced, test_size=0.2, random_state=42)

# Random Forest model
rf_classifier = RandomForestClassifier(random_state=42, n_estimators=100)
rf_classifier.fit(X_train, y_train)
y_pred_rf = rf_classifier.predict(X_test)

print(f"Accuracy of Random Forest Classifier: {accuracy_score(y_test, y_pred_rf)*100:.2f}%")
print("Classification Report for Random Forest:")
print(classification_report(y_test, y_pred_rf))
print("Confusion Matrix for Random Forest:")
print(confusion_matrix(y_test, y_pred_rf))

feature_importances_rf = rf_classifier.feature_importances_
print("\nFeature Importances for Random Forest:")
print(pd.DataFrame({'Feature': selected_features, 'Importance': feature_importances_rf}).sort_values(by='Importance', ascending=False))

# Gradient Boosting model
gb_classifier = GradientBoostingClassifier(random_state=42)
gb_classifier.fit(X_train, y_train)
y_pred_gb = gb_classifier.predict(X_test)

print(f"\nAccuracy of Gradient Boosting Classifier: {accuracy_score(y_test, y_pred_gb)*100:.2f}%")
print("Classification Report for Gradient Boosting:")
print(classification_report(y_test, y_pred_gb))
print("Confusion Matrix for Gradient Boosting:")
print(confusion_matrix(y_test, y_pred_gb))

feature_importances_gb = gb_classifier.feature_importances_
print("\nFeature Importances for Gradient Boosting:")
print(pd.DataFrame({'Feature': selected_features, 'Importance': feature_importances_gb}).sort_values(by='Importance', ascending=False))

# XGBoost model
xgb_classifier = XGBClassifier(random_state=42)
xgb_classifier.fit(X_train, y_train)
y_pred_xgb = xgb_classifier.predict(X_test)

print(f"\nAccuracy of XGBoost Classifier: {accuracy_score(y_test, y_pred_xgb)*100:.2f}%")
print("Classification Report for XGBoost:")
print(classification_report(y_test, y_pred_xgb))
print("Confusion Matrix for XGBoost:")
print(confusion_matrix(y_test, y_pred_xgb))

feature_importances_xgb = xgb_classifier.feature_importances_
print("\nFeature Importances for XGBoost:")
print(pd.DataFrame({'Feature': selected_features, 'Importance': feature_importances_xgb}).sort_values(by='Importance', ascending=False))

import pandas as pd

# Comprehensive analysis and comparison of three models
models = [rf_classifier, gb_classifier, xgb_classifier]
model_names = ['Random Forest', 'Gradient Boosting', 'XGBoost']

results = []

for idx, model in enumerate(models):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    weighted_f1 = report['weighted avg']['f1-score']

    # Combine accuracy and weighted average F1-Score
    model_metric_avg = (accuracy + weighted_f1) / 2

    results.append({
        'Model': model_names[idx],
        'Accuracy': accuracy,
        'Weighted F1-Score': weighted_f1,
        'Combined Metric': model_metric_avg
    })

results_df = pd.DataFrame(results)
best_model = results_df.loc[results_df['Combined Metric'].idxmax()]

print("\nComparison of Models:")
print(results_df)

print(f"\n{best_model['Model']} has the highest combined performance in terms of accuracy and weighted F1-Score.")

# Generate a results table
results_table = results_df.to_markdown(index=False)

# Print the table and save it to a file
print("\nResults Table:")
print(results_table)

with open('model_comparison_results.txt', 'w') as f:
    f.write(results_table)
    f.write(f"\n\n{best_model['Model']} has the highest combined performance.")

# Use the models to predict on the entire dataset
df_combined['predicted_performance_rf'] = rf_classifier.predict(X)
df_combined['predicted_performance_gb'] = gb_classifier.predict(X)
df_combined['predicted_performance_xgb'] = xgb_classifier.predict(X)

# Find players with actual label 0 but predicted as 1 by the models
overlooked_players_rf = df_combined[(df_combined['PERFORMANCE'] == 0) & (df_combined['predicted_performance_rf'] == 1)]
overlooked_players_gb = df_combined[(df_combined['PERFORMANCE'] == 0) & (df_combined['predicted_performance_gb'] == 1)]
overlooked_players_xgb = df_combined[(df_combined['PERFORMANCE'] == 0) & (df_combined['predicted_performance_xgb'] == 1)]

print("Overlooked players according to Random Forest model:")
print(overlooked_players_rf)

print("\nOverlooked players according to Gradient Boosting model:")
print(overlooked_players_gb)

print("\nOverlooked players according to XGBoost model:")
print(overlooked_players_xgb)

# Find players overlooked by all three models
common_overlooked_players = pd.merge(overlooked_players_rf[['BOWLER']], overlooked_players_gb[['BOWLER']], on='BOWLER')
common_overlooked_players = pd.merge(common_overlooked_players, overlooked_players_xgb[['BOWLER']], on='BOWLER')

# Print players overlooked by all three models
print("Common overlooked players according to all three models:")
print(common_overlooked_players)

import os

# Save overlooked player information to Excel
with pd.ExcelWriter('Overlooked_Players_Analysis.xlsx') as writer:
    overlooked_players_rf.to_excel(writer, sheet_name='Overlooked_by_RF', index=False)
    overlooked_players_gb.to_excel(writer, sheet_name='Overlooked_by_GB', index=False)
    overlooked_players_xgb.to_excel(writer, sheet_name='Overlooked_by_XGB', index=False)
    common_overlooked_players.to_excel(writer, sheet_name='Common_Overlooked', index=False)
    results_df.to_excel(writer, sheet_name='Model_Comparison', index=False)

# Automatically open the Excel file
os.system('start excel "Overlooked_Players_Analysis.xlsx"')
