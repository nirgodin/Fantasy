import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression


class PreProcessing:
    """ Class for preprocessing data to time series format and merging in additional information from other sources """

    def __init__(self, season, first_gw, last_gw):
        self.season = season
        self.first_gw = first_gw
        self.last_gw = last_gw

    def fpl_concat(self):
        """ Concatenate different FPL (Fantasy Premier League) data files to a single dataframe """

        # Create empty list to append dataframes
        df_lst = []

        # Iterate through gameweeks and add each gameweek to dataframes list
        for gw in range(5, self.last_gw + 1):
            path = r'Data/FPL/FPL_S' + str(self.season) + '_GW1_' + str(gw) + '.csv'
            df = pd.read_csv(path)
            df.insert(1, 'Gameweek', str(gw))
            df.insert(1, 'Season', self.season)
            df_lst.append(df)

        return pd.concat(df_lst).reset_index(drop=True)

    def plt_concat(self):
        """ Concatenate different PLT (teams data information) data files to a single dataframe """

        # Create empty list to append dataframes
        df_lst = []

        # Iterate through gameweeks and add each gameweek to dataframes list
        for gw in range(5, self.last_gw):
            path = r'Data/PLT/PLT_S' + str(self.season) + '_GW1_' + str(gw) + '.csv'
            df = pd.read_csv(path)
            df.insert(1, 'Gameweek', str(gw))
            df.insert(1, 'Season', self.season)

            df_lst.append(df)

        return pd.concat(df_lst).reset_index(drop=True)

    def schedule_melt(self):
        """ Melt schdule data to long format, for easy merging with other data frames """

        # Import data
        schedule = pd.read_csv(r'Data/Schedule/Schedule_S21.csv')

        # Transform strings to uppercase
        schedule = schedule.applymap(func=lambda x: str.upper(x),
                                     na_action='ignore')

        # Melt data and return it in long format
        return pd.melt(schedule,
                       id_vars='Team',
                       var_name='Gameweek',
                       value_name='Opponent')

    def merging(self, fpl_data, plt_data, schedule):
        """ Merge all different data sources - FPL, teams and opponent teams - to one dataframe """

        # First - Merge FPL data with schedule
        data = pd.merge(left=fpl_data,
                        right=schedule,
                        how='left',
                        left_on=['Team', 'Gameweek'],
                        right_on=['Team', 'Gameweek']
                        )

        # Second - Merge with teams data
        data = pd.merge(left=data,
                        right=plt_data,
                        how='left',
                        left_on=['Team', 'Gameweek', 'Season'],
                        right_on=['Team', 'Gameweek', 'Season']
                        )

        # Third - Create Opponent dataframe and change colnames of PLT data
        opp_data = plt_data.copy()
        opp_data.columns = [col.replace('Team', 'Opponent') for col in opp_data.columns]

        for opp in data['Opponent']:
            try:
                opp = opp.upper
            except AttributeError:
                pass

        # Fourth - Merge data with opponent data and return it
        return pd.merge(left=data,
                        right=opp_data,
                        how='left',
                        left_on=['Opponent', 'Gameweek', 'Season'],
                        right_on=['Opponent', 'Gameweek', 'Season']
                        )

    def dummies(self, data):
        """ Transform role variable to dummies """

        Role = pd.get_dummies(data['Role'])
        return pd.concat([data, Role], axis=1)

    def interactions(self, data):
        """ Add interaction features, based on player roles """

        # For GKP and DEF - interaction with teams Goals Against
        data['GKP_Team_GA'] = data['GKP'] * data['Team_GA']
        data['DEF_Team_GA'] = data['DEF'] * data['Team_GA']

        # For GKP and DEF - interaction with Opponentonents Goals
        data['GKP_Opponent_G'] = data['GKP'] * data['Opponent_G']
        data['DEF_Opponent_G'] = data['DEF'] * data['Opponent_G']

        # For MID and FWD - interaction with team Goals
        data['MID_Team_G'] = data['MID'] * data['Team_G']
        data['FWD_Team_G'] = data['FWD'] * data['Team_G']

        # For MID and FWD - interaction with Opponentonent Goals Against
        data['MID_Opponent_GA'] = data['MID'] * data['Opponent_GA']
        data['FWD_Opponent_GA'] = data['FWD'] * data['Opponent_GA']

        return data

    def pivoting(self, data, var_lst):
        """ Pivot dataframe to time series format """

        # Create empty list to append dataframes
        df_lst = []

        # Iterate through unique player names and create pivoted dataframe for each one
        for player in data['Player'].unique():
            player_df = pd.pivot_table(data=data[data['Player'] == player].reset_index(),
                                       index='Gameweek',
                                       values=var_lst
                                       )

            # Append pivoted player dataframe to df_lst
            df_lst.append(player_df)

        return pd.concat(df_lst)

    def subtracting(self, concat_data, subtract_vars_lst, drop_first_gw=True):
        """ Transform cumulative data to single gw data.
            This is done by subtracting each gameweek cumulative stats with the previous gameweek cumulative stats.
            After iterating through all the subtract vars, an outer join is performed to produce a full data frame
            containing all the relevant data """

        # Create list of gameweeks in the concatenated data
        gw_lst = [str(gw) for gw in list(range(self.first_gw, self.last_gw + 1))]

        # Create empty list to store ready data frames
        df_lst = []

        # Iterate through the subtract vars list
        for var in subtract_vars_lst:

            if var in subtract_vars_lst:

                # Pivot the data
                pvt_data = pd.pivot_table(data=concat_data[['Gameweek', 'Player', var]],
                                          values=var,
                                          index='Player',
                                          columns='Gameweek')

                # Sort the pivoted data by gameweeks order defined in the gw list
                pvt_data = pvt_data[gw_lst]

                # Create a copy of the original data frame and drop the first gameweek
                sgw_var_data = pvt_data.copy()

                if drop_first_gw:
                    sgw_var_data = sgw_var_data.drop(columns=gw_lst[0])

                # Subtract each column from it's previous one
                for gw in sgw_var_data.columns:
                    sgw_var_data[gw] = pvt_data[gw] - pvt_data[str(int(gw) - 1)]

                # Transform the index player names into an actual column
                sgw_var_data['Player'] = sgw_var_data.index

                # Melt the single gameweek data back to long format
                long_var_data = pd.melt(sgw_var_data,
                                        id_vars='Player',
                                        value_vars=sgw_var_data.drop(columns='Player').columns,
                                        var_name='Gameweek',
                                        value_name=var)

                # Transform Player and Gameweek column to indexes
                long_var_data.index = long_var_data[['Player', 'Gameweek']]
                long_var_data = long_var_data.drop(columns=['Player', 'Gameweek'])

            # Add long var data frame to the df_lst
            df_lst.append(long_var_data)

        # Concat data frames in df_lst along columns axis (axis 1)
        subtracted_data = pd.concat(df_lst,
                                    axis=1,
                                    join='outer')

        # Create Player and Gameweek columns from index and reset the index
        subtracted_data['Player'] = [idx[0] for idx in subtracted_data.index.get_level_values(0)]
        subtracted_data['Gameweek'] = [idx[1] for idx in subtracted_data.index.get_level_values(0)]
        subtracted_data = subtracted_data.reset_index(drop=True)

        # Create data frame with the non subtracted data
        non_subtracted_data = concat_data.drop(columns=subtract_vars_lst)

        # Merge subtract and non subtract data
        final = pd.merge(left=subtracted_data,
                         right=non_subtracted_data,
                         on=['Player', 'Gameweek'],
                         how='left')

        return final


class Insights:
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
        cum_minutes = cum_minutes[cum_minutes['Minutes playedsum'] >= minutes_thresh * self.last_gw]
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
        pvt_data['Minus Std'] = pvt_data['Std'] * (-1)

        # Use the MinMax scaler to produce a score ranging from 0 to 1 (where 0 is the most unstable player)
        scaler = MinMaxScaler()
        pvt_data['Stability'] = scaler.fit_transform(pvt_data['Minus Std'].values.reshape(-1, 1))

        # Multiply the Stability index with 100 to create stability score ranging from 0 to 100
        pvt_data['Stability'] = pvt_data['Stability'] * 100

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

        if role_relative:

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

        elif not role_relative:

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

        if role_relative:

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

        elif not role_relative:

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
