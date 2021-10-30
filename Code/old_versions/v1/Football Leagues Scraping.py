import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
import re

# First, we set the season, current gameweek and previous gameweek variables
season = '21'
previous_GW = '10'
current_GW = '11'

# Defining the class and two functions that will allow us scraping the data and arranging it in a dataframe.
# Credit for these function to Scott Rome. They can be found here:
# https://srome.github.io/Parsing-HTML-Tables-in-Python-with-BeautifulSoup-and-pandas/
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

# League List
league_dct = {'La_liga': r'C:\Users\nirgo\Documents\GitHub\Football Stats\La Liga',
              'Bundesliga': r'C:\Users\nirgo\Documents\GitHub\Football Stats\Bundesliga',
              'Serie_A': r'C:\Users\nirgo\Documents\GitHub\Football Stats\Serie A',
              'Ligue_1': r'C:\Users\nirgo\Documents\GitHub\Football Stats\Ligue 1',
              'RFPL': r'C:\Users\nirgo\Documents\GitHub\Football Stats\RFPL'}

for league in league_dct.keys():

    # Setting driver
    driver = webdriver.Chrome(r'C:\Users\nirgo\PycharmProjects\Fantasy\Browsers\chromedriver.exe')
    url = 'https://understat.com/league/' + league

    # Entering the site
    driver.get(url)
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
        try:
            PLT[elem] = [re.split('[-+]', PLT[elem][i])[0] for i in range(0, len(PLT))]
        except TypeError:
            pass


    # # Creating a dictionary to the team names in the PLT to three letters abbreviation
    # team_dct = {'Arsenal': 'ARS',
    #             'Aston Villa': 'AVL',
    #             'Brighton': 'BHA',
    #             'Burnley': 'BUR',
    #             'Chelsea': 'CHE',
    #             'Crystal Palace': 'CRY',
    #             'Everton': 'EVE',
    #             'Fulham': 'FUL',
    #             'Leeds': 'LEE',
    #             'Leicester': 'LEI',
    #             'Liverpool': 'LIV',
    #             'Manchester City': 'MCI',
    #             'Manchester United': 'MUN',
    #             'Newcastle United': 'NEW',
    #             'Sheffield United': 'SHU',
    #             'Southampton': 'SOU',
    #             'Tottenham': 'TOT',
    #             'West Bromwich Albion': 'WBA',
    #             'West Ham': 'WHU',
    #             'Wolverhampton Wanderers': 'WOL'}
    #
    # # Converting team names in the PLT to three letter abbreviation
    # PLT['Team'] = [team_dct[team] for team in PLT['Team']]

    # Editing the PLT colnames
    PLT.rename(columns=lambda x: 'Team_' + x,
               inplace=True)
    PLT.rename(columns={'Team_Team': 'Team', 'Team_№': 'Team_Ranking'},
               inplace=True)

    # Export the final dataframe to a csv file
    teams_folder = league_dct[league] + '\\Teams\\' + 'S_' + season + '_GW1_' + current_GW + '.csv'
    PLT.to_csv(teams_folder, index=False)

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
    players_pages = list(range(2, 6)) + [5] * 60 + [6, 7]
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

    # Verifying that there aren't any na's in the data
    final_players = final_players.dropna().drop_duplicates()
    final_players = final_players[final_players['Player'] != '']

    # # Deleting second team for players who were playing for two teams this season
    # final_players['Team'] = [re.split(',', team)[0] for team in final_players['Team']]
    #
    # # Converting team names in the final_players to three letter abbreviation
    # final_players['Team'] = [team_dct[team] for team in final_players['Team']]

    # Cut out irrelevant info from some of the strings in the table
    for elem in ['Player_xG', 'Player_NPxG', 'Player_xA']:
        final_players[elem] = [re.split('[-+]', final_players[elem][i])[0] for i in final_players.index.tolist()]

    # Exporting the final_players df to csv file
    players_folder = league_dct[league] + '\\Players\\' + 'S_' + season + '_GW1_' + current_GW + '.csv'
    final_players.to_csv(players_folder, index=False)

    driver.quit()
