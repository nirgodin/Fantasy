from Code.crawler.consts.fpl_consts import FPL_EXPORT_PATH_TEMPLATE


class FantasyCrawlerUtils:

    def __init__(self):
        pass

    @staticmethod
    def get_fpl_export_path(season: str, gameweek: str) -> str:
        return fr'{FPL_EXPORT_PATH_TEMPLATE[0]}{season}{FPL_EXPORT_PATH_TEMPLATE[1]}{gameweek}.csv'
