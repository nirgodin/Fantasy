from time import sleep
from typing import List
from pandas import DataFrame
from selenium.webdriver.chrome.webdriver import WebDriver
from Code.crawler.fpl_consts import FPL_DROPDOWN_MENU_XPATH
from Code.crawler.webcontroller.web_controller import WebController


class FantasyCrawler(WebController):

    def __init__(self, chromedriver: WebDriver):
        super(FantasyCrawler).__init__(chromedriver)

    def get_fpl_stats(self, categories: List[str]) -> List[DataFrame]:
        categories_stats = []

        for category in categories:
            self._click_select_element(FPL_DROPDOWN_MENU_XPATH, category)
            sleep(1)
            category_stats = self._parse_multiple_fpl_pages()
            categories_stats.append(category_stats)

        return categories_stats
