import pandas as pd
import numpy as np

# LINEAR MODEL
gw_df_lst = []
for i in range(5, 10):
    previous = str(i)
    current = str(i+1)
    previous_df = pd.read_csv(r'Cumulative Merged Data\CMD_S21_GW_' + previous + '.csv').rename(columns={'Pts.': 'Cum_Pts.'})
    current_df = pd.read_csv(r'Single GW\SGW_S21_GW_' + current + '.csv')
    current_df = current_df[['Player', 'Team', 'Pts.']]
    GW = pd.merge(previous_df,
                  current_df,
                  on=['Player', 'Team'],
                  how='inner')
    GW.insert(0, 'Gameweek', current)
    gw_df_lst.append(GW)

lm_data = pd.concat(gw_df_lst).reset_index(drop=True)
lm_data['Sel.'] = [float(str(lm_data['Sel.'][i]).replace('%', '')) for i in lm_data.index.tolist()]

lm_data.to_csv(r'Models Data\lm_data.csv', index=False)

# # Pivoting the data to suit timeseries mode
# piv_GW = pd.pivot_table(GW,
#                         index='Gameweek',
#                         columns='Player',
#                         values=GW.drop(columns=['Player', 'Season', 'Gameweek', 'Opponent', 'Team', 'Role']).columns)
