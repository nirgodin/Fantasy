import pandas as pd
from lxml import html
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
import time

driver = webdriver.Chrome(r'C:\Users\nirgo\PycharmProjects\Fantasy\Browsers\chromedriver.exe')
driver.get('https://fantasy.premierleague.com/statistics')


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


hp = HTMLTableParser()
df_lst = []
page = 0

while page <= 19:
    raw = hp.parse_html()
    temp = hp.arrange_html(raw)
    df_lst.append(temp)
    nxt = driver.find_element_by_xpath('//*[@id="root"]/div[2]/div/div/div[3]/button[3]')
    nxt.click()
    page += 1

data = pd.concat(df_lst)

