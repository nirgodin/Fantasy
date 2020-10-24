import pandas as pd
import numpy as np

# Import the Gameweek stats dataframe
Gameweek = pd.read_csv(r'C:\Users\nirgo\Documents\GitHub\Fantasy\Fantasy\S21_GW1_5.csv')

# Import the Gameweek league table dataframe
PLT = pd.read_csv(r'C:\Users\nirgo\Documents\GitHub\Fantasy\Fantasy\S21_PLT1_5.csv')

# Import the schedule of all the teams
Schedule = pd.read_csv(r'C:\Users\nirgo\Documents\GitHub\Fantasy\Fantasy\Schedule.csv', index_col=0)
Schedule.loc['ARS', :]

# Inserting an empty opponent column in the Gameweek df
Gameweek.insert(2, 'Opponent', 'nan')
# Inserting the relevant opponents from the Schedule df
Gameweek['Opponent'] = [Schedule.loc[team, '5'] for team in Gameweek['Team']]

