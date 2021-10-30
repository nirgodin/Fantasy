from pandas import DataFrame
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.select import Select
from Code.table_parser.html_table_parser import HTMLTableParser


class WebController(HTMLTableParser):

    def __init__(self, chromedriver: WebDriver):
        super(WebController).__init__()
        self._driver = chromedriver

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
