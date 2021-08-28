from time import sleep
from selenium import webdriver
from Code.crawler.consts.fpl_consts import FPL_STATISTICS_URL, FPL_CATEGORIES
from Code.crawler.consts.understat_consts import UNDERSTAT_PAGES, UNDERSTAT_PLAYER_NEXT_TABLE_XPATH_FORMAT
from Code.crawler.fantasy_crawler import FantasyCrawler

SEASON = '22'
CURRENT_GW = '3'
EXPORT = True
# total_pages = driver.find_element_by_xpath('/html/body/main/div/div[2]/div/div[1]/div[3]/div')
# while page <= int(total_pages.text[-2:]):

if __name__ == '__main__':

    # Set webdriver
    driver = webdriver.Chrome(r'Browsers\chromedriver.exe')
    driver.get(FPL_STATISTICS_URL)
    sleep(5)

    # Set crawler
    crawler = FantasyCrawler(chromedriver=driver)

    # Crawl
    fpl_stats = crawler.get_fpl_stats(categories=FPL_CATEGORIES)
    understat_team_stats = crawler.get_understat_teams_stats()
    understat_player_stats = crawler.get_understat_player_stats(
        pages_numbers=UNDERSTAT_PAGES,
        next_table_xpath_format=UNDERSTAT_PLAYER_NEXT_TABLE_XPATH_FORMAT)

    # Export
    if EXPORT:
        pass
