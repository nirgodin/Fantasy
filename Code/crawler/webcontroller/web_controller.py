from typing import List

import pandas as pd
from pandas import DataFrame
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.select import Select
from Code.crawler.consts.fpl_consts import FPL_NEXT_PAGE_XPATH, FPL_TOTAL_NUMBER_PAGES_XPATH
from Code.crawler.consts.understat_consts import UNDERSTAT_TOTAL_NUMBER_PAGES_XPATH
from Code.crawler.table_parser.html_table_parser import HTMLTableParser


class WebController(HTMLTableParser):

    def __init__(self, chromedriver: WebDriver):
        super(WebController).__init__()
        self._driver = chromedriver

    def _parse_single_understat_player_page(self) -> DataFrame:
        arranged_html = self._parse_single_page()
        players_stats = arranged_html.iloc[20: len(arranged_html) - 1]

        return players_stats

    def _display_all_understat_categories(self,
                                          dropdown_menu_xpath: str,
                                          understat_categories_xapth_format: tuple,
                                          categories: dict,
                                          apply_changes_button_xpath: str) -> None:

        self._click_web_element(dropdown_menu_xpath)

        for category_number in categories.values():
            category_xapth = self._get_element_xpath(understat_categories_xapth_format, category_number)
            self._click_web_element(category_xapth)

        self._click_web_element(apply_changes_button_xpath)

        return None

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

    def _parse_single_page(self) -> DataFrame:
        parsed_html = self._parse_html(self._driver)
        arranged_html = self._arrange_html(parsed_html)

        return arranged_html

    def _click_web_element(self, web_element_xpath: str) -> None:
        web_element = self._driver.find_element_by_xpath(web_element_xpath)
        web_element.click()

        return None

    def _click_select_element(self, select_element_xpath: str, visible_text: str) -> None:
        select_element = Select(self._driver.find_element_by_xpath(select_element_xpath))
        select_element.select_by_visible_text(visible_text)

        return None

    @staticmethod
    def _get_element_xpath(element_xpath_format: tuple, element_xpath_number: int) -> str:
        element_xpath_start = element_xpath_format[0]
        element_xpath_number = str(element_xpath_number)
        element_xpath_finish = element_xpath_format[1]

        full_element_xpath = element_xpath_start + element_xpath_number + element_xpath_finish

        return full_element_xpath

    def _get_total_number_of_fpl_stat_pages(self) -> int:
        total_pages_element = self._driver.find_element_by_xpath(FPL_TOTAL_NUMBER_PAGES_XPATH)
        total_pages_number = total_pages_element.text[-2:]

        return int(total_pages_number)

    def _get_understat_pages_xpath_numbers(self) -> List[int]:
        total_number_of_pages = self._get_total_number_of_understat_stat_pages()

        return list(range(1, 6)) + [5]*(total_number_of_pages - 7) + [6, 7]

    def _get_total_number_of_understat_stat_pages(self) -> int:
        total_pages_element = self._driver.find_element_by_xpath(UNDERSTAT_TOTAL_NUMBER_PAGES_XPATH)
        total_pages_number = total_pages_element.text

        return int(total_pages_number)
