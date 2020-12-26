import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Import data
data = pd.read_csv(r'Model Data\Model Data - Final.csv')

# Creating dummy variables for Role
Role = pd.get_dummies(data['Role'], drop_first=True)
data = pd.concat([data, Role], axis=1).drop(columns=['Role'])

# Dropping irrelevant columns for the regression
data = data.drop(columns=['Player', 'Team', 'Opponent', 'Sel.']).dropna()

# Data Description dataframe
describe = data.describe().transpose()

# Distplot for the intended dependent variable - points
sns.displot(data['Pts.'])

# Correlation matrix
correlation = pd.DataFrame(data.corr()['Pts.'].sort_values())

# Some Scatterplots of the most correlated  Pts. with t
sns.scatterplot(x='Form.1', y='Pts.', data=data)
data['Pts.'].sort_values(ascending=False).head(60)
