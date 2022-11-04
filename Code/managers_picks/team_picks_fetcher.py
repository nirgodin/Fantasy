import asyncio
from typing import List

import pandas as pd
from aiohttp import ClientSession
from asyncio_pool import AioPool
from pandas import DataFrame
from tqdm import tqdm

from Code.managers_picks.managers_picks_consts import FPL_API_HEADERS, ENTRY

PICKS_ENDPOINT_FORMAT = 'https://fantasy.premierleague.com/api/entry/{}/event/{}/picks/'


class TeamsPicksFetcher:
    def __init__(self, gameweek: int, client_session: ClientSession = None):
        self._gameweek = gameweek
        self._client_session = client_session
        self._progress_bar = None

    async def fetch_teams_picks(self, entry_ids: List[int]):
        print('Starting to fetch top managers picks')
        self._progress_bar = tqdm(total=len(entry_ids))
        pool = AioPool(5)
        entries: List[DataFrame] = await pool.map(self._fetch_single_manager_picks, entry_ids)
        entries_data = pd.concat(entries)
        self._progress_bar.close()

        return entries_data

    async def _fetch_single_manager_picks(self, entry_id: int) -> DataFrame:
        page_url = PICKS_ENDPOINT_FORMAT.format(entry_id, self._gameweek)
        self._progress_bar.update(1)

        async with self._client_session.get(page_url, ssl=False) as response:
            picks_json = await response.json()

        return self._to_dataframe(entry_id=entry_id, picks_json=picks_json)

    def _to_dataframe(self, entry_id: int, picks_json: dict) -> DataFrame:
        if not isinstance(picks_json, dict):
            return pd.DataFrame()

        picks = picks_json['picks']
        picks_data = pd.DataFrame.from_records(picks)
        picks_data[ENTRY] = entry_id

        return picks_data
