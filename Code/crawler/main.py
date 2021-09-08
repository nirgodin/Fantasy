from time import sleep
from selenium import webdriver
from Code.crawler.consts.fpl_consts import FPL_STATISTICS_URL, CHROMEDRIVER_PATH, FPL_NON_REPEATED_CATEGORIES
from Code.crawler.consts.understat_consts import UNDERSTAT_PLAYER_NEXT_TABLE_XPATH_FORMAT, UNDERSTAT_EPL_URL
from Code.crawler.fantasy_crawler import FantasyCrawler
from Code.crawler.utils import FantasyCrawlerUtils

SEASON = '22'
CURRENT_GW = '4'
EXPORT = True

if __name__ == '__main__':

    # Set webdriver
    driver = webdriver.Chrome(CHROMEDRIVER_PATH)
    driver.get(FPL_STATISTICS_URL)
    sleep(5)

    # Set crawler and utils
    crawler = FantasyCrawler(chromedriver=driver)
    utils = FantasyCrawlerUtils()

    # Crawl FPL
    fpl_stats = crawler.get_fpl_stats(categories=FPL_NON_REPEATED_CATEGORIES)

    # Crawl Understat
    driver.get(UNDERSTAT_EPL_URL)
    sleep(5)
    understat_team_stats = crawler.get_understat_teams_stats()
    understat_player_stats = crawler.get_understat_player_stats()

    # Export
    if EXPORT:
        pass
        # fpl_stats.to_csv(utils.get_fpl_export_path(season=SEASON,
        #                                            gameweek=CURRENT_GW))
