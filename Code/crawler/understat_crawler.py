from selenium.webdriver.chrome.webdriver import WebDriver

from Code.crawler.webcontroller.understat_web_controller import UnderstatWebController


class UnderstatCrawler(UnderstatWebController):

    def __init__(self, chromedriver: WebDriver):
        super(UnderstatCrawler).__init__(chromedriver)
