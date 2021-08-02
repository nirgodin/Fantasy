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
