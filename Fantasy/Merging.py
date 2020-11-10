import os
import pandas as pd
import numpy as np

# First, we'll define a set of paramaters that will allow us
# to modify easily the code from one gameweek to another
season = '21'
previous_GW = '7'
current_GW = '8'

# Set working directory
os.chdir(r'C:\Users\nirgo\Documents\GitHub\Fantasy\Fantasy')

# Import the previous and this week cumulative dataframes
previous_df = pd.read_csv('S' + season + '_GW1_' + previous_GW + '.csv')
current_df = pd.read_csv('S' + season + '_GW1_' + current_GW + '.csv')

# Creating this week gameweek not cumulative dataframe by subtracting the cumulative dataframes
# Creating a list of all the variables that should be subtracted from each other
subtraction_lst = ['Pts.', 'Minutes played', 'Goals scored', 'Assists', 'Clean sheets',
                   'Goals conceded', 'Own goals', 'Penalties saved', 'Penalties missed',
                   'Yellow cards', 'Red cards', 'Saves', 'Bonus', 'Bonus Points System',
                   'Times in Dream Team', 'Transfers in', 'Transfers out']

# Merging the previous and current gameweeks dataframes
temp_GW = pd.merge(current_df,
                   previous_df,
                   on=['Player', 'Team', 'Role'],
                   how='outer',
                   suffixes=['_current', '_previous'])

# Creating an empty dataframe to which the not cumulative values will be passed
GW = pd.DataFrame(columns=list(current_df.columns))

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
Schedule = pd.read_csv('Schedule.csv', index_col=0)

# Inserting a Gameweek column
GW.insert(1, 'Gameweek', current_GW)

# Inserting an empty opponent column in the GW dataframe
GW.insert(3, 'Opponent', 'nan')

# Inserting the relevant opponents from the Schedule df
GW['Opponent'] = [Schedule.loc[team, current_GW] for team in GW['Team']]


##########################################################################################

# Import the PLT with all the relevant team stats
PLT = pd.read_csv(r'League Table\S' + season + '_GW1_' + current_GW + '.csv')

# Merge the PLT to the GW dataframe
GW = pd.merge(GW,
              PLT,
              on=['Team'],
              how='inner')


##########################################################################################


players_df = pd.read_csv(r'Understat\S' + season + '_GW1_' + current_GW + '.csv')

lala = pd.merge(current_df,
                players_df,
                on=['Player', 'Team'],
                how='inner')

players_df2 = players_df.drop(columns='Player')

lala2 = pd.merge(current_df,
                 players_df2,
                 left_on=['Player', 'Team'],
                 right_on=['Player_first', 'Team'],
                 how='inner')

lala_final = pd.concat([lala, lala2])

players_lst = list(lala_final['Player'])


players_df[~players_df['Player'].isin(list(lala_final['Player']))]

lala_final['Player'].isin(list(players_df['Player']) + list(players_df['Player_first']))
