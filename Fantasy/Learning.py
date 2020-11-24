import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import scale
from sklearn.linear_model import LinearRegression
import seaborn as sns

# Import the data
GW = pd.read_csv(r'Final Data.csv')

# Transforming categorical variables to dummy variables
# Role. This returns 3 dummy variables for FWD, GKP and MID roles, and drops the DEF role.
Role = pd.get_dummies(GW['Role'], drop_first=True)

GW = pd.concat([GW, Role], axis=1).drop(columns=['Role'])

# Feature scaling
GW_LM = GW.copy()
GW_LM

GW_LM = pd.DataFrame(scale(GW.drop(columns=['Player', 'Team', 'Opponent'])),
                        columns=GW.drop(columns=['Player', 'Team', 'Opponent']).columns)

GW_LM = GW_LM.dropna()

# Define X vector of independents variables and Y dependent variable we want to predict (points)
X = GW_LM.drop('Pts.', axis=1)
y = GW_LM['Pts.']

# Define training and test sets
X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=0.33,
                                                    random_state=42)

# Linear Regression model
lm = LinearRegression()

# Fitting
lm.fit(X_train, y_train)

# Coefficients dataframe
lm_cdf = pd.DataFrame(lm.coef_, X.columns, columns=['Coeff'])

# Predicting
lm_predictions = lm.predict(X_test)

# Predictions vs. Test set scatterplot
sns.scatterplot(x=lm_predictions,y=y_test)

# Predictions vs. Test set Distance plot
sns.displot((y_test-lm_predictions))





