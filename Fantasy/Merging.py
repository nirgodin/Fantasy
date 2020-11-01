import pandas as pd
import numpy as np

# Import the previous and this week cumulative dataframes
previous_GW = pd.read_csv(r'C:\Users\nirgo\Documents\GitHub\Fantasy\Fantasy\S21_GW1_5.csv')
current_GW = pd.read_csv(r'C:\Users\nirgo\Documents\GitHub\Fantasy\Fantasy\S21_GW1_6.csv')

# Creating this week gameweek not cumulative dataframe by subtracting the cumulative dataframes
# Creating a list of all the variables that should be subtracted from each other
subtraction_lst = ['Pts.', 'Minutes played', 'Goals scored', 'Assists', 'Clean sheets',
                   'Goals conceded', 'Own goals', 'Penalties saved', 'Penalties missed',
                   'Yellow cards', 'Red cards', 'Saves', 'Bonus', 'Bonus Points System',
                   'Times in Dream Team', 'Transfers in', 'Transfers out']

# Merging the previous and current gameweeks dataframes
temp_GW = pd.merge(current_GW, previous_GW, on=['Player', 'Team', 'Role'], how='inner')

# Creating an empty dataframe to which the not cumulative values will be passed
GW = pd.DataFrame(columns=list(current_GW.columns))

# Iterating through the columns and passing them to the final dataframe
for col in list(GW.columns):
    if col in subtraction_lst:
        GW[col] = temp_GW[col + '_x'] - temp_GW[col + '_y']
    elif col in ['Player', 'Team', 'Role']:
        GW[col] = temp_GW[col]
    else:
        GW[col] = temp_GW[col + '_x']

###########################################################################################

# Import the schedule of all the teams
Schedule = pd.read_csv(r'C:\Users\nirgo\Documents\GitHub\Fantasy\Fantasy\Schedule.csv', index_col=0)

# Inserting an empty opponent column in the Gameweek df
GW.insert(2, 'Opponent', 'nan')
# Inserting the relevant opponents from the Schedule df
GW['Opponent'] = [Schedule.loc[team, '6'] for team in GW['Team']]

