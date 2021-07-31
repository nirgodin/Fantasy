from typing import List
from pandas import DataFrame
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.remote.webelement import WebElement

from Code.crawler.consts import FPL_NEXT_PAGE_XPATH
from Code.crawler.table_parser.html_table_parser import HTMLTableParser


class WebController(HTMLTableParser):

    def __init__(self, chromedriver: WebDriver):
        super(WebController).__init__()
        self._driver = chromedriver
        self._next_page_button = self._get_next_page_button(FPL_NEXT_PAGE_XPATH)

    def _parse_multiple_pages(self) -> List[DataFrame]:
        dataframes = []

        while True:
            try:
                page_stats = self._parse_single_page()
                dataframes.append(page_stats)
                self._click_next_page_button(self._next_page_button)
            except ElementClickInterceptedException as error:
                break

        return dataframes

    def _parse_single_page(self):
        parsed_html = self._parse_html(self._driver)
        arranged_html = self._arrange_html(parsed_html)

        return arranged_html

    @staticmethod
    def _click_next_page_button(next_page_button: WebElement) -> None:
        next_page_button.click()

        return None

    @staticmethod
    def _click_dropdown_menu(dropdown_menu_button: Select, category_name: str) -> None:
        dropdown_menu_button.select_by_visible_text(category_name)

        return None

    def _get_dropdown_menu_button(self, dropdown_menu_xpath: str) -> Select:
        dropdown_menu_button = self._driver.find_element_by_xpath(dropdown_menu_xpath)

        return dropdown_menu_button

    def _get_next_page_button(self, next_page_xpath: str):
        next_page_button = self._driver.find_element_by_xpath(next_page_xpath)

        return next_page_button
