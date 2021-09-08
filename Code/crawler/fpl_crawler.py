from time import sleep
from typing import List
import pandas as pd
from pandas import DataFrame
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.webdriver import WebDriver
from Code.crawler.consts.fpl_consts import FPL_DROPDOWN_MENU_XPATH, FPL_TOTAL_NUMBER_PAGES_XPATH, FPL_NEXT_PAGE_XPATH
from Code.crawler.pre_processor import CrawlerPreProcessor
from Code.crawler.webcontroller.web_controller import WebController


class FPLCrawler(WebController):

    def __init__(self, chromedriver: WebDriver):
        super(FPLCrawler, self).__init__(chromedriver)
        self._preprocessor = CrawlerPreProcessor()

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

    def _parse_multiple_fpl_pages(self) -> DataFrame:
        players_stats = []
        page = 1
        while page <= self._get_total_number_of_fpl_stat_pages():
            page_stats = self._parse_single_page()
            players_stats.append(page_stats)
            try:
                self._click_web_element(FPL_NEXT_PAGE_XPATH)
            except ElementClickInterceptedException:
                break
            page += 1

        category_stats = pd.concat(players_stats).drop_duplicates().reset_index(drop=True)

        return category_stats

    def _get_total_number_of_fpl_stat_pages(self) -> int:
        total_pages_element = self._driver.find_element_by_xpath(FPL_TOTAL_NUMBER_PAGES_XPATH)
        total_pages_number = total_pages_element.text[-2:]

        return int(total_pages_number)
