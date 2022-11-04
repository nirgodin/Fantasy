from typing import List

import pandas as pd
from aiohttp import ClientSession
from asyncio_pool import AioPool
from pandas import DataFrame
from tqdm import tqdm

OVERALL_LEAGUE_ID = 314
TOP_TEAMS_NUMBER = 10000
STANDINGS_PER_PAGE = 50
STANDINGS_ROUTE_FORMAT = 'https://fantasy.premierleague.com/api/leagues-classic/{}/standings?page_standings={}'


class TopTeamsFetcher:
    def __init__(self, client_session: ClientSession = None):
        self._client_session = client_session
        self._progress_bar = None

    async def fetch_top_teams_info(self) -> DataFrame:
        print('Starting to fetch top managers team ids')
        number_of_pages = round(TOP_TEAMS_NUMBER / STANDINGS_PER_PAGE)
        self._progress_bar = tqdm(total=number_of_pages)
        pool = AioPool(5)
        pages: List[DataFrame] = await pool.map(self._fetch_single_page, range(1, number_of_pages + 2))
        valid_pages = [page for page in pages if isinstance(page, DataFrame)]
        self._progress_bar.close()

        return pd.concat(valid_pages)

    async def _fetch_single_page(self, page_number: int) -> DataFrame:
        page_url = STANDINGS_ROUTE_FORMAT.format(OVERALL_LEAGUE_ID, page_number)
        self._progress_bar.update(1)

        async with self._client_session.get(page_url, ssl=False) as response:
            page_data = await response.json()

        standings = page_data['standings']['results']

        return pd.DataFrame.from_records(standings)
