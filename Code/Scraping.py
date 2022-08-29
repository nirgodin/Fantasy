import pandas as pd
import numpy as np
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
import re
from Code.Functions import HTMLTableParser
hp = HTMLTableParser()

# First, we set the season, current gameweek and previous gameweek variables
season = '23'
current_GW = '4'

# Setting driver
driver = webdriver.Chrome(r'Browsers\chromedriver.exe')

# Enter the Fantasy Premier League site
driver.get('https://fantasy.premierleague.com/statistics')
sleep(20)
try:
    accept_cookies = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div[5]/button[1]')
    accept_cookies.click()
except:
    pass

# Setting the path to the next page button, to scroll between pages online
next_page = driver.find_element_by_xpath('//*[@id="root"]/div[2]/div/div/div[3]/button[3]')
# Setting the path to the menu button, to switch between summaries of different stats
menu = Select(driver.find_element_by_xpath('/html/body/main/div/div[2]/div/div/form/div/div[2]/div/div/select'))

# Creating a list containing the full list of the stats we're interested in
category_lst = ['Player',
                'Cost',
                'Sel.',
                'Form',
                'Pts.',
                'Minutes played',
                'Goals scored',
                'Assists',
                'Clean sheets',
                'Goals conceded',
                'Own goals',
                'Penalties saved',
                'Penalties missed',
                'Yellow cards',
                'Red cards',
                'Saves',
                'Bonus',
                'Bonus Points System',
                'Influence',
                'Creativity',
                'Threat',
                'ICT Index',
                'Form',
                'Times in Dream Team',
                'Value (form)',
                'Value (season)',
                'Points per match',
                'Transfers in',
                'Transfers out',
                'Price rise',
                'Price fall']

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
    page = 1
    total_pages = driver.find_element_by_xpath('/html/body/main/div/div[2]/div/div[1]/div[3]/div')
    while page <= int(total_pages.text[-2:]):
        try:
            raw = hp.parse_html(driver=driver)
            temp = hp.arrange_html(raw)
            category_df.append(temp)
            next_page.click()
            page += 1
        except ElementClickInterceptedException as error:
            break

    # while (True):
    #     try:
    #         raw = hp.parse_html(driver=driver)
    #         temp = hp.arrange_html(raw)
    #         category_df.append(temp)
    #         next_page.click()
    #     except ElementClickInterceptedException as error:
    #         break
    final = pd.concat(category_df)
    final.rename(columns={'**': elem}, inplace=True)
    df_lst.append(final)


# Merging the different DF's in df_lst to one dataframe
temp_df = df_lst[0]

for i in range(1, len(df_lst)):
    temp_df = pd.merge(temp_df, df_lst[i],
                       on=['Player', 'Cost', 'Sel.', 'Form', 'Pts.'],
                       how='outer')

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
final_df.to_csv(r'Data\FPL\FPL_S' + season + '_GW1_' + current_GW + '.csv', index=False)

###############################################################################

# Entering the site
driver.get('https://understat.com/league/EPL/2022')
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
raw_PLT = hp.parse_html(driver=driver)

# Arranging the Premier league table
PLT = hp.arrange_html(raw_PLT).iloc[0:20]

# Cut out irrelevant info from some of the strings in the table
for elem in ['xG', 'xGA', 'xPTS']:
    PLT[elem] = [re.split('[-+]', PLT[elem][i])[0] for i in range(0, len(PLT))]

# Creating a dictionary to the team names in the PLT to three letters abbreviation
team_dct = {'Arsenal': 'ARS',
            'Aston Villa': 'AVL',
            'Bournemouth': 'BOU',
            'Brentford': 'BRE',
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
            'Norwich': 'NOR',
            'Nottingham Forest': 'NFO',
            'Sheffield United': 'SHU',
            'Southampton': 'SOU',
            'Tottenham': 'TOT',
            'Watford': 'WAT',
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
PLT.to_csv(r'Data\PLT\PLT_S' + season + '_GW1_' + current_GW + '.csv', index=False)

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
players_pages = list(range(2, 6)) + [5] * 50 + [6, 7]
players_pages = [str(i) for i in players_pages]

for i in players_pages:
    raw_players = hp.parse_html(driver=driver)
    temp_players = hp.arrange_html(raw_players)
    temp_players = temp_players.iloc[20:len(temp_players) - 1]
    players_df.append(temp_players)
    next_table_str = '/html/body/div[1]/div[3]/div[4]/div/div[2]/div[1]/ul/li[' + i + ']/a'
    next_table = driver.find_element_by_xpath(next_table_str)
    next_table.click()

final_players = pd.concat(players_df)

# Resetting the dataframe index
final_players = final_players.drop_duplicates().reset_index(drop=True)

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
final_players = final_players.dropna()
final_players = final_players[final_players['Player'] != '']

# Deleting second team for players who were playing for two teams this season
final_players['Team'] = [re.split(',', team)[0] for team in final_players['Team']]

# Converting team names in the final_players to three letter abbreviation
final_players['Team'] = [team_dct[team] for team in final_players['Team']]

# Cut out irrelevant info from some of the strings in the table
for elem in ['Player_xG', 'Player_NPxG', 'Player_xA']:
    final_players[elem] = [re.split('[-+]', final_players[elem][i])[0] for i in final_players.index.tolist()]

# Exporting the final_players df to csv file
final_players.to_csv(r'Data\Understat\xG_S' + season + '_GW1_' + current_GW + '.csv', index=False)

