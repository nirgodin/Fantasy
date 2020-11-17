import pandas as pd
import seaborn as sns
import os

# Set working directory
os.chdir(r'C:\Users\nirgo\Documents\GitHub\Fantasy\Fantasy')

data = pd.read_csv('S21_GW1_8.csv')

Pts_histogram = sns.displot(data['Pts.'], kde=True)

Cost_Pts_scatterplot = sns.jointplot(x='Cost',
                                     y='Pts.',
                                     data= data,
                                     hue='Role')
