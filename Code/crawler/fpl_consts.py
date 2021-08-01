CHROMEDRIVER_PATH = r'Browsers\chromedriver.exe'
FPL_STATISTICS_URL = 'https://fantasy.premierleague.com/statistics'

FPL_NEXT_PAGE_XPATH = '//*[@id="root"]/div[2]/div/div/div[3]/button[3]'
FPL_DROPDOWN_MENU_XPATH = '/html/body/main/div/div[2]/div/div/form/div/div[2]/div/div/select'

# Categories that doesn't appear in all stats pages. They appear only if selected in the dropdown menu
FPL_NON_REPEATED_CATEGORIES = ['Minutes played',
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

# Categories that appear in all stats pages, alongside the selected category in the dropdown menu
FPL_REPEATED_CATEGORIES = ['Player',
                           'Cost',
                           'Sel.',
                           'Form',
                           'Pts.']

FPL_CATEGORIES = FPL_NON_REPEATED_CATEGORIES + FPL_REPEATED_CATEGORIES


# FPL column names
PLAYER = 'Player'
COST = 'Cost'
SELECTED = 'Sel.'
FORM = 'Form'
POINTS = 'Pts.'
TEAM = 'Team'
ROLE = 'Role'
