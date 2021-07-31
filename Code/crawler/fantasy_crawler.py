from Code.crawler.webcontroller.web_controller import WebController


class FantasyCrawler(WebController):

    def __init__(self, chromedriver):
        super(FantasyCrawler).__init__(chromedriver)
