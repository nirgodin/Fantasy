UNDERSTAT_URL = 'https://understat.com/league/'

UNDERSTAT_LEAGUES = {'England': 'EPL',
                     'Spain': 'La_liga',
                     'Germany': 'Bundesliga',
                     'Italy': 'Serie_A',
                     'France': 'Ligue_1',
                     'Russia': 'RFPL'}

UNDERSTAT_TEAM_DROPDOWN_MENU_XPATH = '/html/body/div[1]/div[3]/div[3]/div/div[2]/div/div[1]/button'
UNDERSTAT_TEAM_CATEGORIES = {'NPxG': '11',
                             'NPxGA': '13',
                             'NPxGD': '14',
                             'PPDA': '15',
                             'OPPDA': '16',
                             'DC': '17',
                             'ODC': '18'}

UNDERSTAT_TEAM_CATEGORIES_XPATH_FORMAT = ('/html/body/div[1]/div[3]/div[3]/div/div[2]/div/div[2]/div[2]/div/div[',
                                          ']/div[2]/label')
UNDERSTAT_TEAM_APPLY_CHANGES_BUTTON = '/html/body/div[1]/div[3]/div[3]/div/div[2]/div/div[2]/div[3]/a[2]'


TEAMS_ABBREVIATIONS = {'Arsenal': 'ARS',
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



UNDERSTAT_PLAYER_CATEGORIES = {'N': '1',
                               'NPG': '7',
                               'NPxG': '10',
                               'xGChain': '12',
                               'xGBuildup': '13',
                               'NPxG90': '15',
                               'xG90 + xA90': '17',
                               'NPxG90 + xA90': '18',
                               'xGChain90': '19',
                               'xGBuildup90': '20'}


UNDERSTAT_PLAYER_DROPDOWN_MENU_XPATH = '/html/body/div[1]/div[3]/div[4]/div/div[2]/div[1]/button'
UNDERSTAT_PLAYER_CATEGORIES_XPATH_FORMAT = ('/html/body/div[1]/div[3]/div[4]/div/div[2]/div[2]/div[2]/div/div[',
                                            ']/div[2]/label')

UNDERSTAT_PLAYER_APPLY_CHANGES_BUTTON = '/html/body/div[1]/div[3]/div[4]/div/div[2]/div[2]/div[3]/a[2]'

UNDERSTAT_PLAYER_NEXT_TABLE_XPATH_FORMAT = ('/html/body/div[1]/div[3]/div[4]/div/div[2]/div[1]/ul/li[',
                                            ']/a')


UNDERSTAT_CATEGORIES = ['Player',
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
