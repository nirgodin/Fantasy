import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Import data
data = pd.read_csv(r'Model Data\Model Data - Final.csv')

# Create a new dataframe which is regularized to player appearances
col_lst = ['Cum Pts.',
           'Minutes played',
           'Goals scored',
           'Assists',
           'Clean sheets',
           'Goals conceded',
           'Own goals',
           'Penalties']
data2 = data


# Exploring the upper percentile of the points distribution
head = data['Pts.'].sort_values(ascending=False).head(round(.01*len(data)))

# Exploring the bottom percentile of the points distribution
tail = data['Pts.'].sort_values(ascending=True).head(round(.01*len(data)))

# Checking if there are any players with 0 minutes played
minutes = data[data['Minutes played'] / data['Player_Appearances'] < 10]

# Data Description dataframe
describe = data.describe().transpose()

# Distplot for the intended dependent variable - points
sns.displot(data['Pts.'])

# Correlation matrix
correlation = pd.DataFrame(data.corr()['Pts.'].sort_values())

# Some Scatterplots of the most correlated  Pts. with t
sns.scatterplot(x='Form.1', y='Pts.', data=data)
data['Pts.'].sort_values(ascending=False).head(60)
