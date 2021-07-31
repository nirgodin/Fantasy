from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.select import Select


class WebController:

    def __init__(self, chromedriver: WebDriver):
        self._driver = chromedriver

    @staticmethod
    def _click_next_page_button(next_page_button) -> None:
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
