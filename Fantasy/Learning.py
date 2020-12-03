import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import scale
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import learning_curve
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import seaborn as sns
# from keras.models import Sequential
# from keras.layers import LSTM, Dense, Dropout, Masking, Embedding

# LINEAR REGRESSION

# Import data
lm_data = pd.read_csv(r'Models Data\lm_data.csv')

# Creating dummy variables for Role
Role = pd.get_dummies(lm_data['Role'], drop_first=True)
lm_data = pd.concat([lm_data, Role], axis=1).drop(columns=['Role'])

# Dropping irrelevant columns for the regression
lm_data = lm_data.drop(columns=['Player', 'Team']).dropna()

# Feature scaling
lm_data[lm_data.drop(columns=['Pts.', 'FWD', 'GKP', 'MID']).columns] = lm_data.drop(columns=['Pts.', 'FWD', 'GKP', 'MID']).apply(scale)

# Define X vector of independents variables and Y dependent variable we want to predict (points)
X_lm = lm_data.drop('Pts.', axis=1)
y_lm = lm_data['Pts.']

# Define training and test sets
X_lm_train, X_lm_test, y_lm_train, y_lm_test = train_test_split(X_lm,
                                                                y_lm,
                                                                test_size=0.33,
                                                                random_state=42)

# Learning Curve
train_sizes, train_scores, validation_scores = learning_curve(estimator=LinearRegression(),
                                                              X=X_lm,
                                                              y=y_lm,
                                                              train_sizes=list(range(1, len(X_lm_train), round((len(X_lm_train)/20)))),
                                                              cv=5,
                                                              scoring='neg_mean_squared_error')

# Calculating mean train and validation scores, which are calculated as MSE, and printing them
train_scores_mean = -train_scores.mean(axis=1)
validation_scores_mean = -validation_scores.mean(axis=1)
print('Mean training scores - Linear Regression\n\n', pd.Series(train_scores_mean, index=train_sizes))
print('\n', '-' * 20) # separator
print('\nMean validation scores - Linear Regression\n\n', pd.Series(validation_scores_mean, index=train_sizes))

# Drawing the learning curves
plt.style.use('seaborn')
plt.plot(train_sizes, train_scores_mean, label='Training error')
plt.plot(train_sizes, validation_scores_mean, label='Validation error')
plt.ylabel('MSE', fontsize=14)
plt.xlabel('Training set size', fontsize=14)
plt.title('Learning curves for a linear regression model', fontsize=18, y=1.03)
plt.legend()
plt.ylim(0, 40)

# Linear Regression model
lm = LinearRegression()

# Fitting
lm.fit(X_train, y_train)

# Coefficients lm_dataframe
# lm_cdf = pd.lm_data.DataFrame(lm.coef_, X.columns, columns=['Coeff'])

# Predicting
lm_predictions = lm.predict(X_test)

# Predictions vs. Test set scatterplot
sns.scatterplot(x=lm_predictions, y=y_test)

# Predictions vs. Test set Distance plot
sns.displot((y_test-lm_predictions))


#######################################################################################################################


# RANDOM FOREST TREE

# Setting Regressor
rft = RandomForestRegressor(n_estimators=500)

# Fitting
rft.fit(X_lm_train, y_lm_train)

# Predicting
rft_predictions = rft.predict(X_lm_test)

# Predictions vs. Test set Distance plot
sns.displot((y_lm_test-rft_predictions))

# Learning Curve
train_sizes, train_scores, validation_scores = learning_curve(estimator=RandomForestRegressor(n_estimators=200),
                                                              X=X_lm,
                                                              y=y_lm,
                                                              train_sizes=list(range(1, len(X_lm_train), round((len(X_lm_train)/20)))),
                                                              cv=5,
                                                              scoring='neg_mean_squared_error')

# Calculating mean train and validation scores, which are calculated as MSE, and printing them
train_scores_mean = -train_scores.mean(axis=1)
validation_scores_mean = -validation_scores.mean(axis=1)
print('Mean training scores - Linear Regression\n\n', pd.Series(train_scores_mean, index=train_sizes))
print('\n', '-' * 20) # separator
print('\nMean validation scores - Linear Regression\n\n', pd.Series(validation_scores_mean, index=train_sizes))

# Drawing the learning curves
plt.style.use('seaborn')
plt.plot(train_sizes, train_scores_mean, label='Training error')
plt.plot(train_sizes, validation_scores_mean, label='Validation error')
plt.ylabel('MSE', fontsize=14)
plt.xlabel('Training set size', fontsize=14)
plt.title('Learning Curves for a Random Forest Tree Model', fontsize=18, y=1.03)
plt.legend()
plt.ylim(0, 40)

