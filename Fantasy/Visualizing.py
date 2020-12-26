import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Setting variables which are relevant for the entire analysis
season = '21'
last_GW = '10'
minutes_threshold = 200

# Import data
data = pd.read_csv('Final Data.csv')
data = data.drop_duplicates()

######################                            SECTION 1 - FANTASY                            ######################

# SECTION 1.a - PLAYER STABILITY

# Which are the most stable players from the fantasy points aspect?
# This question is answered by measuring the different players' fantasy points standard deviation
# Low standard deviation indicates a stabler player

# Subset the relevant data
stable_players = data[['Gameweek', 'Player', 'Team', 'Pts.']]

# We won't like to include players who didn't play much in our analysis, so we will import the data about
# the cumulative minutes each played played in the season, and delete players who didn't play much
minutes_played = pd.read_csv(r'Cumulative Merged Data\CMD_S' + season + '_GW_' + last_GW + '.csv')[['Player',
                                                                                                    'Team',
                                                                                                    'Minutes played']]

# Merge the minutes played to the stable players df
stable_players = pd.merge(stable_players,
                          minutes_played,
                          on=['Player', 'Team'],
                          how='inner')

# Subsetting players who played less minutes than the minutes threshold we defined
stable_players = stable_players[stable_players['Minutes played'] >= minutes_threshold]

# Pivot the table
stable_players = pd.pivot_table(stable_players.drop(columns=['Team', 'Minutes played']),
                                index='Player',
                                columns='Gameweek',
                                values='Pts.')

# Calculating the Mean and Standard Deviation for each player
stable_players['Mean'] = stable_players.mean(axis=1,
                                             skipna=True)
stable_players['Std'] = stable_players.std(axis=1,
                                           skipna=True)

# Sorting the players by their standard deviation
stable_players = stable_players.sort_values(by='Std')

# Creating a list of the top 10 stable player who scored a lot of points
top10_stable_players = stable_players[stable_players['Mean'] > 5].sort_values(by='Std').reset_index().head(10)


# SECTION 1.b - PLAYER VALUE FOR MONEY

# Subset, create the Value variable and pivot
value_for_money = data[['Player', 'Gameweek', 'Cost', 'Pts.']]
value_for_money['Value'] = value_for_money['Pts.'] / value_for_money['Cost']
value_for_money = pd.pivot_table(value_for_money.drop(columns=['Cost', 'Pts.']),
                                 index='Player',
                                 columns='Gameweek',
                                 values='Value')

# Calculating average value for money
value_for_money['Mean'] = value_for_money.mean(axis=1,
                                               skipna=True)

# Sorting
value_for_money = value_for_money.sort_values(by='Mean',
                                              ascending=False)

# SECTION 1.c - FANTASY POINTS BY ROLE
role_fantasy_points = pd.read_csv(r'FPL\FPL_S' + season + '_GW1_' + last_GW + '.csv')[['Player',
                                                                                       'Team',
                                                                                       'Role',
                                                                                       'Pts.']]

# Merge with the minutes played dataframe
role_fantasy_points = pd.merge(role_fantasy_points,
                               minutes_played,
                               on=['Player', 'Team'],
                               how='inner')

role_fantasy_points = role_fantasy_points[role_fantasy_points['Minutes played'] >= minutes_threshold]
role_fantasy_points = role_fantasy_points.drop(columns=['Player', 'Team', 'Minutes played'])

role_fantasy_points = role_fantasy_points.groupby(by='Role').mean().sort_values(by='Pts.',
                                                                                ascending=False)

# SECTION 1.d - TEAMS FANTASY POINTS
team_fantasy_points = pd.read_csv(r'FPL\FPL_S' + season + '_GW1_' + last_GW + '.csv')[['Team', 'Pts.']]
team_fantasy_points = team_fantasy_points.groupby(by='Team').sum().sort_values(by='Pts.',
                                                                               ascending=False)

# SECTION 1.e - Selection vs. Fantasy Points

# Does most fantasy players knows what they are doing? Does the selection ratio of each player predicts his points?
# This is measured via a scatter plot of fantasy points and the selection ratio

sel_fantasy_points = sns.scatterplot(x='Sel.',
                                     y='Pts.',
                                     x_jitter=.1,
                                     data=data)

######################                            SECTION 2 - PLAYERS                            ######################

# SECTION 2.a - PLAYER OPPORTUNITY SEIZURE

# Which are the players who are best in seizing goaling opportunities?
# This question is answered by measuring the different players' cumulative non penalty Goals minus NPxG (non penalty xG).
# The higher this substraction is, the better the player in seizing opportunities, and vice versa.

# Import data and subset relevant columns
CM_data = pd.read_csv(r'Cumulative Merged Data\CMD_S' + season + '_GW_' + last_GW + '.csv')
seizing_players = CM_data[['Player', 'Player_NPG', 'Player_NPxG']]

# Create the Seizure variable
seizing_players['Seizure'] = seizing_players['Player_NPG'] - seizing_players['Player_NPxG']

# Sorting
seizing_players = seizing_players.sort_values(by='Seizure',
                                              ascending=False)

# Creating a list of the top 10 and worst 10 seizing players
top10_seizing_players = seizing_players.head(10)
worst10_seizing_players = seizing_players.tail(10)


#######################                            SECTION 3 - TEAMS                            #######################

# SECTION 2.a - TEAM OPPORTUNITY SEIZURE

# Which are the teams who are best in seizing goaling opportunities?
# This question is answered by the same methodology as the player opportunity seizure was answered

# Import data and subset relevant columns
PLT_data = pd.read_csv(r'PLT\PLT_S' + season + '_GW1_' + last_GW + '.csv')
seizing_teams = PLT_data[['Team', 'Team_G', 'Team_xG']]

# Create the Seizure variable
seizing_teams['Seizure'] = seizing_teams['Team_G'] - seizing_teams['Team_xG']

# Sorting
seizing_teams = seizing_teams.sort_values(by='Seizure',
                                          ascending=False)


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


