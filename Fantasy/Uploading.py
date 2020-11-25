import psycopg2
import pandas as pd
import os
from datetime import datetime

os.environ
def run_syntax(db_connection: psycopg2, syntax: str) -> None:
    """
    Run syntax.
    :param db_connection: Database connection object.
    :param syntax: Syntax for execution.
    """
    cur = db_connection.cursor()
    cur.execute(syntax)
    cur.close()


def create_table(schema: str, table: str) -> None:
    """
    Create a table in the DB based on a schema.
    :param schema: The table schema.
    :param schema: The schema.
    :param table: The name of the table.
    """
    db_connection = psycopg2.connect(
        host=os.environ["hostname"],
        user=os.environ["user"],
        password=os.environ["password"],
        dbname=os.environ["database"],
    )

    # Create table if it does not yet exist
    run_syntax(db_connection=db_connection, syntax=f"CREATE TABLE IF NOT EXISTS {table}({schema})")

    db_connection.commit()
    db_connection.close()


def populate_table(table_name: str, df: pd.DataFrame) -> None:
    """
    Populate a table in the database from a pandas dataframe.
    :param table_name: The name of the table in the DB that we will add the values in df to.
    :param df: The dataframe that we use for puplating the table.
    """
    db_connection = psycopg2.connect(
        host=os.environ["hostname"],
        user=os.environ["user"],
        password=os.environ["password"],
        dbname=os.environ["database"],
    )

    # Check that all columns are present in the CSV file
    cur = db_connection.cursor()
    cur.execute(f"SELECT * FROM {table_name} LIMIT 0")
    cur.close()

    col_names = [i[0] for i in cur.description]
    df["row_timestamp"] = [datetime.now().strftime("%m-%d-%Y %H:%M:%S")] * len(df.index)

    missing_columns = set(col_names).difference(df.columns)
    assert not missing_columns, f"The following columns are missing in your CSV file: {','.join(missing_columns)}"

    # Re-order CSV
    df = df[col_names]

    # Inject data
    for index, row in df.iterrows():
        run_syntax(db_connection=db_connection, syntax=f"INSERT INTO {table_name} VALUES{tuple(row.values)}")
    db_connection.commit()
    db_connection.close()


# Import the schedule of all the teams
Schedule = pd.read_csv(r'Schedule\Schedule_S21.csv')
Schedule = Schedule.fillna('-')
for col in Schedule.columns.drop('Team'):
    Schedule = Schedule.rename(columns={col: 'gw_' + col})
Schedule = Schedule.rename(columns={'Team': 'team'})

schedule_schema = """
team VARCHAR(3) PRIMARY KEY NOT NULL,
gw_1 VARCHAR(3),
gw_2 VARCHAR(3),
gw_3 VARCHAR(3),
gw_4 VARCHAR(3),
gw_5 VARCHAR(3),
gw_6 VARCHAR(3),
gw_7 VARCHAR(3),
gw_8 VARCHAR(3),
gw_9 VARCHAR(3),
gw_10 VARCHAR(3),
gw_11 VARCHAR(3),
gw_12 VARCHAR(3),
gw_13 VARCHAR(3),
gw_14 VARCHAR(3),
gw_15 VARCHAR(3),
gw_16 VARCHAR(3),
gw_17 VARCHAR(3),
gw_18 VARCHAR(3),
gw_19 VARCHAR(3),
gw_20 VARCHAR(3),
gw_21 VARCHAR(3),
gw_22 VARCHAR(3),
gw_23 VARCHAR(3),
gw_24 VARCHAR(3),
gw_25 VARCHAR(3),
gw_26 VARCHAR(3),
gw_27 VARCHAR(3),
gw_28 VARCHAR(3),
gw_29 VARCHAR(3),
gw_30 VARCHAR(3),
gw_31 VARCHAR(3),
gw_32 VARCHAR(3),
gw_33 VARCHAR(3),
gw_34 VARCHAR(3),
gw_35 VARCHAR(3),
gw_36 VARCHAR(3),
gw_37 VARCHAR(3),
gw_38 VARCHAR(3)
"""

create_table(table='s21_schedule',
             schema=schedule_schema)

populate_table(table_name='s21_schedule',
               df=Schedule)



