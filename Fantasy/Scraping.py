import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
import re

# First, we'll define a set of paramaters that will allow us
# to modify easily the code from one gameweek to another
season = '21'
previous_GW = '7'
current_GW = '8'

# Setting driver
driver = webdriver.Chrome(r'C:\Users\nirgo\PycharmProjects\Fantasy\Browsers\chromedriver.exe')


class HTMLTableParser:

    def parse_html(self):
        sourcecode = driver.page_source
        return BeautifulSoup(sourcecode, 'lxml')

    def arrange_html(self, table):
        n_columns = 0
        n_rows = 0
        column_names = []

        # Find number of rows and columns
        # we also find the column titles if we can
        for row in table.find_all('tr'):

            # Determine the number of rows in the table
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows += 1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_tags)

            # Handle column names if we find them
            th_tags = row.find_all('th')
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    column_names.append(th.get_text())

        # Safeguard on Column Titles
        if len(column_names) > 0 and len(column_names) != n_columns:
            raise Exception("Column titles do not match the number of columns")

        columns = column_names if len(column_names) > 0 else range(0, n_columns)
        df = pd.DataFrame(columns=columns,
                          index=range(0, n_rows))
        row_marker = 0
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                df.iat[row_marker, column_marker] = column.get_text()
                column_marker += 1
            if len(columns) > 0:
                row_marker += 1

        # Convert to float if possible
        for col in df:
            try:
                df[col] = df[col].astype(float)
            except ValueError:
                pass

        return df


# Shortcut for the HTMLTableParser class
hp = HTMLTableParser()

# Enter the Fantasy Premier League site
driver.get('https://fantasy.premierleague.com/statistics')
sleep(5)

# Setting the path to the next page button, to scroll between pages online
next_page = driver.find_element_by_xpath('//*[@id="root"]/div[2]/div/div/div[3]/button[3]')
# Setting the path to the menu button, to switch between summaries of different stats
menu = Select(driver.find_element_by_xpath('/html/body/main/div/div[2]/div/div/form/div/div[2]/div/div/select'))

# Creating a list containing the full list of the stats we're interested in
category_lst = ['Player', 'Cost', 'Sel.', 'Form', 'Pts.', 'Minutes played', 'Goals scored',
                'Assists', 'Clean sheets', 'Goals conceded', 'Own goals', 'Penalties saved',
                'Penalties missed', 'Yellow cards', 'Red cards', 'Saves', 'Bonus',
                'Bonus Points System', 'Influence', 'Creativity', 'Threat', 'ICT Index',
                'Form', 'Times in Dream Team', 'Value (form)', 'Value (season)',
                'Points per match', 'Transfers in', 'Transfers out', 'Price rise', 'Price fall']

# The first six elements in category_lst appears in all the pages, so we don't need to scrape them seperately.
# Therefore we'll create a different scraping list
scraping_lst = [elem for elem in category_lst if elem not in ['Player', 'Cost', 'Sel.', 'Form', 'Pts.']]

# Creating an empty list to which we'll append the scarped dataframes
df_lst = []
# Iterating through the values in scraping_lst to scrape all wanted data and append to df_lst
for elem in scraping_lst:
    category_df = []
    clk = 'menu.select_by_visible_text' + '(' + '"' + elem + '"' + ')'
    exec(clk)
    page = 0
    while page <= 19:
        raw = hp.parse_html()
        temp = hp.arrange_html(raw)
        category_df.append(temp)
        next_page.click()
        page += 1
    final = pd.concat(category_df)
    final.rename(columns={'**': elem}, inplace=True)
    df_lst.append(final)

# while(True):
#     try:
#         raw = hp.parse_html()
#         temp = hp.arrange_html(raw)
#         category_df.append(temp)
#         next_page.click()
#     except (ElementClickInterceptedException, WebDriverException)  as error:
#         break

# Merging the different DF's in df_lst to one dataframe
temp_df = df_lst[0]
for i in range(1, len(df_lst)):
    temp_df = pd.merge(temp_df, df_lst[i], on=['Player', 'Cost', 'Sel.', 'Form', 'Pts.'], how='inner')
final_df = temp_df[category_lst].copy()

# Spliting the Player column to three columns: Player, Team and Role
Player = [player[0:len(player) - 6] for player in final_df['Player']]
Team = [player[len(player) - 6:len(player) - 3] for player in final_df['Player']]
Role = [player[len(player) - 3:len(player)] for player in final_df['Player']]

# Inserting the three new columns to the dataframe
final_df['Player'] = Player
final_df.insert(2, 'Role', Role)
final_df.insert(1, 'Team', Team)

# Export the final dataframe to a csv file
final_df.to_csv(r'C:\Users\nirgo\Documents\GitHub\Fantasy\Fantasy\S21_GW1_' + current_GW + '.csv', index=False)

###############################################################################

# Entering the site
driver.get('https://understat.com/league/EPL/2020')
sleep(5)

# Expanding the table to include more data
# Opening the options menu
team_button = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[3]/div/div[2]/div/div[1]/button')
team_button.click()

# Iterate through the menu to click on all the unmarked labels
team_labels_dct = {'NPxG': '11',
                   'NPxGA': '13',
                   'NPxGD': '14',
                   'PPDA': '15',
                   'OPPDA': '16',
                   'DC': '17',
                   'ODC': '18'}

for label in team_labels_dct.values():
    label_button = driver.find_element_by_xpath(
        '/html/body/div[1]/div[3]/div[3]/div/div[2]/div/div[2]/div[2]/div/div[' + label + ']/div[2]/label')
    label_button.click()

# Applying the changes
team_apply = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[3]/div/div[2]/div/div[2]/div[3]/a[2]')
team_apply.click()

# Parsing the first page
raw_PLT = hp.parse_html()

# Arranging the Premier league table
PLT = hp.arrange_html(raw_PLT).iloc[0:20]

# Cut out irrelevant info from some of the strings in the table
for elem in ['xG', 'xGA', 'xPTS']:
    PLT[elem] = [re.split('[-+]', PLT[elem][i])[0] for i in range(0, len(PLT))]

# Creating a dictionary to the team names in the PLT to three letters abbreviation
team_dct = {'Arsenal': 'ARS',
            'Aston Villa': 'AVL',
            'Brighton': 'BHA',
            'Burnley': 'BUR',
            'Chelsea': 'CHE',
            'Crystal Palace': 'CRY',
            'Everton': 'EVE',
            'Fulham': 'FUL',
            'Leeds': 'LEE',
            'Leicester': 'LEI',
            'Liverpool': 'LIV',
            'Manchester City': 'MCI',
            'Manchester United': 'MUN',
            'Newcastle United': 'NEW',
            'Sheffield United': 'SHU',
            'Southampton': 'SOU',
            'Tottenham': 'TOT',
            'West Bromwich Albion': 'WBA',
            'West Ham': 'WHU',
            'Wolverhampton Wanderers': 'WOL'}

# Converting team names in the PLT to three letter abbreviation
PLT['Team'] = [team_dct[team] for team in PLT['Team']]

# Editing the PLT colnames
PLT.rename(columns=lambda x: 'Team_' + x,
           inplace=True)
PLT.rename(columns={'Team_Team': 'Team', 'Team_№': 'Team_Ranking'},
           inplace=True)

# Export the final dataframe to a csv file
PLT.to_csv(r'C:\Users\nirgo\Documents\GitHub\Fantasy\Fantasy\League Table\S21_GW1_' + current_GW + '.csv', index=False)

###############################################################################

# Expanding the table to include more data
# Opening the options menu
player_button = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[4]/div/div[2]/div[1]/button')
player_button.click()

# Iterate through the menu to click on all the unmarked labels
player_labels_dct = {'N': '1',
                     'NPG': '7',
                     'NPxG': '10',
                     'xGChain': '12',
                     'xGBuildup': '13',
                     'NPxG90': '15',
                     'xG90 + xA90': '17',
                     'NPxG90 + xA90': '18',
                     'xGChain90': '19',
                     'xGBuildup90': '20'}

for label in player_labels_dct.values():
    label_button = driver.find_element_by_xpath(
        '/html/body/div[1]/div[3]/div[4]/div/div[2]/div[2]/div[2]/div/div[' + label + ']/div[2]/label')
    label_button.click()

# Applying the changes
player_apply = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[4]/div/div[2]/div[2]/div[3]/a[2]')
player_apply.click()

# Scraping

players_df = []
players_pages = list(range(2, 6)) + [5] * 35 + [6, 7]
players_pages = [str(i) for i in players_pages]

for i in players_pages:
    raw_players = hp.parse_html()
    temp_players = hp.arrange_html(raw_players)
    temp_players = temp_players.iloc[20:len(temp_players) - 1]
    players_df.append(temp_players)
    next_table_str = '/html/body/div[1]/div[3]/div[4]/div/div[2]/div[1]/ul/li[' + i + ']/a'
    next_table = driver.find_element_by_xpath(next_table_str)
    next_table.click()

final_players = pd.concat(players_df)

# Resetting the dataframe index
final_players = final_players.reset_index(drop=True)

# Creating a list of the categories of the final_players df
US_category_lst = ['Player',
                   'Team',
                   'Appearances',
                   'Minutes played',
                   'Goals scored',
                   'NPG',
                   'Assists',
                   'xG',
                   'NPxG',
                   'xA',
                   'xGChain',
                   'xGBuildup',
                   'xG90',
                   'NPxG90',
                   'xA90',
                   'xG90+xA90',
                   'NPxG90+xA90',
                   'xGChain90',
                   'xGBuildup90']

# Renaming the columns of the dataframe
# Adding to the column names into 'Player', to distinguish them from the team stats in the final df
for i in range(0, len(US_category_lst)):
    final_players.rename(columns={final_players.columns[i]: 'Player_' + US_category_lst[i]},
                         inplace=True)
final_players.rename(columns={'Player_Team': 'Team', 'Player_Player': 'Player'},
                     inplace=True)

# Deleting second team for players who were playing for two teams this season
final_players['Team'] = [re.split(',', team)[0] for team in final_players['Team']]

# Converting team names in the final_players to three letter abbreviation
final_players['Team'] = [team_dct[team] for team in final_players['Team']]

# Cut out irrelevant info from some of the strings in the table
for elem in ['Player_xG', 'Player_NPxG', 'Player_xA']:
    final_players[elem] = [re.split('[-+]', final_players[elem][i])[0] for i in range(0, len(final_players))]

# Breaking down the full name of the players to first (2nd column) and last names (1st column) 
final_players.insert(1, 'Player_first', 'nan')
for i in range(0, len(final_players)):
    final_players['Player_first'][i] = re.split('[ ]', final_players['Player'][i])[0]
    try:
        final_players['Player'][i] = re.split('[ ]', final_players['Player'][i])[1] + ' ' +\
                                     re.split('[ ]', final_players['Player'][i])[2]
    except IndexError:
        pass
        try:
            final_players['Player'][i] = re.split('[ ]', final_players['Player'][i])[1]
        except IndexError:
            pass

# Exporting the final_players df to csv file
final_players.to_csv(r'C:\Users\nirgo\Documents\GitHub\Fantasy\Fantasy\Understat\S21_GW1_' +
                     current_GW + '.csv', index=False)

