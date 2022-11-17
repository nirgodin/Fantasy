from pandas import DataFrame
from sqlalchemy import create_engine


class DBManager:
    def __init__(self, connection_url: str):
        self._connection_url = connection_url

    def to_sql(self, data: DataFrame, table_name: str) -> None:
        sql_engine = create_engine(self._connection_url, echo=False, pool_timeout=360)

        with sql_engine.connect() as connection:
            data.to_sql(
                name=table_name,
                con=connection,
                if_exists="append",
                index=False
            )
