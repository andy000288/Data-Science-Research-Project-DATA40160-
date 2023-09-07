import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import PolynomialFeatures
from imblearn.over_sampling import SMOTE
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.stattools import durbin_watson
import seaborn as sns

# Read the data
df = pd.read_excel('BATTER_Merged_Data.xlsx')

# Remove unnecessary columns
df.drop(['CLUB', 'BATTER', 'ID'], axis=1, inplace=True)

# Data cleaning: Handle missing values in numerical columns
for col in df.select_dtypes(include=['float64', 'int64']).columns:
    df[col].fillna(df[col].mean(), inplace=True)

# Data inspection: Print correlation matrix
print("Correlation Matrix:")
print(df.corr())

# Calculate VIF to check for multicollinearity
vif_data = pd.DataFrame()
vif_data["feature"] = df.columns
vif_data["VIF"] = [variance_inflation_factor(df.values, i) for i in range(len(df.columns))]
print("VIF values:")
print(vif_data)

# Features and Labels
X = df[['RUNS', 'BALLS', '4s', "6s", "SR"]]
y = df['Performance']

# Data Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Over-sampling to solve class imbalance
sm = SMOTE(random_state=42)
X_res, y_res = sm.fit_resample(X_train, y_train)

# Feature Selection
selector = SelectFromModel(RandomForestClassifier(n_estimators=100, random_state=42))
selector.fit(X_res, y_res)
X_res_selected = selector.transform(X_res)
X_test_selected = selector.transform(X_test)

# Polynomial Features
poly = PolynomialFeatures(degree=2, interaction_only=True)
X_poly = poly.fit_transform(X_res_selected)
X_test_poly = poly.transform(X_test_selected)

# Logistic Regression Model
model = LogisticRegression()
model.fit(X_poly, y_res)
y_pred = model.predict(X_test_poly)
y_prob = model.predict_proba(X_test_poly)[:, 1]

# Print Model Evaluation Metrics
print("\n------Logistic Regression------")
print('Accuracy:', accuracy_score(y_test, y_pred))
print('Confusion Matrix:', confusion_matrix(y_test, y_pred))
print('Classification Report:', classification_report(y_test, y_pred))

# Check for Linearity: Residual Plot
residuals = y_test - y_prob
sns.residplot(x=y_prob, y=residuals, lowess=True, line_kws={'color': 'red', 'lw': 1, 'alpha': 1})
plt.xlabel('Fitted values')
plt.title('Residual plot')
plt.show()

# Check for Independence: Durbin-Watson Statistic
durbin_watson_stat = durbin_watson(residuals)
print(f"Durbin-Watson statistic: {durbin_watson_stat}")

# If Durbin-Watson is close to 2, then observations are independent
if durbin_watson_stat > 1.5 and durbin_watson_stat < 2.5:
    print("The observations are independent.")
else:
    print("The observations are not independent.")


# Output selected features
selected_feat= X_train.columns[(selector.get_support())]
print(f"Selected features: {selected_feat}")

# Output ignored features
ignored_feat = X_train.columns[(~selector.get_support())]
print(f"Ignored features: {ignored_feat}")
