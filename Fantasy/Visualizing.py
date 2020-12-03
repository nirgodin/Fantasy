import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

data = pd.read_csv('Final Data.csv')

# Section 1: Fantasy

######################                               Player Stability                             ######################

# which are the most stable players from the fantasy points aspect

# Subsetting the relevant data and pivoting the table
stable_players = data[['Gameweek', 'Player', 'Pts.']]
stable_players = pd.pivot_table(stable_players,
                                index='Player',
                                columns='Gameweek',
                                values='Pts.')

cum_min_played = pd.read_csv(r'Cumulative Merged Data\CMD_S21_GW_10.csv')[['Player', 'Minutes played']]

stable_players = pd.merge(stable_players,
                          cum_min_played,
                          on='Player',
                          how='inner')

stable_players = stable_players[stable_players['Minutes played'] >= 200]

# Calculating the Mean and Standard Deviation for each player
stable_players['Mean'] = stable_players.drop(columns='Minutes played').mean(axis=1,
                                                                            skipna=True)

stable_players['Std'] = stable_players.drop(columns='Minutes played').std(axis=1,
                                                                          skipna=True)

stable_players = stable_players.sort_values(by='Std')
top_10_stable_players = stable_players[stable_players['Mean'] > 5].sort_values(by='Std').reset_index().head(10)



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


