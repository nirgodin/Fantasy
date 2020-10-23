import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementClickInterceptedException

# Setting driver and enter the Fantasy Premier League site
driver = webdriver.Chrome(r'C:\Users\nirgo\PycharmProjects\Fantasy\Browsers\chromedriver.exe')
driver.get('https://fantasy.premierleague.com/statistics')
sleep(5)

# Setting the path to the next page button, to scroll between pages online
next_page = driver.find_element_by_xpath('//*[@id="root"]/div[2]/div/div/div[3]/button[3]')
# Setting the path to the menu button, to switch between summaries of different stats
menu = Select(driver.find_element_by_xpath('/html/body/main/div/div[2]/div/div/form/div/div[2]/div/div/select'))


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
    page = 0
    category_df = []
    clk = 'menu.select_by_visible_text' + '(' + '"' + elem + '"' + ')'
    exec(clk)
    while(True):
        try:
            raw = hp.parse_html()
            temp = hp.arrange_html(raw)
            category_df.append(temp)
            page += 1
            next_page.click()
        except ElementClickInterceptedException:
            break
    final = pd.concat(category_df)
    final.rename(columns={'**': elem}, inplace=True)
    df_lst.append(final)

# Merging the different DF's in df_lst to one dataframe
temp_df = df_lst[0]
for i in range(1, len(df_lst)):
    temp_df = pd.merge(temp_df, df_lst[i], on=['Player', 'Cost', 'Sel.', 'Form', 'Pts.'], how='inner')
final_df = temp_df[category_lst].copy()

# Spliting the Player column to three columns: Player, Team and Role
Player = [player[0:len(player)-6] for player in final_df['Player']]
Team = [player[len(player)-6:len(player)-3] for player in final_df['Player']]
Role = [player[len(player)-3:len(player)] for player in final_df['Player']]

# Inserting the three new columns to the dataframe
final_df['Player'] = Player
final_df.insert(1, 'Team', Team)
final_df.insert(2, 'Role', Role)

# Export the final dataframe to a csv file
final_df.to_csv(r'C:\Users\nirgo\Documents\GitHub\Fantasy\Fantasy\S21_GW1_8.csv', index=False)

