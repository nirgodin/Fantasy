from Code.crawler.consts.fpl_consts import FPL_EXPORT_PATH_TEMPLATE
from Code.crawler.consts.understat_consts import UNDERSTAT_PLAYERS_EXPORT_PATH_TEMPLATE, \
    UNDERSTAT_TEAMS_EXPORT_PATH_TEMPLATE


class FantasyCrawlerUtils:

    def __init__(self):
        pass

    @staticmethod
    def get_fpl_export_path(season: str, gameweek: str) -> str:
        return fr'{FPL_EXPORT_PATH_TEMPLATE[0]}{season}{FPL_EXPORT_PATH_TEMPLATE[1]}{gameweek}.csv'

    @staticmethod
    def get_understat_players_export_path(season: str, gameweek: str) -> str:
        return fr'{UNDERSTAT_PLAYERS_EXPORT_PATH_TEMPLATE[0]}{season}{UNDERSTAT_PLAYERS_EXPORT_PATH_TEMPLATE[1]}{gameweek}.csv'

    @staticmethod
    def get_understat_teams_export_path(season: str, gameweek: str) -> str:
        return fr'{UNDERSTAT_TEAMS_EXPORT_PATH_TEMPLATE[0]}{season}{UNDERSTAT_TEAMS_EXPORT_PATH_TEMPLATE[1]}{gameweek}.csv'
