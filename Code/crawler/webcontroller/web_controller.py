from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.select import Select


class WebController:

    def __init__(self, chromedriver: WebDriver):
        self._driver = chromedriver

    @staticmethod
    def _click_dropdown_menu(select_menu_button: Select, category_name: str) -> None:
        select_menu_button.select_by_visible_text(category_name)

        return None

    def _get_select_menu_button(self, select_menu_xpath: str):
        select_menu_button = self._driver.find_element_by_xpath(select_menu_xpath)

        return select_menu_button