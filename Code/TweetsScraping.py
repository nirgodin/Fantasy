import json
from datetime import datetime, timedelta
from typing import Iterable, List, Generator, Optional

import pandas as pd
import numpy as np
import time
import tweepy
import pytz
import os

from pandas import DataFrame
from tweepy import API
from tweepy.models import Status

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
bearer = os.getenv('BEARER')
OUTPUT_PATH_FORMAT = r'Data/FPL Status Tweets/from_{}_to_{}.json'
TWITTER_API_DATE_FORMAT = '%Y%m%d%H%M'


class TweetsScraper:
    def __init__(self, end_date: datetime, initial_start_date: datetime, max_results: int = 100):
        self._end_date = end_date
        self._initial_start_date = initial_start_date
        self._normalized_start_date = self._normalize_date_to_api_format(initial_start_date)
        self._max_results = max_results

    def scrape(self, screen_name: str) -> None:
        should_stop_scraping = False
        end_date = self._normalize_date_to_api_format(self._end_date)

        while should_stop_scraping is False:
            query_results = list(self._perform_single_query(screen_name, end_date))

            if not query_results:
                end_date = self._force_end_date_to_subtract(end_date)

            else:
                last_record_date = query_results[0]['created_at']
                self._save_query_results(query_results, last_record_date)
                end_date = last_record_date

            should_stop_scraping = self._should_stop_scraping(query_results, end_date)

    def _perform_single_query(self, screen_name: str, end_date: str) -> Generator[dict, None, None]:
        response: List[Status] = self._api.search_full_archive(
            label='dev',
            query=screen_name,
            fromDate=self._normalized_start_date,
            toDate=end_date,
            maxResults=self._max_results
        )

        for status in response:
            yield {
                'text': status.text,
                'entities': status.entities,
                'created_at': self._normalize_date_to_api_format(status.created_at),
                'account': screen_name
            }

    def _force_end_date_to_subtract(self, start_date: str) -> str:
        normalized_start_date = datetime.strptime(start_date, TWITTER_API_DATE_FORMAT)
        advanced_start_date = normalized_start_date - timedelta(days=7)

        return self._normalize_date_to_api_format(advanced_start_date)

    @staticmethod
    def _save_query_results(query_results: List[dict], last_record_date: str) -> None:
        first_record_date = query_results[-1]['created_at']
        output_path = OUTPUT_PATH_FORMAT.format(first_record_date, last_record_date)
        print(f'Saving query results from start date `{first_record_date}` to end date {last_record_date}')

        with open(output_path, 'w') as f:
            json.dump(query_results, f)

    def _should_stop_scraping(self, query_results: List[dict], last_record_date: Optional[str]) -> bool:
        normalized_last_record_date = datetime.strptime(last_record_date, TWITTER_API_DATE_FORMAT)
        last_record_end_date_gap = (normalized_last_record_date - self._initial_start_date).days

        if last_record_end_date_gap < -1:
            return True

        if not query_results and last_record_end_date_gap < 5:
            return True

        return False

    @staticmethod
    def _normalize_date_to_api_format(date: datetime) -> str:
        return date.strftime(TWITTER_API_DATE_FORMAT)

    @property
    def _api(self) -> API:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        return API(auth, wait_on_rate_limit=True)


if __name__ == '__main__':
    START_DATE = datetime(2020, 9, 1)
    END_DATE = datetime(2022, 10, 2)

    scraper = TweetsScraper(end_date=END_DATE, initial_start_date=START_DATE)
    scraper.scrape('FPLStatus')
