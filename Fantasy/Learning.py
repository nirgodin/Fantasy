import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures
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

# Dropping observations with the highest number of points, which doesn't represent typical players' performance
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
scaler = MinMaxScaler()
scaler.fit(X)
X = scaler.transform(X)

# Define train, cross validation and test sets
# First split - train and test
X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=0.4,
                                                    random_state=42)

# Second split - cross validation and test
X_cv, X_test, y_cv, y_test = train_test_split(X_test, y_test, test_size=0.5)


#######################################        ARTIFICIAL NEURAL NETWORK         #######################################


# Building a simple neural network
ann = Sequential()

# Add three dense layers with decreasing number of neurons, each with dropout layers
ann.add(Dense(5, activation='selu'))
ann.add(Dropout(0.5))

# Add final output layer, which will predict the number of points
ann.add(Dense(1))
ann.compile(optimizer='adam',
            loss='mse')

# Set early stopping rule
early_stop = EarlyStopping(monitor='val_loss',
                           mode='min',
                           patience=50)

# Train
ann.fit(x=X_train,
        y=y_train,
        validation_data=(X_cv, y_cv),
        batch_size=128,
        epochs=500,
        callbacks=[early_stop],
        verbose=0)


##########################################            EVALUATING             ##########################################


# Learning curve - describing test and validation errors over epochs
LC = pd.DataFrame(ann.history.history)
LC.plot()

# Checking the MSE against the true y value, to see if they are correlated
y_hats = ann.predict(X_test)
y_hats = pd.Series(y_hats.reshape(len(y_hats),))

true_hats = pd.DataFrame({'true y': y_test.values,
                          'y hat': y_hats})


# Define mse function for convenience
def mse(y_true, y_hat):
    r = np.square(np.subtract(y_true, y_hat)).mean()
    return r


# Calculate the mse for each observation
true_hats['mse'] = true_hats['true y'].apply(lambda x: mse(x, true_hats['y hat']))

sns.scatterplot(x='true y',
                y='mse',
                data=true_hats)

