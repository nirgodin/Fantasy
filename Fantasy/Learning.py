import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import scale
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import learning_curve
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


############################################         PREPROCESSING         ############################################


# Import data
data = pd.read_csv(r'Model Data\Model Data - Final.csv')

# Creating dummy variables for Role
Role = pd.get_dummies(data['Role'], drop_first=True)
data = pd.concat([data, Role], axis=1).drop(columns=['Role'])

# Dropping irrelevant columns for the regression
data = data.drop(columns=['Player', 'Team', 'Opponent', 'Sel.']).dropna()

# Define X vector of independent variables and y dependent variable we want to predict (points)
X = data.drop('Pts.', axis=1)
y = data['Pts.']

# Introducing Polynomial Features
trans2 = PolynomialFeatures(degree=2)
poly2 = pd.DataFrame(trans2.fit_transform(X[['Goals scored', 'Assists', 'Cost']]))
X = pd.concat([X.drop(columns=['Goals scored', 'Assists', 'Cost']).reset_index(drop=True), poly2.reset_index(drop=True)], axis=1)

# Feature scaling
X[X.drop(columns=['FWD', 'GKP', 'MID']).columns] = X.drop(columns=['FWD', 'GKP', 'MID']).apply(scale)


# Define training and test sets
X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=0.33,
                                                    random_state=42)


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


############################################         NEURAL NETWORK         ############################################


# Building a simple neural network
snn = Sequential()

# Add three dense layers with 4 neurons
snn.add(Dense(4, activation='relu'))
snn.add(Dense(4, activation='relu'))
snn.add(Dense(4, activation='relu'))

# Add final output layer, which will predict the number of points
snn.add(Dense(1))
snn.compile(optimizer='rmsprop',
            loss='mse',
            metrics='mse')

# Train
snn.fit(x=X_train,
        y=y_train,
        epochs=500,
        verbose=0)

# First way to evaluate the model epochs
snn_loss_df = pd.DataFrame(snn.history.history)
snn_loss_df.plot()

# Learning curve sketch - needs revisiting
history = snn.fit(X_train,
                  y_train,
                  validation_data=(X_test, y_test),
                  epochs=200,
                  batch_size=20)

history_dict = history.history
loss_values = history_dict['loss']
val_loss_values = history_dict['val_loss']
accuracy = history_dict['mse']
val_accuracy = history_dict['val_mse']

epochs = range(1, len(loss_values) + 1)
fig, ax = plt.subplots(1, 2, figsize=(14, 6))
#
# Plot the model accuracy vs Epochs
#
ax[0].plot(epochs, accuracy, 'bo', label='Training accuracy')
ax[0].plot(epochs, val_accuracy, 'b', label='Validation accuracy')
ax[0].set_title('Training &amp; Validation Accuracy', fontsize=16)
ax[0].set_xlabel('Epochs', fontsize=16)
ax[0].set_ylabel('Accuracy', fontsize=16)
ax[0].legend()
#
# Plot the loss vs Epochs
#
ax[1].plot(epochs, loss_values, 'bo', label='Training loss')
ax[1].plot(epochs, val_loss_values, 'b', label='Validation loss')
ax[1].set_title('Training &amp; Validation Loss', fontsize=16)
ax[1].set_xlabel('Epochs', fontsize=16)
ax[1].set_ylabel('Loss', fontsize=16)
ax[1].legend()

fig.show()
