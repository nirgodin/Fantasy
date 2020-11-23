import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import scale

# Import the data
GW = pd.read_csv(r'Single GW\SGW_S21_GW_8.csv')

# Transforming categorical variables to dummy variables
# Role. This returns 3 dummy variables for FWD, GKP and MID roles, and drops the DEF role.
Role = pd.get_dummies(GW['Role'],
                        drop_first= True)

GW = pd.concat([GW, Role], axis=1).drop(columns=['Role'])

# Feature scaling
lala = scale(GW.drop(columns=['Player', 'Team', 'Opponent']))


# Define X vector of independents variables and Y dependent variable we want to predict (points)
X = GW.drop('Pts.', axis=1)
y = GW['Pts.']

# Define training and test sets
X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=0.33,
                                                    random_state=42)




