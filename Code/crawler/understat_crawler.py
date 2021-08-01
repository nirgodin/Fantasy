from selenium.webdriver.chrome.webdriver import WebDriver

from Code.crawler.webcontroller.fpl_web_controller import WebController


class UnderstatCrawler(WebController):

    def __init__(self, chromedriver: WebDriver):
        super(UnderstatCrawler).__init__(chromedriver)
