import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# Transforming categorical variables to dummy variables
# Role. This returns 3 dummy variables for FWD, GKP and MID roles, and drops the DEF role.
Role = pd.get_dummies(GW['Role'],
                        drop_first= True)

# Define X vector of independents variables and Y dependent variable we want to predict (points)
X = GW.drop('Pts.', axis=1)
y = GW['Pts.']

# Define training and test sets
X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=0.33,
                                                    random_state=42)




