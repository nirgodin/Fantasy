from typing import List

import pandas as pd
from pandas import DataFrame
from selenium.webdriver.chrome.webdriver import WebDriver
from Code.crawler.consts.understat_consts import UNDERSTAT_PLAYER_NEXT_TABLE_XPATH_FORMAT, \
    UNDERSTAT_PLAYER_DROPDOWN_MENU_XPATH, UNDERSTAT_PLAYER_CATEGORIES_XPATH_FORMAT, UNDERSTAT_PLAYER_CATEGORIES, \
    UNDERSTAT_PLAYER_APPLY_CHANGES_BUTTON, UNDERSTAT_TEAM_DROPDOWN_MENU_XPATH, UNDERSTAT_TEAM_CATEGORIES_XPATH_FORMAT, \
    UNDERSTAT_TEAM_CATEGORIES, UNDERSTAT_TEAM_APPLY_CHANGES_BUTTON, UNDERSTAT_TOTAL_NUMBER_PAGES_XPATH
from Code.crawler.pre_processor import CrawlerPreProcessor
from Code.crawler.webcontroller.web_controller import WebController


class UnderstatCrawler(WebController):

    def __init__(self, chromedriver: WebDriver):
        super(UnderstatCrawler, self).__init__(chromedriver)
        self._preprocessor = CrawlerPreProcessor()

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

    def _get_understat_pages_xpath_numbers(self) -> List[int]:
        total_number_of_pages = self._get_total_number_of_understat_stat_pages()

        return list(range(1, 6)) + [5]*(total_number_of_pages - 7) + [6, 7]

    def _get_total_number_of_understat_stat_pages(self) -> int:
        total_pages_element = self._driver.find_element_by_xpath(UNDERSTAT_TOTAL_NUMBER_PAGES_XPATH)
        total_pages_number = total_pages_element.text

        return int(total_pages_number)

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
