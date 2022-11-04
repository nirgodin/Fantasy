import asyncio
from typing import Dict

import requests
from aiohttp import ClientSession
from pandas import DataFrame

from Code.managers_picks.managers_picks_consts import FPL_API_HEADERS, ENTRY, PLAYER_ID, PLAYER_ELEMENT, ELEMENTS, \
    PLAYER, MANAGERS_PICKS_OUTPUT_OUTPUT_PATH_FORMAT
from Code.managers_picks.team_picks_fetcher import TeamsPicksFetcher
from Code.managers_picks.top_teams_fetcher import TopTeamsFetcher

BOOTSTRAP_STATIC_ENDPOINT = 'https://fantasy.premierleague.com/api/bootstrap-static/'


class TopTeamsPicksManager:
    def __init__(self, season: int, gameweek: int):
        self._season = season
        self._gameweek = gameweek

    async def collect_picks_data(self):
        picks_data = await self._get_picks_data()
        self._add_player_name_column(picks_data)
        players_count = self._get_players_selection_count(picks_data)
        output_path = MANAGERS_PICKS_OUTPUT_OUTPUT_PATH_FORMAT.format(self._season, self._gameweek)

        players_count.to_csv(output_path, index=False)

    async def _get_picks_data(self) -> DataFrame:
        async with ClientSession(headers=FPL_API_HEADERS) as client_session:
            teams_data = await self._fetch_teams_data(client_session)
            picks_data = await self._fetch_picks_data(teams_data=teams_data, client_session=client_session)

        return picks_data.merge(
            right=teams_data,
            on=ENTRY,
            how='left'
        )

    @staticmethod
    async def _fetch_teams_data(client_session: ClientSession) -> DataFrame:
        teams_fetcher = TopTeamsFetcher(client_session=client_session)
        return await teams_fetcher.fetch_top_teams_info()

    async def _fetch_picks_data(self, teams_data: DataFrame, client_session: ClientSession) -> DataFrame:
        entries_ids = teams_data[ENTRY].tolist()
        picks_fetcher = TeamsPicksFetcher(gameweek=self._gameweek, client_session=client_session)

        return await picks_fetcher.fetch_teams_picks(entry_ids=entries_ids)

    def _add_player_name_column(self, picks_data: DataFrame) -> None:
        elements_mapping = self._create_elements_mapping()
        picks_data[PLAYER] = picks_data[PLAYER_ELEMENT].map(elements_mapping)

    @staticmethod
    def _create_elements_mapping() -> Dict[int, str]:
        bootstrap_static_response = requests.get(BOOTSTRAP_STATIC_ENDPOINT)
        jsonified_response = bootstrap_static_response.json()
        game_elements = jsonified_response[ELEMENTS]

        return {element[PLAYER_ID]: element['web_name'] for element in game_elements}

    def _get_players_selection_count(self, picks_data: DataFrame) -> DataFrame:
        entries_number = len(picks_data[ENTRY].unique())
        players_count = picks_data.groupby(PLAYER).count()
        sorted_count = players_count.sort_values(by=PLAYER_ID, ascending=False)
        non_duplicated_count = sorted_count[PLAYER_ID].to_frame()
        non_duplicated_count.columns = ['Count']
        non_duplicated_count.reset_index(level=0, inplace=True)
        non_duplicated_count['Entries Number'] = entries_number
        non_duplicated_count['Season'] = self._season
        non_duplicated_count['Gameweek'] = self._gameweek

        return non_duplicated_count
