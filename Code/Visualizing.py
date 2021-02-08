import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN, KMeans
from sklearn.impute import SimpleImputer
import plotly.graph_objects as go

# Setting variables which are relevant for the entire analysis
season = '21'
last_GW = '22'
minutes_threshold = 200

# Import data
# We'll use three kinds of data, presented by three different dfs, in this code
# No 1. - Single gameweeks data, i.e, not cumulative data
data = pd.read_csv(r'Data\Final Data.csv')
data = data.drop_duplicates()

# No 2. - Cumulative data
cum_data = pd.read_csv(r'Data\Cumulative Merged Data\CMD_S' + season + '_GW_' + last_GW + '.csv')
cum_data.drop_duplicates()

# No 3. - Teams data
PLT_data = pd.read_csv(r'Data\PLT\PLT_S' + season + '_GW1_' + last_GW + '.csv')
PLT_data.drop_duplicates()


######################                            SECTION 1 - FANTASY                            ######################

# SECTION 1.a - PLAYER STABILITY

# Which are the most stable players from the fantasy points aspect?
# This question is answered by measuring the different players' fantasy points standard deviation
# Low standard deviation indicates a stabler player

# Merge the minutes played to the stable players df
stable_players = pd.merge(data[['Gameweek', 'Player', 'Team', 'Pts.']],
                          cum_data[['Player', 'Team', 'Minutes played']],
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

# Drop players with Std = 0
stable_players = stable_players[stable_players['Std'] != 0]

# Multiply the Std column by -1 to assign the lowest std (i.e the most stable player) the highest value
stable_players['Minus Std'] = stable_players['Std']*(-1)

# Use the MinMax scaler to produce a score ranging from 0 to 1 (where 0 is the most unstable player)
scaler = MinMaxScaler()
stable_players['Stability'] = scaler.fit_transform(stable_players['Minus Std'].values.reshape(-1, 1))
stable_players = stable_players.drop(index='Dawson')
# Get rid from players with mean points less than 4, and sort the dataframe by stability
top_stable_players = stable_players[stable_players['Mean'] > 4].sort_values(by='Stability',
                                                                            ascending=False).head(20)

# Delete irrelevant columns and round numbers
top_stable_players = top_stable_players[['Stability', 'Mean']].round(2)

# Create table
stable_table = go.Figure(data=[go.Table(
             header=dict(values=['Player', 'Stability', 'Points per game'],
                         fill_color='paleturquoise'),
             cells=dict(values=[top_stable_players.index, top_stable_players.Stability, top_stable_players.Mean],
                        fill_color='lavender'))
])

# # Update layout and size
# stable_table.update_layout_images(width=600,
#                                   height=335)

# Show table on browser
stable_table.show()

# Export
stable_table.write_image('Visualizations/Stability.png')


########################################


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


########################################


# SECTION 1.c - FANTASY POINTS BY ROLE
role_fantasy_points = pd.read_csv(r'Data\FPL\FPL_S' + season + '_GW1_' + last_GW + '.csv')[['Player',
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


########################################


# SECTION 1.d - TEAMS FANTASY POINTS
team_fantasy_points = pd.read_csv(r'Data\FPL\FPL_S' + season + '_GW1_' + last_GW + '.csv')[['Team', 'Pts.']]
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
seizing_players = cum_data[['Player', 'Player_NPG', 'Player_NPxG']]

# Create the Seizure variable
seizing_players['Seizure'] = seizing_players['Player_NPG'] - seizing_players['Player_NPxG']

# Sorting
seizing_players = seizing_players.sort_values(by='Seizure',
                                              ascending=False)

# Creating a list of the top 10 and worst 10 seizing players
top_seizing_players = seizing_players.head(10)
worst_seizing_players = seizing_players.tail(10)


#############################


# SECTION 2.b - HEAD 2 HEAD PLAYER COMPARISON

# Define the two player name you want to compare
name1 = 'Kane'
name2 = 'Salah'

# Which player is better - player A or player B?
# This question is answered by creating a radar plot comparing two players by multiple aspects

# Choose the categories that will appear on the plot
categories = ['Cost',
              'Goals scored',
              'Assists',
              'Points per match',
              'Form']

# Create a new dataframe containing only the desired categories
radar_data = cum_data[['Player'] + categories]

# Create a list of each player stats
Player1 = radar_data[radar_data['Player'] == name1].values.tolist()[0]
Player2 = radar_data[radar_data['Player'] == name2].values.tolist()[0]

# Add two more columns to each player's df, using the stats we produced earlier: Seizure and Stability
# Seizure
Player1.append(seizing_players['Seizure'][seizing_players['Player'] == name1].values[0])
Player2.append(seizing_players['Seizure'][seizing_players['Player'] == name2].values[0])

# Stability
Player1.append(stable_players['Stability'][stable_players.index == name1].values[0]*10)
Player2.append(stable_players['Stability'][stable_players.index == name2].values[0]*10)

# Update the categories names
categories = categories + ['Seizure', 'Stability']

radar = go.Figure()

radar.add_trace(go.Scatterpolar(
                r=Player1[1:],
                theta=categories,
                fill='toself',
                name=Player1[0]))

radar.add_trace(go.Scatterpolar(
                r=Player2[1:],
                theta=categories,
                fill='toself',
                name=Player2[0]))

radar.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=False,
      range=[min(Player1[1:] + Player2[1:]) - 1, max(Player1[1:] + Player2[1:]) + 1]
    ),
    angularaxis=dict(
        tickfont=dict(size=18)
    )),
  legend=dict(
      yanchor="top",
      y=0.99,
      xanchor="left",
      x=0.85,
      font=dict(size=18)
  ),
  showlegend=True,
  width=1200,
  height=670)

# Show plot
radar.show()

# Export plot
radar.write_image('Visualizations/Radar_' + name1 + '_' + name2 + '.png')


#######################                            SECTION 3 - TEAMS                            #######################


# SECTION 3.a - TEAM OPPORTUNITY SEIZURE

# Which are the teams who are best in seizing goaling opportunities?
# This question is answered by the same methodology as the player opportunity seizure was answered

# Import data and subset relevant columns
seizing_teams = PLT_data[['Team', 'Team_G', 'Team_xG']]

# Create the Seizure variable
seizing_teams['Seizure'] = seizing_teams['Team_G'] - seizing_teams['Team_xG']

# Sorting
seizing_teams = seizing_teams.sort_values(by='Seizure',
                                          ascending=False)


#############################


# SECTION 2.b - HEAD 2 HEAD TEAMS COMPARISON


# Define the two player TEAMS you want to compare
name1 = 'TOT'
name2 = 'LIV'

# Which Team is better - Team A or Team B?
# This question is answered by creating a radar plot comparing two Teams by multiple aspects

# Choose the categories that will appear on the plot
categories = ['Team_PTS',
              'Team_G',
              'Team_GA']

# Create a new dataframe containing only the desired categories
team_radar_data = PLT_data[['Team'] + categories]

# Create a list of each Team stats
Team1 = team_radar_data[team_radar_data['Team'] == name1].values.tolist()[0]
Team2 = team_radar_data[team_radar_data['Team'] == name2].values.tolist()[0]

# Append two more values to each Team's list, using the stats we produced earlier: Seizure and Passes completed (DC)
# Seizure
Team1.append(seizing_teams['Seizure'][seizing_teams['Team'] == name1].values[0])
Team2.append(seizing_teams['Seizure'][seizing_teams['Team'] == name2].values[0])

# DC
Team1.append(PLT_data['Team_DC'][PLT_data['Team'] == name1].values[0]/10)
Team2.append(PLT_data['Team_DC'][PLT_data['Team'] == name2].values[0]/10)

# Fantasy points
Team1.append(team_fantasy_points['Pts.'][team_fantasy_points.index == name1].values[0]/20)
Team2.append(team_fantasy_points['Pts.'][team_fantasy_points.index == name2].values[0]/20)

# # Stability
# Team1.append(stable_Teams['Stability'][stable_Teams.index == name1].values[0]*10)
# Team2.append(stable_Teams['Stability'][stable_Teams.index == name2].values[0]*10)

# Update the categories names
categories = ['Pts.',
              'Goals',
              'Goals against',
              'Passes completed',
              'Seizure',
              'Fantasy points']

team_radar = go.Figure()

team_radar.add_trace(go.Scatterpolar(
                     r=Team1[1:],
                     theta=categories,
                     fill='toself',
                     name=Team1[0]))

team_radar.add_trace(go.Scatterpolar(
                     r=Team2[1:],
                     theta=categories,
                     fill='toself',
                     name=Team2[0]))

team_radar.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=False,
      range=[min(Team1[1:] + Team2[1:]) - 1, max(Team1[1:] + Team2[1:]) + 1]
    ),
    angularaxis=dict(
        tickfont=dict(size=18)
    )),
  legend=dict(
      yanchor="top",
      y=0.99,
      xanchor="left",
      x=0.85,
      font=dict(size=18)
  ),
  showlegend=True,
  width=1200,
  height=670)

# Show plot
team_radar.show()

# Export plot
team_radar.write_image('Visualizations/team_radar_' + name1 + '_' + name2 + '.png')


#################                            SECTION 4 - STATISTICS ACCURACY                           #################

# SECTION 4.a - Players' xG vs. players' goals

# Does the xG stat predicts well the player number of goals
# This is a twofold comparison: 1. xG per game vs. goals per game ; 2. Total xG vs. Total Goals over all games

# Single game xG and goals
sns.scatterplot(x='Player_xG',
                y='Goals scored',
                data=data)

SGW_xG_corr = data.corr()._get_value('Goals scored', 'Player_xG')

# Cumulative xG and goals
sns.regplot(x='Player_xG',
            y='Goals scored',
            data=cum_data)

cum_xG_corr = cum_data.corr()._get_value('Goals scored', 'Player_xG')

# SECTION 4.b - Players' xA vs. players' assists

# Does the xA stat predicts well the players' number of assists
# This is a twofold comparison: 1. xA per game vs. assists per game ; 2. Total xA vs. Total Assists over all games

# Single games data
sns.scatterplot(x='Player_xA',
                y='Assists',
                data=data)

SGW_xA_corr = data.corr()._get_value('Assists', 'Player_xA')

# Cumulative data
sns.regplot(x='Player_xA',
            y='Assists',
            data=cum_data)

cum_xA_corr = cum_data.corr()._get_value('Assists', 'Player_xA')


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


