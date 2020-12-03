import pandas as pd
import numpy as np
import seaborn as sns

# Importing the data
data = pd.read_csv(r'Final Data.csv')

# Subsetting only the rows that contain missing values
missing = data[data.isnull().any(axis=1)]

# It seems that there has been a problem while scraping gameweek eight's cost data.
#

player_cost = pd.pivot_table(data,
                             index=['Player'],
                             columns='Gameweek',
                             values='Cost')

sns.heatmap(player_cost[[6, 7, 9]].corr(),
            annot=True,
            cmap='coolwarm')
d
player_cost.columns

