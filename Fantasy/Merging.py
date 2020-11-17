import os
import pandas as pd
import numpy as np
import re

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

# Importing the players xG stats from the Understat site
xG_df = pd.read_csv(r'Understat\S' + season + '_GW1_' + current_GW + '.csv')

# First, we'll merge using the full player name
full_name = pd.merge(current_df,
                     xG_df,
                     on=['Player', 'Team'],
                     how='inner')

# This got us 379 out of 410 players merged.
# Now, we'll break their names to first and last names, and try to merge by them
xG_df.insert(1, 'Player_first', 'nan')
for i in range(0, len(xG_df)):
    xG_df['Player_first'][i] = re.split('[ ]', xG_df['Player'][i])[0]
    try:
        xG_df['Player'][i] = re.split('[ ]', xG_df['Player'][i])[1] + ' ' + \
                                     re.split('[ ]', xG_df['Player'][i])[2] + ' ' + \
                                     re.split('[ ]', xG_df['Player'][i])[3]
    except IndexError:
        pass
        try:
            xG_df['Player'][i] = re.split('[ ]', xG_df['Player'][i])[1] + ' ' +\
                                         re.split('[ ]', xG_df['Player'][i])[2]
        except IndexError:
            pass
            try:
                xG_df['Player'][i] = re.split('[ ]', xG_df['Player'][i])[1]
            except IndexError:
                pass

# Inner merge the xG df with the FPL df based on the last name of the players
last_name = pd.merge(current_df,
                     xG_df,
                     on=['Player', 'Team'],
                     how='inner')

# Concatenating the two dfs while dropping the first name column, which interfers dropping duplicates
xG_FPL = pd.concat([full_name, last_name]).drop(columns=['Player_first']).drop_duplicates()

# Then, we create another xG df without the Player column, to try merging based on the players' first name
xG_df2 = xG_df.drop(columns='Player')
first_name = pd.merge(current_df,
                      xG_df2,
                      left_on=['Player', 'Team'],
                      right_on=['Player_first', 'Team'],
                      how='inner')

# Again, we concatenate the first_name df with the existing xG_FPL merged df
xG_FPL = pd.concat([xG_FPL, first_name]).drop(columns=['Player_first']).drop_duplicates()

# We're still missing 14 players to fully merge the xG_df and the current_df. Let's track them
miss_df = xG_df[['Player', 'Player_first']][(~xG_df['Player'].isin(xG_FPL['Player'])) &
                                             (~xG_df['Player_first'].isin(xG_FPL['Player']))]

# Creating manually a dictionary to replace the wrong player names with right ones
miss_dct = {'Mitrovic': 'Mitrović',
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
xG_missing = xG_df[xG_df['Player'].isin(miss_dct.keys())]
xG_missing['Player'] = xG_missing['Player'].map(miss_dct)

# Merging the xG_FPL df with the xG_missing df, and then concatenating
missing_name = pd.merge(current_df,
                        xG_missing,
                        on=['Player', 'Team'],
                        how='inner')

xG_FPL = pd.concat([xG_FPL, xG_missing]).drop(columns=['Player_first']).drop_duplicates()

# Replace duplicate family names manually
xG_df[(xG_df['Player'] == 'Luiz') & (xG_df['Player_first'] == 'David')] == 'David Luiz'
xG_df[(xG_df['Player'] == 'Luiz') & (xG_df['Player_first'] == 'Douglas')] == 'Douglas Luiz'
xG_df[(xG_df['Player'] == 'Longstaff') & (xG_df['Player_first'] == 'Sean')] == 'Sean Longstaff'
xG_df[(xG_df['Player'] == 'Longstaff') & (xG_df['Player_first'] == 'Matthew')] == 'Matty Longstaff'


# Concatenating the first and last name df's and dropping duplicate rows
xG_FPL = pd.concat([first_name, last_name])
xG_FPL[xG_FPL.duplicated()]
# .drop_duplicates()

xG_FPL[xG_FPL['Player'] == 'David Luiz']


current_df.iloc[64]

xG_df[xG_df['Player'] == 'Anderson']
# players_lst = list(lala_final['Player'])
#
# check = xG_df['Player_first'][~xG_df['Player'].isin(lala['Player'])]
# check2 = check[~check.isin(lala2['Player'])]
# len(check2)
# xG_df[~xG_df['Player'].isin(list(lala_final['Player']))]
#
# lala_final['Player'].isin(list(xG_df['Player']) + list(xG_df['Player_first']))
#
# lala_final[lala_final['Player'] == 'Kepa']
# xG_df.drop_duplicates()
#
# len(xG_df[['Player', 'Player_first']][xG_df['Player'].isin(check2) | xG_df['Player_first'].isin(check2)])
