import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN, KMeans
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go

# Setting variables which are relevant for the entire analysis
season = '22'
last_GW = '5'
minutes_threshold = 150

# Import data
# We'll use three kinds of data, presented by three different dfs, in this code
# No 1. - Single gameweeks data, i.e, not cumulative data
data = pd.read_csv(r'Data\Final Data.csv')
data = data.drop_duplicates()

# No 2. - Cumulative data
cum_data = pd.read_csv(r'Data\FPL\FPL_S' + season + '_GW1_' + last_GW + '.csv')
cum_data.drop_duplicates()

# No 3. - Teams data
PLT_data = pd.read_csv(r'Data\PLT\PLT_S' + season + '_GW1_' + last_GW + '.csv')
PLT_data.drop_duplicates()


######################                            SECTION 1 - FANTASY                            ######################


class Visualizing:
    """ Class for apply the data manipulations necessary for creating some of the insights we're interested in """

    def __init__(self, season, last_gw):
        self.season = season
        self.last_gw = last_gw

    def stability_scores(self, ts_data, pts_thresh, minutes_thresh):
        """ Create data frame containing fantasy points stability scores for all players.
            These scores ranges from 0 (least stable) to 100 (most stable).
            They are created using players' standard deviations which are passed to MinMax scaler """

        # Calculate the cumulative number of minutes each player played
        cum_minutes = ts_data.groupby(by='Player').agg({'Minutes played': [sum]})
        cum_minutes.columns = list(map(''.join, cum_minutes.columns.values))

        # Drop players who didn't play the average minutes per game defined in the minutes threshold
        cum_minutes = cum_minutes[cum_minutes['Minutes playedsum'] >= minutes_thresh*self.last_gw]
        ts_data = ts_data[ts_data['Player'].isin(cum_minutes.index.tolist())]

        # Pivot the time series data
        pvt_data = pd.pivot_table(ts_data[['Player', 'Gameweek', 'Pts.']],
                                  index='Player',
                                  columns='Gameweek',
                                  values='Pts.')

        # Calculating the Mean and Standard Deviation for each player
        pvt_data['Mean'] = pvt_data.mean(axis=1,
                                         skipna=True)
        pvt_data['Std'] = pvt_data.std(axis=1,
                                       skipna=True)

        # Drop players with Std = 0
        pvt_data = pvt_data[pvt_data['Std'] != 0]

        # Multiply the Std column by -1 to assign the lowest std (i.e the most stable player) the highest value
        pvt_data['Minus Std'] = pvt_data['Std']*(-1)

        # Use the MinMax scaler to produce a score ranging from 0 to 1 (where 0 is the most unstable player)
        scaler = MinMaxScaler()
        pvt_data['Stability'] = scaler.fit_transform(pvt_data['Minus Std'].values.reshape(-1, 1))

        # Multiply the Stability index with 100 to create stability score ranging from 0 to 100
        pvt_data['Stability'] = pvt_data['Stability']*100

        # Drop players which their mean points per game is lower than the points threshold defined and sort by stability
        stability_data = pvt_data[pvt_data['Mean'] >= pts_thresh].sort_values(by='Stability',
                                                                              ascending=False)

        # Delete irrelevant columns and round numbers
        stability_data = stability_data[['Stability', 'Mean']].round(2)

        return stability_data

    def value_for_money(self, ts_data, role_relative=True):
        """ This function computes the value each player delivered relative to his cost.
            This is computed using a linear regression model, where value is calculated as the player's residual """

        # Pivot the time series data
        pvt_data = pd.pivot_table(ts_data[['Player', 'Gameweek', 'Role', 'Pts.', 'Cost']],
                                  index=['Player', 'Role'],
                                  columns='Gameweek',
                                  values=['Pts.', 'Cost'])

        # Compute mean points and cost per game
        pvt_data['Sum pts.'] = pvt_data.filter(like='Pts').sum(axis=1,
                                                                skipna=True)

        pvt_data['Mean cost'] = pvt_data.filter(like='Cost').mean(axis=1,
                                                                  skipna=True)

        # Subset only player names and roles
        reg_data = pd.DataFrame({'Player': pvt_data.index.get_level_values(0),
                                 'Role': pvt_data.index.get_level_values(1),
                                 'Pts.': pvt_data['Sum pts.'],
                                 'Cost': pvt_data['Mean cost']}).dropna().reset_index(drop=True)

        # Create linear regression model
        lm = LinearRegression()

        # For each role create a regression object and return vector of residuals
        resid_lst = []

        if role_relative == True:

            for role in reg_data['Role'].unique():
    
                # Subset only current role data
                role_data = reg_data[reg_data['Role'] == role].reset_index(drop=True)
    
                # Create X and y vectors
                X = role_data['Cost'].values.reshape(-1, 1)
                y = role_data['Pts.'].values.reshape(-1, 1)
    
                # Fit regression
                reg = lm.fit(X, y)
    
                # Append results to list
                resid_lst.append(pd.DataFrame({'Player': role_data['Player'],
                                               'Cost': role_data['Cost'],
                                               'Pts.': role_data['Pts.'],
                                               'Value': (y - reg.predict(X)).ravel()}))
    
            # Concatenate all data frames (one df for each role) to big final residuals data frame
            residuals = pd.concat(resid_lst).sort_values(by='Value',
                                                         ascending=False).reset_index(drop=True)

        elif role_relative == False:

            # Create X and y vectors
            X = reg_data['Cost'].values.reshape(-1, 1)
            y = reg_data['Pts.'].values.reshape(-1, 1)

            # Fit regression
            reg = lm.fit(X, y)

            # Append results to list
            resid_lst.append(pd.DataFrame({'Player': reg_data['Player'],
                                           'Cost': reg_data['Cost'],
                                           'Pts.': reg_data['Pts.'],
                                           'Value': (y - reg.predict(X)).ravel()}))

            # Concatenate all data frames (one df for each role) to big final residuals data frame
            residuals = pd.concat(resid_lst).sort_values(by='Value',
                                                         ascending=False).reset_index(drop=True)

        return residuals

    def opportunity_seizure(self, cum_data, role_relative=True):
        """ This function computes the opportunity seizure of each player.
            This is computed using a linear regression model, where expected goals are regressed against actual goals.
            Opportunity seizure is calculated as the player's residual """

        # Pivot the time series data
        pvt_data = pd.pivot_table(cum_data[['Player', 'Gameweek', 'Role', 'Goals scored', 'Player_xG']],
                                  index=['Player', 'Role'],
                                  columns='Gameweek',
                                  values=['Goals scored', 'Player_xG'])

        # Subset only player names and roles
        reg_data = pd.DataFrame({'Player': pvt_data.index.get_level_values(0),
                                 'Role': pvt_data.index.get_level_values(1),
                                 'Goals': pvt_data['Goals scored'],
                                 'xG': pvt_data['Player_xG']}).dropna().reset_index(drop=True)

        # Create linear regression model
        lm = LinearRegression()

        # For each role create a regression object and return vector of residuals
        resid_lst = []

        if role_relative == True:

            for role in reg_data['Role'].unique():

                # Subset only current role data
                role_data = reg_data[reg_data['Role'] == role].reset_index(drop=True)

                # Create X and y vectors
                X = role_data['xG'].values.reshape(-1, 1)
                y = role_data['Goals'].values.reshape(-1, 1)

                # Fit regression
                reg = lm.fit(X, y)

                # Append results to list
                resid_lst.append(pd.DataFrame({'Player': role_data['Player'],
                                               'xG': role_data['xG'],
                                               'Goals': role_data['Goals'],
                                               'Seizure': (y - reg.predict(X)).ravel()}))

            # Concatenate all data frames (one df for each role) to big final residuals data frame
            residuals = pd.concat(resid_lst).sort_values(by='Seizure',
                                                         ascending=False).reset_index(drop=True)
        elif role_relative == False:

            # Create X and y vectors
            X = reg_data['xG'].values.reshape(-1, 1)
            y = reg_data['Goals'].values.reshape(-1, 1)

            # Fit regression
            reg = lm.fit(X, y)

            # Append results to list
            resid_lst.append(pd.DataFrame({'Player': reg_data['Player'],
                                           'xG': reg_data['xG'],
                                           'Goals': reg_data['Goals'],
                                           'Seizure': (y - reg.predict(X)).ravel()}))

            # Concatenate all data frames (one df for each role) to big final residuals data frame
            residuals = pd.concat(resid_lst).sort_values(by='Seizure',
                                                         ascending=False).reset_index(drop=True)

        return residuals

    def team_pts(self, ts_data):
        """ Calculate the sum of fantasy points each team scored during the season """

        # Group by teams and sum the points
        team_pts = ts_data.groupby(by='Team').agg({'Pts.': [sum]})

        # Change column names
        team_pts.columns = list(map(''.join, team_pts.columns.values))
        team_pts.columns = ['Pts.']

        return team_pts.sort_values(by='Pts.',
                                    ascending=False)




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
g = sns.FacetGrid(col='Role',
                  hue='Role',
                  sharex=False,
                  sharey=False,
                  data=cum_data[cum_data['Role'] != 'GKP'])

g.map_dataframe(sns.regplot,
                x='Player_xG',
                y='Goals scored')

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

# Regplot of the Fantasy Cost vs. Fantasy Points
role_lst = ['GKP', 'DEF', 'MID', 'FWD']

# Add column caculating the points per gameweek
cum_data['Points per gw'] = cum_data['Pts.']/int(last_GW)

g = sns.lmplot(x='Cost',
               y='Points per gw',
               hue='Role',
               col='Role',
               col_wrap=2,
               col_order=['GKP', 'DEF', 'MID', 'FWD'],
               sharex=False,
               data=cum_data)


for ax, role in zip(g.axes.ravel(), role_lst):
    for t, x, y in cum_data[cum_data['Role'] == role][['Player', 'Cost', 'Points per gw']].values.tolist():
        ax.annotate(t, (x, y), fontsize=6)

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


