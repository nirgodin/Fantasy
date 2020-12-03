import psycopg2
import pandas as pd
import os
from datetime import datetime

# First, we set the season, current gameweek and previous gameweek variables
season = '21'
previous_GW = '9'
current_GW = '10'

# Create the functions that will connect between python and the sql database, create and populate the tables
# Credit to Niels Goet from TowardsDataScience for these functions. they can be found here:
# https://towardsdatascience.com/how-to-build-a-relational-database-from-csv-files-using-python-and-heroku-20ea89a55c63


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


# Creating the tables that will be later populated.
# This code runs one time when uploading a new table, and then is commented out.


#######################################################################################################################

# # Fantasy Table
# fantasy_schema = """
# season REAL,
# gameweek REAL,
# player VARCHAR,
# team VARCHAR(3),
# role VARCHAR(3),
# cost REAL,
# sel VARCHAR,
# form REAL,
# pts REAL,
# minutes_played REAL,
# goals_scored REAL,
# assists REAL,
# clean_sheets REAL,
# goals_conceded REAL,
# own_goals REAL,
# penalties_saved REAL,
# penalties_missed REAL,
# yellow_cards REAL,
# red_cards REAL,
# saves REAL,
# bonus REAL,
# bonus_points_system REAL,
# influence REAL,
# creativity REAL,
# threat REAL,
# ict_index REAL,
# form1 REAL,
# times_in_dream_team REAL,
# value_form REAL,
# value_season REAL,
# points_per_match REAL,
# transfers_in REAL,
# transfers_out REAL,
# price_rise REAL,
# price_fall REAL
# """
#
# # Creating the fantasy table
# create_table(table='fantasy',
#              schema=fantasy_schema)

#######################################################################################################################

# # xg_players table
# xg_players_schema = """
# season REAL,
# gameweek REAL,
# player VARCHAR,
# team VARCHAR(3),
# appearances REAL,
# minutes_played REAL,
# goals_scored REAL,
# npg REAL,
# assists REAL,
# xg REAL,
# npxg REAL,
# xa REAL,
# xgchain REAL,
# xgbuildup REAL,
# xg90 REAL,
# npxg90 REAL,
# xa90 REAL,
# xg90_plus_xa90 REAL,
# npxg90_plus_xa90 REAL,
# xgchain90 REAL,
# xgbuildup90 REAL
# """
#
# # Creating the xg_players table
# create_table(table='xg_players',
#              schema=xg_players_schema)

#######################################################################################################################

# # xg_teams table
# xg_teams_schema = """
# season REAL,
# gameweek REAL,
# ranking REAL,
# team VARCHAR (3),
# m REAL,
# w REAL,
# d REAL,
# l REAL,
# g REAL,
# ga REAL,
# pts REAL,
# xg REAL,
# npxg REAL,
# xga REAL,
# npxga REAL,
# npxgd REAL,
# ppda REAL,
# oppda REAL,
# dc REAL,
# odc REAL,
# xpts REAL
# """
#
# # Creating the xg_teams table
# create_table(table='xg_teams',
#              schema=xg_teams_schema)

#######################################################################################################################

# # Schedule Table
# schedule_schema = """
# team VARCHAR(3) PRIMARY KEY NOT NULL,
# gw_1 VARCHAR(3),
# gw_2 VARCHAR(3),
# gw_3 VARCHAR(3),
# gw_4 VARCHAR(3),
# gw_5 VARCHAR(3),
# gw_6 VARCHAR(3),
# gw_7 VARCHAR(3),
# gw_8 VARCHAR(3),
# gw_9 VARCHAR(3),
# gw_10 VARCHAR(3),
# gw_11 VARCHAR(3),
# gw_12 VARCHAR(3),
# gw_13 VARCHAR(3),
# gw_14 VARCHAR(3),
# gw_15 VARCHAR(3),
# gw_16 VARCHAR(3),
# gw_17 VARCHAR(3),
# gw_18 VARCHAR(3),
# gw_19 VARCHAR(3),
# gw_20 VARCHAR(3),
# gw_21 VARCHAR(3),
# gw_22 VARCHAR(3),
# gw_23 VARCHAR(3),
# gw_24 VARCHAR(3),
# gw_25 VARCHAR(3),
# gw_26 VARCHAR(3),
# gw_27 VARCHAR(3),
# gw_28 VARCHAR(3),
# gw_29 VARCHAR(3),
# gw_30 VARCHAR(3),
# gw_31 VARCHAR(3),
# gw_32 VARCHAR(3),
# gw_33 VARCHAR(3),
# gw_34 VARCHAR(3),
# gw_35 VARCHAR(3),
# gw_36 VARCHAR(3),
# gw_37 VARCHAR(3),
# gw_38 VARCHAR(3)
# """
#
# create_table(table='s21_schedule',
#              schema=schedule_schema)

#######################################################################################################################

# Load and populate the fantasy table
cum_curr_fpl = pd.read_csv(r'FPL/FPL_S' + season + '_GW1_' + current_GW + '.csv').fillna('-')

# Transforming the column names to a suitable format for a SQL database (lowercase, no spaces, parenthesis or dots)
for col in cum_curr_fpl.columns.tolist():
    cum_curr_fpl = cum_curr_fpl.rename(columns={col: col.lower()
                                                        .replace(' ', '_')
                                                        .replace('(', '')
                                                        .replace(')', '')
                                                        .replace('.', '')})

# Deleting apostrophes in the players' names, which causes troubles to upload to the sql database
cum_curr_fpl['player'] = [player.replace("'", "") for player in cum_curr_fpl['player']]

# Inserting season and gameweek variables to the dataframe, to help distinguish between different seasons and weeks
cum_curr_fpl.insert(0, 'gameweek', current_GW)
cum_curr_fpl.insert(0, 'season', season)

# Populating the table
populate_table(table_name='fantasy',
               df=cum_curr_fpl)

#######################################################################################################################

# Load and populate the xg_players table
cum_curr_xG = pd.read_csv(r'Understat\xG_S' + season + '_GW1_' + current_GW + '.csv').fillna('-')

# Transforming the column names to a suitable format for a SQL database (lowercase, no spaces and parenthesis)
for col in cum_curr_xG.columns.tolist():
    cum_curr_xG = cum_curr_xG.rename(columns={col: col.lower()
                                                      .replace('player_', '')
                                                      .replace(' ', '_')
                                                      .replace('+', '_plus_')})

# Deleting apostrophes in the players' names, which causes troubles to upload to the sql database
cum_curr_xG['player'] = [player.replace("'", "") for player in cum_curr_xG['player']]

# Inserting season and gameweek variables to the dataframe, to help distinguish between different seasons and weeks
cum_curr_xG.insert(0, 'gameweek', current_GW)
cum_curr_xG.insert(0, 'season', season)

# Populating the table
populate_table(table_name='xg_players',
               df=cum_curr_xG)

#######################################################################################################################

# Load and populate the PLT_teams table
cum_curr_PLT = pd.read_csv(r'PLT\PLT_S' + season + '_GW1_' + current_GW + '.csv').fillna('-')

# Transforming the column names to a suitable format for a SQL database (lowercase, no spaces and parenthesis)
for col in cum_curr_PLT.columns.tolist():
    cum_curr_PLT = cum_curr_PLT.rename(columns={col: col.lower()
                                                        .replace('team_', '')})

# Inserting season and gameweek variables to the dataframe, to help distinguish between different seasons and weeks
cum_curr_PLT.insert(0, 'gameweek', current_GW)
cum_curr_PLT.insert(0, 'season', season)

# Populating the table
populate_table(table_name='xg_teams',
               df=cum_curr_PLT)

#######################################################################################################################

# Import the schedule of all the teams

# Load and populate the schedule table.
# This is commented out until there will be a new season and a new schedule to load
Schedule = pd.read_csv(r'Schedule\Schedule_S21.csv').fillna('-')

# Adding 'gw_' introduction to all the column names besides team, to avoid numeric column names
for col in Schedule.columns.drop('Team'):
    Schedule = Schedule.rename(columns={col: 'gw_' + col})

# Lowercase the team column name, to better suit SQL
Schedule = Schedule.rename(columns={'Team': 'team'})

# Populating the table
populate_table(table_name='s21_schedule',
               df=Schedule)

