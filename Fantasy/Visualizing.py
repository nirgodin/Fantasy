import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

data = pd.read_csv('S21_GW1_8.csv')

# Checking if there are any missing values in the xG_FPL df, using a Seaborn heatmap
sns.heatmap(xG_FPL.isnull(),
            yticklabels=False,
            cbar=False,
            cmap='viridis')

# Histogram of the Fantasy points
Pts_histogram = sns.displot(data['Pts.'], kde=True)

# Scatterplot of the Fantasy Cost vs. Fantasy Points
Cost_Pts_scatterplot = sns.jointplot(x='Cost',
                                     y='Pts.',
                                     data= data,
                                     hue='Role')

# Scatterplot of the cumulative xG vs. cumulative Goals
xG_Goals_scatterplot = sns.jointplot(x='Player_xG',
                                     y='Goals scored',
                                     data=xG_FPL[xG_FPL['Role'] != 'GKP'],
                                     hue='Role')

# Scatterplot of the cumulative xA vs. cumulative Assists
xA_Assists_scatterplot = sns.jointplot(x='Player_xA',
                                     y='Assists',
                                     data=xG_FPL[xG_FPL['Role'] != 'GKP'],
                                     hue='Role')

# Comparing the average Fantasy points the different team gained, using barplot
av_team_pts = sns.barplot(x='Team',
                          y='Pts.',
                          data=xG_FPL)

# Comparing the Fantasy points sum the different team gained, using barplot
av_team_pts = sns.barplot(x='Team',
                          y='Pts.',
                          data=xG_FPL,
                          estimator=np.sum)

# Correlation heatmap for teams: team points and teams xG and xGA
sns.heatmap(xG_FPL_Team[['Team_PTS', 'Team_xG', 'Team_xGA']].corr(),
            annot=True,
            cmap='coolwarm')

# Clustering map for the entire xG_FPL dataframe
sns.clustermap(xG_FPL.drop(columns=['Player', 'Team', 'Role', 'Sel.']),
               cmap='coolwarm',
               standard_scale=1)
