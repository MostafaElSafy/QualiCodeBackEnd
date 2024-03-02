import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import classification_report
from sklearn.linear_model import Ridge, Lasso
from sklearn.svm import SVR
import xgboost as xgb
from sklearn.ensemble import AdaBoostRegressor
from lightgbm import LGBMRegressor
import joblib

# Load the dataset
data = pd.read_csv('data.csv')
data

data.describe()

data.info()

data = data.drop("file_name",axis=1)

data.isnull().sum()

# Splitting the data into features and target
training = data.drop("complexity",axis=1)
training = pd.get_dummies(training, drop_first=True)

# Encode categorical columns
training = pd.get_dummies(training, drop_first=True)

# Encode target variable
target_mapping = {'n': 0, '1': 1, 'n_square': 2, 'nlogn': 3, 'logn': 4}
target_encoded = data["complexity"].map(target_mapping)

X_train, X_test, y_train, y_test = train_test_split(training, target_encoded, test_size=0.3, random_state=42)

# Separate numeric and categorical columns
numeric_cols = data.select_dtypes(include=['number']).columns
categorical_cols = data.select_dtypes(exclude=['number']).columns

# Standardize features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Print unique values in the target variable
print("Unique values in target variable ('y_train'):")
print(y_train.unique())

# Applying Linear Regression
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)
linear_predictions = linear_model.predict(X_test)
linear_predictions_rounded = linear_predictions.round()
linear_accuracy = accuracy_score(y_test, linear_predictions_rounded)

print("Linear Regression Accuracy:", linear_accuracy)

# Applying SVM
svm_model = SVC()
svm_model.fit(X_train, y_train)
svm_predictions = svm_model.predict(X_test)
svm_accuracy = accuracy_score(y_test, svm_predictions)

print("SVM Accuracy:", svm_accuracy)

# Applying Support Vector Machine with Linear kernel
svm_linear_model = SVC(kernel='linear')
svm_linear_model.fit(X_train, y_train)
svm_linear_predictions = svm_linear_model.predict(X_test)
svm_linear_accuracy = accuracy_score(y_test, svm_linear_predictions)
print("SVM Linear Accuracy:", svm_linear_accuracy)

# Applying Support Vector Regression (SVR)
svr_model = SVR()
svr_model.fit(X_train, y_train)
svr_predictions = svr_model.predict(X_test)
svr_predictions_rounded = svr_predictions.round()
svr_accuracy = accuracy_score(y_test, svr_predictions_rounded)
print("SVR Accuracy:", svr_accuracy)

# Applying Support Vector Regression with RBF kernel (SVR-RBF)
svr_rbf_model = SVR(kernel='rbf')
svr_rbf_model.fit(X_train, y_train)
svr_rbf_predictions = svr_rbf_model.predict(X_test)
svr_rbf_predictions_rounded = svr_rbf_predictions.round()
svr_rbf_accuracy = accuracy_score(y_test, svr_rbf_predictions_rounded)
print("SVR-RBF Accuracy:", svr_rbf_accuracy)

# Decision Tree Regression
dt_model = DecisionTreeRegressor(random_state=42)
dt_model.fit(X_train, y_train)
dt_predictions = dt_model.predict(X_test)

# Convert predictions to integer values for classification report
dt_predictions_int = dt_predictions.astype(int)

# Calculate accuracy for Decision Tree Regression
dt_accuracy = accuracy_score(y_test, dt_predictions_int)
print("Accuracy for Decision Tree Regression:", dt_accuracy)

# Applying Random Forest Regression
rf_model = RandomForestRegressor(random_state=42)
rf_model.fit(X_train, y_train)
rf_predictions = rf_model.predict(X_test)
rf_predictions_rounded = rf_predictions.round()
rf_accuracy = accuracy_score(y_test, rf_predictions_rounded)
print("Random Forest Regression Accuracy:", rf_accuracy)

# Applying Gradient Boosting Regression
gb_model = GradientBoostingRegressor(random_state=42)
gb_model.fit(X_train, y_train)
gb_predictions = gb_model.predict(X_test)
gb_predictions_rounded = gb_predictions.round()
gb_accuracy = accuracy_score(y_test, gb_predictions_rounded)
print("Gradient Boosting Regression Accuracy:", gb_accuracy)

# Applying XGBoost Regression
xgb_model = xgb.XGBRegressor(random_state=42)
xgb_model.fit(X_train, y_train)
xgb_predictions = xgb_model.predict(X_test)
xgb_predictions_rounded = xgb_predictions.round()
xgb_accuracy = accuracy_score(y_test, xgb_predictions_rounded)
print("XGBoost Regression Accuracy:", xgb_accuracy)

# Applying AdaBoost Regression
adaboost_model = AdaBoostRegressor(random_state=42)
adaboost_model.fit(X_train, y_train)
adaboost_predictions = adaboost_model.predict(X_test)
adaboost_predictions_rounded = adaboost_predictions.round()
adaboost_accuracy = accuracy_score(y_test, adaboost_predictions_rounded)
print("AdaBoost Regression Accuracy:", adaboost_accuracy)


df = pd.read_csv('data.csv')

# Assuming 'best_model' is your trained model
joblib.dump(svm_linear_model, 'best_model.pkl')

loaded_model = joblib.load('best_model.pkl')
#do preprocessing needed

# Assuming 'new_data' is a DataFrame with the same features as the training data
predictions = loaded_model.predict(df.drop(['file_name', 'complexity'], axis=1))
predictions