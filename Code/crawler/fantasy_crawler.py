from time import sleep
from typing import List, Tuple
import pandas as pd
from pandas import DataFrame
from selenium.webdriver.chrome.webdriver import WebDriver
from Code.crawler.consts.fpl_consts import FPL_DROPDOWN_MENU_XPATH, TWO_ASTERISKS
from Code.crawler.pre_processing import CrawlerPreProcessing
from Code.crawler.utils import FantasyCrawlerUtils
from Code.crawler.webcontroller.web_controller import WebController


class FantasyCrawler(WebController):

    def __init__(self, chromedriver: WebDriver):
        super(FantasyCrawler, self).__init__(chromedriver)
        self._preprocessor = CrawlerPreProcessing()

    def get_understat_player_stats(self,
                                   pages_numbers: List[int],
                                   next_table_xpath_format: Tuple[str, str]) -> DataFrame:
        players_stats = []

        for page_number in pages_numbers:
            current_table_stats = self._parse_single_understat_player_page()
            players_stats.append(current_table_stats)

            page_xpath = self._get_element_xpath(element_xpath_format=next_table_xpath_format,
                                                 element_xpath_number=page_number)
            self._click_web_element(web_element_xpath=page_xpath)

            all_stats = pd.concat(players_stats).drop_duplicates().reset_index(drop=True)

            return all_stats

    def get_understat_teams_stats(self) -> DataFrame:
        arranged_html = self._parse_single_page()
        teams_stats = arranged_html[0:20]

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
