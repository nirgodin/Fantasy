from time import sleep
from typing import List, Tuple
import pandas as pd
from pandas import DataFrame
from selenium.webdriver.chrome.webdriver import WebDriver
from Code.crawler.consts.fpl_consts import FPL_DROPDOWN_MENU_XPATH, TWO_ASTERISKS
from Code.crawler.consts.understat_consts import UNDERSTAT_TEAM_DROPDOWN_MENU_XPATH, \
    UNDERSTAT_TEAM_CATEGORIES_XPATH_FORMAT, UNDERSTAT_TEAM_CATEGORIES, UNDERSTAT_TEAM_APPLY_CHANGES_BUTTON, \
    UNDERSTAT_PLAYER_DROPDOWN_MENU_XPATH, UNDERSTAT_PLAYER_CATEGORIES_XPATH_FORMAT, UNDERSTAT_PLAYER_CATEGORIES, \
    UNDERSTAT_PLAYER_APPLY_CHANGES_BUTTON, UNDERSTAT_PLAYER_NEXT_TABLE_XPATH_FORMAT
from Code.crawler.pre_processing import CrawlerPreProcessing
from Code.crawler.utils import FantasyCrawlerUtils
from Code.crawler.webcontroller.web_controller import WebController


class FantasyCrawler(WebController):

    def __init__(self, chromedriver: WebDriver):
        super(FantasyCrawler, self).__init__(chromedriver)
        self._preprocessor = CrawlerPreProcessing()

    def get_understat_player_stats(self) -> DataFrame:

        self._display_all_understat_categories(
            dropdown_menu_xpath=UNDERSTAT_PLAYER_DROPDOWN_MENU_XPATH,
            understat_categories_xapth_format=UNDERSTAT_PLAYER_CATEGORIES_XPATH_FORMAT,
            categories=UNDERSTAT_PLAYER_CATEGORIES,
            apply_changes_button_xpath=UNDERSTAT_PLAYER_APPLY_CHANGES_BUTTON
        )

        players_stats = []

        for page_number in self._get_understat_pages_xpath_numbers():
            page_xpath = self._get_element_xpath(element_xpath_format=UNDERSTAT_PLAYER_NEXT_TABLE_XPATH_FORMAT,
                                                 element_xpath_number=page_number)
            self._click_web_element(web_element_xpath=page_xpath)
            current_table_stats = self._parse_single_understat_player_page()
            players_stats.append(current_table_stats)

        return pd.concat(players_stats).dropna().reset_index(drop=True)

    def get_understat_teams_stats(self) -> DataFrame:
        self._display_all_understat_categories(dropdown_menu_xpath=UNDERSTAT_TEAM_DROPDOWN_MENU_XPATH,
                                               understat_categories_xapth_format=UNDERSTAT_TEAM_CATEGORIES_XPATH_FORMAT,
                                               categories=UNDERSTAT_TEAM_CATEGORIES,
                                               apply_changes_button_xpath=UNDERSTAT_TEAM_APPLY_CHANGES_BUTTON)
        arranged_html = self._parse_single_page()
        teams_stats = arranged_html.iloc[:20]

        return teams_stats

    def get_fpl_stats(self, categories: List[str]) -> DataFrame:
        categories_stats = self._get_fpl_categories_stats(categories=categories)
        fpl_stats = self._preprocessor.merge_categories(categories_stats=categories_stats)

        return self._preprocessor.subset_categories_columns(data=fpl_stats)

    def _get_fpl_categories_stats(self, categories: List[str]) -> List[DataFrame]:
        categories_stats = []

        for category in categories:
            self._click_select_element(FPL_DROPDOWN_MENU_XPATH, category)
            sleep(1)
            category_stats = self._parse_multiple_fpl_pages()
            category_stats = self._preprocessor.rename_asterisks_column_with_category(category_stats=category_stats,
                                                                                      category_name=category)
            categories_stats.append(category_stats)

        return categories_stats
