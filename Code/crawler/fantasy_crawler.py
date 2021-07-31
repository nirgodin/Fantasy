from time import sleep
from typing import List
from pandas import DataFrame
from Code.crawler.webcontroller.web_controller import WebController


class FPLCrawler(WebController):

    def __init__(self, chromedriver):
        super(FPLCrawler).__init__(chromedriver)

    def get_fpl_stats(self, categories: List[str]) -> List[DataFrame]:
        categories_stats = []

        for category in categories:
            self._click_dropdown_menu(self._dropdown_menu_button, category)
            sleep(1)
            category_stats = self._parse_multiple_pages()
            categories_stats.append(category_stats)

        return categories_stats
