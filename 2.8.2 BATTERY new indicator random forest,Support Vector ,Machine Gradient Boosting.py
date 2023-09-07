import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import GridSearchCV

# Read data
df = pd.read_excel('BATTER_Enhanced_Anonymized_Data.xlsx')

# Remove unnecessary columns
df.drop(['BATTER'], axis=1, inplace=True)

# Data cleaning: handling missing values in numerical columns
for col in df.select_dtypes(include=['float64', 'int64']).columns:
    df[col].fillna(df[col].mean(), inplace=True)

# Features and Labels
X = df[["Total_RUNS", "Innings", "Highest_Score", "Total_BALLS", "Batting_Average", "Centuries", "Fifties", "Zeroes", "Strike_Rate"]]
y = df['Performance']

# Data split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define resampling strategy
resample = Pipeline([
    ('Under', RandomUnderSampler(sampling_strategy=0.5)),
    ('Over', SMOTE())
])

# Resampling
X_resampled, y_resampled = resample.fit_resample(X_train, y_train)

# Feature selection
selector = SelectFromModel(RandomForestClassifier(n_estimators=100, random_state=42))
selector.fit(X_resampled, y_resampled)
X_res_selected = selector.transform(X_resampled)
X_test_selected = selector.transform(X_test)

# Random Forest model
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_res_selected, y_resampled)
y_pred_rf = rf.predict(X_test_selected)

# Support Vector Machine model
svm = SVC(probability=True, random_state=42)
svm.fit(X_res_selected, y_resampled)
y_pred_svm = svm.predict(X_test_selected)

# Define Gradient Boosting Grid Search parameters
param_grid = {
    'n_estimators': [50, 100, 150],
    'learning_rate': [0.01, 0.1, 1.0],
    'max_depth': [1, 3, 5]
}

# Optimize Gradient Boosting using Grid Search
grid_search = GridSearchCV(GradientBoostingClassifier(random_state=42), param_grid, cv=5)
grid_search.fit(X_res_selected, y_resampled)

# Get the best model
best_gbm = grid_search.best_estimator_

# Make predictions using the best model
y_prob_best_gbm = best_gbm.predict_proba(X_test_selected)[:, 1]

# Adjust the threshold
new_threshold_best_gbm = 0.3
y_pred_best_gbm = [1 if prob >= new_threshold_best_gbm else 0 for prob in y_prob_best_gbm]

# Evaluate models
def evaluate_model(y_test, y_pred, model_name):
    print(f"\n------ {model_name} ------")
    print('Accuracy:', accuracy_score(y_test, y_pred))
    print('Confusion Matrix:', confusion_matrix(y_test, y_pred))
    print('Classification Report:', classification_report(y_test, y_pred))

# Evaluate Random Forest
evaluate_model(y_test, y_pred_rf, "Random Forest")

# Evaluate Support Vector Machine
evaluate_model(y_test, y_pred_svm, "Support Vector Machine")

# Evaluate Optimized Gradient Boosting
evaluate_model(y_test, y_pred_best_gbm, "Optimized Gradient Boosting Machine")
