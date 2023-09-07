import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from imblearn.over_sampling import SMOTE

# Read the data
df = pd.read_excel('BATTER_Merged_Data.xlsx')

# Remove unnecessary columns
df.drop(['CLUB', 'BATTER', 'ID'], axis=1, inplace=True)

# Data cleaning: Handling missing values in numerical columns
for col in df.select_dtypes(include=['float64', 'int64']).columns:
    df[col].fillna(df[col].mean(), inplace=True)

# Features and labels
X = df[['RUNS', 'BALLS', '4s', '6s', 'SR']]
y = df['Performance']

# Data splitting
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Address class imbalance with oversampling
sm = SMOTE(random_state=42)
X_res, y_res = sm.fit_resample(X_train, y_train)

# Initial Random Forest model for feature selection
sel = RandomForestClassifier(n_estimators=100)
sel.fit(X_res, y_res)

# Feature selection
sel = SelectFromModel(sel)
sel.fit(X_res, y_res)
X_res_transformed = sel.transform(X_res)
X_test_transformed = sel.transform(X_test)

# Random Forest model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_res_transformed, y_res)
y_pred = rf_model.predict(X_test_transformed)

# Output model evaluation results
print("\n------Random Forest------")
print('Accuracy:', accuracy_score(y_test, y_pred))
print('Confusion Matrix:', confusion_matrix(y_test, y_pred))
print('Classification Report:', classification_report(y_test, y_pred))
