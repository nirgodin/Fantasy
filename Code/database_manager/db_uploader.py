from pandas import DataFrame

from Code.database_manager.db_manager import DBManager


class DBUploader:
    def __init__(self, db_manager: DBManager, season: int, gameweek: int):
        self._db_manager = db_manager
        self._season = season
        self._gameweek = gameweek

    def upload_data(self, data: DataFrame, table_name: str) -> None:
        pre_processed_data = self._pre_process_data(data)
        self._db_manager.to_sql(pre_processed_data, table_name)

    def _pre_process_data(self, data: DataFrame) -> DataFrame:
        pre_processed_data = data.copy(deep=True)
        pre_processed_data.insert(0, 'Gameweek', self._gameweek)
        pre_processed_data.insert(0, 'Season', self._season)

        return pre_processed_data
