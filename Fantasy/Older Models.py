import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import scale, PolynomialFeatures
from sklearn.model_selection import learning_curve, train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Masking
from tensorflow.keras.callbacks import EarlyStopping


############################################         PREPROCESSING         ############################################


# Import data
data = pd.read_csv(r'Model Data\Model Data - Final.csv')

# Creating dummy variables for Role
Role = pd.get_dummies(data['Role'], drop_first=True)
data = pd.concat([data, Role], axis=1).drop(columns=['Role'])

# Dropping irrelevant columns for the regression
data = data.drop(columns=['Player', 'Team', 'Opponent', 'Sel.']).dropna()

# Dropping players with the highest number of points per game
data = data[data['Pts.'] <= 16]

# Dropping players who played less than 10 minutes per appearance
data = data[data['Minutes played'] / data['Player_Appearances'] > 10]

# Define X vector of independent variables and y dependent variable we want to predict (points)
X = data.drop('Pts.', axis=1)
# X = data[['Form', 'Minutes played', 'Goals scored', 'Assists', 'Clean sheets', 'Goals conceded', 'Bonus']]
y = data['Pts.']

# Introducing Polynomial Features
# trans2 = PolynomialFeatures(degree=2)
# poly2 = pd.DataFrame(trans2.fit_transform(X[['Goals scored', 'Assists', 'Cost']]))
# X = pd.concat([X.drop(columns=['Goals scored', 'Assists', 'Cost']).reset_index(drop=True), poly2.reset_index(drop=True)], axis=1)

# Feature scaling
X[X.drop(columns=['FWD', 'GKP', 'MID']).columns] = X.drop(columns=['FWD', 'GKP', 'MID']).apply(scale)
# X = X.apply(scale)

# Define train, cross validation and test sets
# First split - train and test
X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=0.4,
                                                    random_state=42)

# Second split - cross validation and test
X_cv, X_test, y_cv, y_test = train_test_split(X_test, y_test, test_size=0.5)


###########################################        LINEAR REGRESSION        ###########################################


# Learning Curve
train_sizes, train_scores, validation_scores = learning_curve(estimator=LinearRegression(),
                                                              X=X,
                                                              y=y,
                                                              train_sizes=list(range(1, len(X_train), round((len(X_train)/20)))),
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


###########################################        RANDOM FOREST TREE        ###########################################


# Setting Regressor
rft = RandomForestRegressor(n_estimators=200)

# Fitting
rft.fit(X_train, y_train)

# Predicting
rft_predictions = rft.predict(X_test)

# Predictions vs. Test set Distance plot
sns.displot((y_test-rft_predictions))

# Learning Curve
train_sizes, train_scores, validation_scores = learning_curve(estimator=RandomForestRegressor(n_estimators=200),
                                                              X=X,
                                                              y=y,
                                                              train_sizes=list(range(1, len(X_train), round((len(X_train)/20)))),
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


#######################################        RECURRENT NEURAL NETWORK         #######################################


rnn = Sequential()

# Recurrent layer
rnn.add(LSTM(64,
             return_sequences=False,
             dropout=0.1,
             recurrent_dropout=0.1))

# Fully connected layer
rnn.add(Dense(64,
              activation='relu'))

# Dropout for regularization
rnn.add(Dropout(0.5))

# Output layer
rnn.add(Dense(1))

# Compile the model
rnn.compile(optimizer='rmsprop',
            loss='mse',
            metrics=['mse'])

