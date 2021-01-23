import pandas as pd
import numpy as np
import re

# First, we set the season, current gameweek and previous gameweek variables
season = '21'
previous_GW = '18'
current_GW = '19'

# Import the previous and this week cumulative dataframes
cum_prev_df = pd.read_csv(r'FPL/FPL_S' + season + '_GW1_' + previous_GW + '.csv')
cum_curr_df = pd.read_csv(r'FPL/FPL_S' + season + '_GW1_' + current_GW + '.csv')

# Importing the previous and current cumulative players xG stats from the Understat site
cum_prev_xG_df = pd.read_csv(r'Understat\xG_S' + season + '_GW1_' + previous_GW + '.csv')
cum_curr_xG_df = pd.read_csv(r'Understat\xG_S' + season + '_GW1_' + current_GW + '.csv')

# Import the previous and current cumulative PLT's with all the relevant team stats
cum_prev_PLT = pd.read_csv(r'PLT\PLT_S' + season + '_GW1_' + previous_GW + '.csv')
cum_curr_PLT = pd.read_csv(r'PLT\PLT_S' + season + '_GW1_' + current_GW + '.csv')

# First, we'll drop some column on the xG's dataframes we already have on the FPL dataframes
drop_col_lst = ['Player_Minutes played',
                'Player_Goals scored',
                'Player_Assists']

cum_prev_xG_df = cum_prev_xG_df.drop(columns=drop_col_lst)
cum_curr_xG_df = cum_curr_xG_df.drop(columns=drop_col_lst)

# Now, we'll start the merging process
# First, We'll merge using the full player name
full_name = pd.merge(cum_curr_df,
                     cum_curr_xG_df,
                     on=['Player', 'Team'],
                     how='inner')

# This got us 379 out of 410 players merged.
# Now, we'll break their names to first and last names, and try to merge by them
cum_curr_xG_df.insert(1, 'Player_first', 'nan')
for i in range(0, len(cum_curr_xG_df)):
    cum_curr_xG_df['Player_first'][i] = re.split('[ ]', cum_curr_xG_df['Player'][i])[0]
    try:
        cum_curr_xG_df['Player'][i] = re.split('[ ]', cum_curr_xG_df['Player'][i])[1] + ' ' + \
                                     re.split('[ ]', cum_curr_xG_df['Player'][i])[2] + ' ' + \
                                     re.split('[ ]', cum_curr_xG_df['Player'][i])[3]
    except IndexError:
        pass
        try:
            cum_curr_xG_df['Player'][i] = re.split('[ ]', cum_curr_xG_df['Player'][i])[1] + ' ' +\
                                         re.split('[ ]', cum_curr_xG_df['Player'][i])[2]
        except IndexError:
            pass
            try:
                cum_curr_xG_df['Player'][i] = re.split('[ ]', cum_curr_xG_df['Player'][i])[1]
            except IndexError:
                pass

# Inner merge the xG df with the FPL df based on the last name of the players
# First, there are few players with incorrect team names, so we'll change them and then merge.
cum_curr_xG_df['Team'][cum_curr_xG_df['Player'] == 'Walcott'] = 'SOU'
cum_curr_xG_df['Team'][cum_curr_xG_df['Player'] == 'Loftus-Cheek'] = 'FUL'

last_name = pd.merge(cum_curr_df,
                     cum_curr_xG_df,
                     on=['Player', 'Team'],
                     how='inner')

# Concatenating the two dfs while dropping the first name column, which interfers dropping duplicates
curr_merged_df = pd.concat([full_name, last_name]).drop(columns=['Player_first']).drop_duplicates()

# Then, we create another xG df without the Player column, to try merging based on the players' first name
cum_curr_xG_df2 = cum_curr_xG_df.drop(columns='Player')
first_name = pd.merge(cum_curr_df,
                      cum_curr_xG_df2,
                      left_on=['Player', 'Team'],
                      right_on=['Player_first', 'Team'],
                      how='inner')

# Again, we concatenate the first_name df with the existing curr_merged_df merged df
curr_merged_df = pd.concat([curr_merged_df, first_name]).drop(columns=['Player_first']).drop_duplicates()

# We're still missing 14 players to fully merge the cum_curr_xG_df and the cum_curr_df. Let's track them
miss_df = cum_curr_xG_df[['Player', 'Player_first']][(~cum_curr_xG_df['Player'].isin(curr_merged_df['Player'])) &
                                             (~cum_curr_xG_df['Player_first'].isin(curr_merged_df['Player']))]

# Creating manually a dictionary to replace the wrong player names with right ones
miss_dct = {'Mitrovic': 'Mitrović',
            'Reid': 'Decordova-Reid',
            'Saiss': 'Saïss',
            'Pepe': 'Pépé',
            'Konsa Ngoyo': 'Konsa',
            'Berg Gudmundsson': 'Gudmundsson',
            'Elmohamady': 'El Mohamady',
            'Gomes': 'André Gomes',
            'Rodri': 'Rodrigo',
            'Hegazy': 'Hegazi',
            'Martinez': 'Martínez',
            'Kepa': 'Arrizabalaga',
            'Zambo': 'Anguissa',
            'Vinicius': 'Carlos'}

# Replace the wrong values player names by mapping
xG_missing = cum_curr_xG_df[cum_curr_xG_df['Player'].isin(miss_dct.keys())]
xG_missing['Player'] = xG_missing['Player'].map(miss_dct)

# Merging the curr_merged_df df with the xG_missing df, and then concatenating
missing_name = pd.merge(cum_curr_df,
                        xG_missing,
                        on=['Player', 'Team'],
                        how='inner')

curr_merged_df = pd.concat([curr_merged_df, missing_name]).drop(columns=['Player_first']).drop_duplicates().reset_index(drop=True)

# Merging the cumulative team stats to the curr_merged_df
curr_merged_df = pd.merge(curr_merged_df,
                          cum_curr_PLT,
                          on=['Team'],
                          how='inner')

# We'll finish by exporting to csv file the curr_merged_df, which will be useful for some of our models
curr_merged_df.to_csv(r'Cumulative Merged Data\CMD_S' + season + '_GW_' + current_GW + '.csv', index=False)

#######################################################################################################################



# Now, we'll repeat the process for the previous gameweek xG and FPL dataframes

# First, we'll merge using the full player name
full_name = pd.merge(cum_prev_df,
                     cum_prev_xG_df,
                     on=['Player', 'Team'],
                     how='inner')

# This got us 379 out of 410 players merged.
# Now, we'll break their names to first and last names, and try to merge by them
cum_prev_xG_df.insert(1, 'Player_first', 'nan')
for i in range(0, len(cum_prev_xG_df)):
    cum_prev_xG_df['Player_first'][i] = re.split('[ ]', cum_prev_xG_df['Player'][i])[0]
    try:
        cum_prev_xG_df['Player'][i] = re.split('[ ]', cum_prev_xG_df['Player'][i])[1] + ' ' + \
                                     re.split('[ ]', cum_prev_xG_df['Player'][i])[2] + ' ' + \
                                     re.split('[ ]', cum_prev_xG_df['Player'][i])[3]
    except IndexError:
        pass
        try:
            cum_prev_xG_df['Player'][i] = re.split('[ ]', cum_prev_xG_df['Player'][i])[1] + ' ' +\
                                         re.split('[ ]', cum_prev_xG_df['Player'][i])[2]
        except IndexError:
            pass
            try:
                cum_prev_xG_df['Player'][i] = re.split('[ ]', cum_prev_xG_df['Player'][i])[1]
            except IndexError:
                pass

# Inner merge the xG df with the FPL df based on the last name of the players
# First, there are few players with incorrect team names, so we'll change them and then merge.
cum_prev_xG_df['Team'][cum_prev_xG_df['Player'] == 'Walcott'] = 'SOU'
cum_prev_xG_df['Team'][cum_prev_xG_df['Player'] == 'Loftus-Cheek'] = 'FUL'

last_name = pd.merge(cum_prev_df,
                     cum_prev_xG_df,
                     on=['Player', 'Team'],
                     how='inner')

# Concatenating the two dfs while dropping the first name column, which interfers dropping duplicates
prev_merged_df = pd.concat([full_name, last_name]).drop(columns=['Player_first']).drop_duplicates()

# Then, we create another xG df without the Player column, to try merging based on the players' first name
cum_prev_xG_df2 = cum_prev_xG_df.drop(columns='Player')
first_name = pd.merge(cum_prev_df,
                      cum_prev_xG_df2,
                      left_on=['Player', 'Team'],
                      right_on=['Player_first', 'Team'],
                      how='inner')

# Again, we concatenate the first_name df with the existing prev_merged_df merged df
prev_merged_df = pd.concat([prev_merged_df, first_name]).drop(columns=['Player_first']).drop_duplicates()

# We're still missing 14 players to fully merge the cum_prev_xG_df and the cum_prev_df. Let's track them
miss_df = cum_prev_xG_df[['Player', 'Player_first']][(~cum_prev_xG_df['Player'].isin(prev_merged_df['Player'])) &
                                             (~cum_prev_xG_df['Player_first'].isin(prev_merged_df['Player']))]

# Replace the wrong values player names by mapping
xG_missing = cum_prev_xG_df[cum_prev_xG_df['Player'].isin(miss_dct.keys())]
xG_missing['Player'] = xG_missing['Player'].map(miss_dct)

# Merging the prev_merged_df df with the xG_missing df, and then concatenating
missing_name = pd.merge(cum_prev_df,
                        xG_missing,
                        on=['Player', 'Team'],
                        how='inner')

prev_merged_df = pd.concat([prev_merged_df, missing_name]).drop(columns=['Player_first']).drop_duplicates().reset_index(drop=True)

# We'll finish by merging the cumulative team stats to the prev_merged_df
prev_merged_df = pd.merge(prev_merged_df,
                          cum_prev_PLT,
                          on=['Team'],
                          how='inner')


########################################################################################################################


# Now, we'll crete the final Gameweek dataframe by subtracting the cumulative dataframes

# Creating a list of all the variables that should be subtracted from each other
# List of variables of the FPL stats that should be subtracted
FPL_subtract = ['Pts.', 'Minutes played', 'Goals scored', 'Assists', 'Clean sheets',
                'Goals conceded', 'Own goals', 'Penalties saved', 'Penalties missed',
                'Yellow cards', 'Red cards', 'Saves', 'Bonus', 'Bonus Points System',
                'Times in Dream Team', 'Transfers in', 'Transfers out']

# List of variables of the player xG stats that should be subtracted
xG_subtract = ['Player_NPG', 'Player_xG', 'Player_NPxG',
               'Player_xA', 'Player_xGChain', 'Player_xGBuildup']

# List of variables of the Team stats that should be subtracted
PLT_subtract = ['Team_M', 'Team_W', 'Team_D', 'Team_L', 'Team_G', 'Team_GA',
                'Team_PTS', 'Team_xG', 'Team_NPxG', 'Team_xGA', 'Team_NPxGA',
                'Team_NPxGD', 'Team_PPDA', 'Team_OPPDA', 'Team_DC', 'Team_ODC', 'Team_xPTS']

# Concatenating the three list to the final subtraction list
subtraction_lst = FPL_subtract + xG_subtract + PLT_subtract

# Merging the previous and current gameweeks dataframes
temp_GW = pd.merge(curr_merged_df,
                   prev_merged_df,
                   on=['Player', 'Team', 'Role'],
                   how='outer',
                   suffixes=['_current', '_previous'])

# Creating an empty dataframe to which the not cumulative values will be passed
GW = pd.DataFrame(columns=list(curr_merged_df.columns))

# Iterating through the columns and passing them to the final dataframe
for col in list(GW.columns):
    if col in subtraction_lst:
        GW[col] = temp_GW[col + '_current'] - temp_GW[col + '_previous']
    elif col in ['Player', 'Team', 'Role']:
        GW[col] = temp_GW[col]
    else:
        GW[col] = temp_GW[col + '_current']

###########################################################################################

# Import the schedule of all the teams
Schedule = pd.read_csv(r'Schedule\Schedule_S' + season + '.csv', index_col=0)

# Inserting a Gameweek and a Season column
GW.insert(1, 'Gameweek', current_GW)
GW.insert(1, 'Season', season)

# Inserting an empty opponent column in the GW dataframe
GW.insert(3, 'Opponent', 'nan')

# Inserting the relevant opponents from the Schedule df
GW['Opponent'] = [Schedule.loc[team, current_GW] for team in GW['Team']]

# Inserting Home column, which will contain a dummy variable: 1 for home game, 0 for away game
# Classification to Home/Away games is done based on the opponent team's name being uppercase/lowercase
GW.insert(5, 'Home', 0)
for i in GW.index.tolist():
    try:
        if GW['Opponent'][i].isupper():
            GW['Home'][i] = 1
        else:
            pass
    except AttributeError:
        GW['Home'][i] = np.nan

##########################################################################################

# Create a dataframe which will contain the average stats of the team. This stats will be merged to the dataframe
# as the opponent team stats, in order to get a better understanding of the quality of the opponent team
avg_opponent = cum_curr_PLT.drop(columns=['Team_W', 'Team_D', 'Team_L'])

# Dividing and changing column names to start with "Opp_Avg" instead of "Team"
for elem in avg_opponent.columns.drop(['Team_Ranking', 'Team', 'Team_M']):
    avg_opponent[elem] = avg_opponent[elem] / avg_opponent['Team_M']
    avg_opponent = avg_opponent.rename(columns={elem: str(elem).replace('Team', 'Opp_Avg')})

avg_opponent = avg_opponent.rename(columns={'Team_Ranking': 'Opp_Ranking',
                                            'Team': 'Opponent'})

# Drop the opponent number of matches stats, which doesn't interest us.
avg_opponent = avg_opponent.drop(columns='Team_M')

# Merging this information to the main dataframe, with the Opponent column on the left and the Team column on the right

# Before merging, we'll have to uppercase the team names in the GW's Opponent column, otherwise merge won't work
GW['Opponent'] = GW['Opponent'].str.upper()

# Merging
GW = pd.merge(GW,
              avg_opponent,
              on='Opponent',
              how='inner')

# Dropping the percent sign off the Sel. column in both dataframes.
# This will allow us to convert the column to numeric type
GW['Sel.'] = [float(str(GW['Sel.'][i]).replace('%', '')) for i in GW.index.tolist()]

# Exporting the final GW dataframe to a single gameweek csv file
GW.to_csv(r'Single GW\SGW_S' + season + '_GW_' + current_GW + '.csv', index=False)

# Appending the final GW dataframe to the Final Data file, which contains all the gameweeks
Final_Data = pd.read_csv('Final Data.csv')

# Verifying the GW dataframe is in the same column order as the final data one
GW = GW[Final_Data.columns]

# Concatenating and saving
Final_Data = pd.concat([Final_Data, GW])

Final_Data.to_csv('Final Data.csv', index=False)

# Finally, we'll create a dataframe which contains the average player, team and opponent data until the previous GW
# And the current gameweek points. This data will be used for most of our models
Model_Data = prev_merged_df.rename(columns={'Pts.': 'Cum Pts.'})

# Inserting a Gameweek and a Season column
Model_Data.insert(1, 'Gameweek', current_GW)
Model_Data.insert(1, 'Season', season)

# Inserting an empty opponent column in the Model_Data dataframe
Model_Data.insert(3, 'Opponent', 'nan')

# Inserting the relevant opponents from the Schedule df
Model_Data['Opponent'] = [Schedule.loc[team, current_GW] for team in Model_Data['Team']]

# Inserting Home column, which will contain a dummy variable: 1 for home game, 0 for away game
# Classification to Home/Away games is done based on the opponent team's name being uppercase/lowercase
Model_Data.insert(5, 'Home', 0)
for i in Model_Data.index.tolist():
    try:
        if Model_Data['Opponent'][i].isupper():
            Model_Data['Home'][i] = 1
        else:
            pass
    except AttributeError:
        Model_Data['Home'][i] = np.nan

# Create a dataframe which will contain the average stats of the team. This stats will be merged to the dataframe
# as the opponent team stats, in order to get a better understanding of the quality of the opponent team
avg_opponent_2 = cum_prev_PLT.drop(columns=['Team_W', 'Team_D', 'Team_L'])

# Dividing and changing column names to start with "Opp_Avg" instead of "Team"
for elem in avg_opponent_2.columns.drop(['Team_Ranking', 'Team', 'Team_M']):
    avg_opponent_2[elem] = avg_opponent_2[elem] / avg_opponent_2['Team_M']
    avg_opponent_2 = avg_opponent_2.rename(columns={elem: str(elem).replace('Team', 'Opp_Avg')})

avg_opponent_2 = avg_opponent_2.rename(columns={'Team_Ranking': 'Opp_Ranking',
                                                'Team': 'Opponent'})

# Drop the opponent number of matches stats, which doesn't interest us.
avg_opponent_2 = avg_opponent_2.drop(columns='Team_M')

# Merging this information to the main dataframe, with the Opponent column on the left and the Team column on the right

# Before merging, we'll have to uppercase the team names in the GW's Opponent column, otherwise merge won't work
Model_Data['Opponent'] = Model_Data['Opponent'].str.upper()

# Merging the opponent stats
Model_Data = pd.merge(Model_Data,
                      avg_opponent_2,
                      on='Opponent',
                      how='inner')

# Merging the fantasy points stats for this gameweek
Model_Data = pd.merge(Model_Data,
                      GW[['Player', 'Team', 'Pts.']],
                      on=['Player', 'Team'],
                      how='inner')

# Dropping Duplicates
Model_Data = Model_Data.drop_duplicates()

# Exporting
Model_Data.to_csv(r'Model Data\Single GW\MD_S' + season + '_GW1_' + current_GW + '.csv', index=False)

# Appending the final GW dataframe to the Final Data file, which contains all the gameweeks
Model_Data_Final = pd.read_csv(r'Model Data\Model Data - Final.csv')

# Verifying the GW dataframe is in the same column order as the final data one
Model_Data = Model_Data[Model_Data_Final.columns]

# Concatenating and saving
Model_Data_Final = pd.concat([Model_Data_Final, Model_Data])

Model_Data_Final.to_csv(r'Model Data\Model Data - Final.csv', index=False)
