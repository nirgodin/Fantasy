from time import sleep
from selenium import webdriver
from Code.consts.fpl_consts import FPL_STATISTICS_URL, CHROMEDRIVER_PATH, FPL_NON_REPEATED_CATEGORIES
from Code.consts.understat_consts import UNDERSTAT_EPL_URL
from Code.crawler.fpl_crawler import FPLCrawler
from Code.crawler.understat_crawler import UnderstatCrawler
from Code.crawler.utils import FantasyCrawlerUtils

SEASON = '22'
CURRENT_GW = '19'
EXPORT = True

if __name__ == '__main__':

    # Set webdriver
    driver = webdriver.Chrome(CHROMEDRIVER_PATH)

    # Set crawlers and utils
    fpl_crawler = FPLCrawler(chromedriver=driver)
    understat_crawler = UnderstatCrawler(chromedriver=driver)
    utils = FantasyCrawlerUtils()

    # Crawl FPL
    driver.get(FPL_STATISTICS_URL)
    sleep(5)
    fpl_stats = fpl_crawler.get_fpl_stats(categories=FPL_NON_REPEATED_CATEGORIES)

    # Crawl Understat
    driver.get(UNDERSTAT_EPL_URL)
    sleep(5)
    understat_team_stats = understat_crawler.get_understat_teams_stats()
    understat_player_stats = understat_crawler.get_understat_player_stats()

    # Export
    if EXPORT:
        fpl_stats.to_csv(utils.get_fpl_export_path(season=SEASON, gameweek=CURRENT_GW),
                         index=False)

        understat_team_stats.to_csv(utils.get_understat_teams_export_path(season=SEASON, gameweek=CURRENT_GW),
                                    index=False)

        understat_player_stats.to_csv(utils.get_understat_players_export_path(season=SEASON, gameweek=CURRENT_GW),
                                      index=False)
