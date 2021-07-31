from pandas import DataFrame

from Code.crawler.consts import PLAYER_COLUMN_NAME, ROLE_COLUMN_NAME, TEAM_COLUMN_NAME


class CrawlerPreProcessing:
    
    def __init__(self):
        pass

    def get_player_name_team_and_role(self, scraped_data: DataFrame):
        player_names = [self._split_player_name(name)['player name'] for name in scraped_data[PLAYER_COLUMN_NAME]]
        team_names = [self._split_player_name(name)['team name'] for name in scraped_data[PLAYER_COLUMN_NAME]]
        roles = [self._split_player_name(name)['role'] for name in scraped_data[PLAYER_COLUMN_NAME]]

        organized_data = scraped_data.copy()
        organized_data[PLAYER_COLUMN_NAME] = player_names
        organized_data.insert(2, ROLE_COLUMN_NAME, roles)
        organized_data.insert(1, TEAM_COLUMN_NAME, team_names)

        return organized_data

    @staticmethod
    def _split_player_name(scraped_player_name: str) -> dict:
        """
        When scraped, players names are concatenated to teams names and role.
        This functions takes the original scraped name as argument and returns the player's name, team and role
        """
        player_details = {'player name': scraped_player_name[0:len(scraped_player_name) - 6],
                          'team name': scraped_player_name[len(scraped_player_name) - 6:len(scraped_player_name) - 3],
                          'role': scraped_player_name[len(scraped_player_name) - 3:len(scraped_player_name)]}

        return player_details
