from functools import reduce
from typing import List
import pandas as pd
from pandas import DataFrame
from Code.crawler.consts.fpl_consts import PLAYER, ROLE, TEAM, TWO_ASTERISKS, FPL_CATEGORIES, FPL_REPEATED_CATEGORIES


class CrawlerPreProcessing:
    
    def __init__(self):
        pass

    def get_player_name_team_and_role(self, scraped_data: DataFrame):
        players = [self._split_player_name(name)[PLAYER] for name in scraped_data[PLAYER]]
        teams = [self._split_player_name(name)[TEAM] for name in scraped_data[PLAYER]]
        roles = [self._split_player_name(name)[ROLE] for name in scraped_data[PLAYER]]

        organized_data = scraped_data.copy()
        organized_data[PLAYER] = players
        organized_data.insert(2, ROLE, roles)
        organized_data.insert(1, TEAM, teams)

        return organized_data

    @staticmethod
    def _split_player_name(scraped_player_name: str) -> dict:
        """
        When scraped, players names are concatenated to teams names and role.
        This functions takes the original scraped name as argument and returns the player's name, team and role
        """
        player_details = {PLAYER: scraped_player_name[0:len(scraped_player_name) - 6],
                          TEAM: scraped_player_name[len(scraped_player_name) - 6:len(scraped_player_name) - 3],
                          ROLE: scraped_player_name[len(scraped_player_name) - 3:len(scraped_player_name)]}

        return player_details

    @staticmethod
    def subset_categories_columns(data: DataFrame):
        return data[FPL_CATEGORIES]

    @staticmethod
    def merge_categories(categories_stats: List[DataFrame]) -> DataFrame:
        return reduce(lambda left, right: pd.merge(left,
                                                   right,
                                                   on=FPL_REPEATED_CATEGORIES,
                                                   how='outer'),
                      categories_stats)

    @staticmethod
    def rename_asterisks_column_with_category(category_stats: DataFrame, category_name: str) -> DataFrame:
        category_stats.rename(columns={TWO_ASTERISKS: category_name}, inplace=True)
        return category_stats
