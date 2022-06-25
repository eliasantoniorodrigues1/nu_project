from . import db_design
from . import db_action
from . import db_read_query
from api import read_api
import dateutil.parser
import json
import os
import log


logger = log.get_logger('migration_plan')

BASE_DIR = os.path.abspath(os.path.dirname('main.py'))
MODEL_DIR = os.path.join(BASE_DIR, 'model')
QUERY_DIR = os.path.join(MODEL_DIR, 'query')
SETTINGS_DIR = os.path.join(BASE_DIR, 'settings')
RAW_TABLES_DIR = os.path.join(BASE_DIR, 'raw_tables')

# credentials
with open(os.path.join(SETTINGS_DIR, 'credentials_snow.json'), 'r') as f:
    credentials_snow = json.load(f)

with open(os.path.join(SETTINGS_DIR, 'credentials_star.json'), 'r') as f:
    credentials_star = json.load(f)

# table conf
with open(os.path.join(SETTINGS_DIR, 'tables.json'), 'r') as f:
    data_tables = json.load(f)


def execute_migration_plan(model: str):
    '''
        This funcion runs all the process to create the original
        model and the proposal model.
    '''

    if model == 'snow_flake':
        logger.info(f'Creating {model} schema.')
        # create schema
        conn = db_design.db_conn(credentials=credentials_snow)
        db_design.create_database(conn, credentials_snow['database'])

        # create all tables for snow flake model
        new_conn = db_design.db_conn(credentials_snow)
        tables = data_tables[model + '_tables']
        for table in tables:
            for v in table.values():
                query = f"{v}"
                logger.info(f'Script: {query}')
                db_design.create_table(new_conn, query)

    if model == 'star_schema':
        logger.info(f'Creating {model} schema.')
        # create schema
        conn = db_design.db_conn(credentials=credentials_star)
        db_design.create_database(conn, credentials_star['database'])

        # create all tables for star schema model
        new_conn = db_design.db_conn(credentials_star)
        tables = data_tables[model + '_tables']
        for table in tables:
            for v in table.values():
                query = f"{v}"
                logger.info(f'Script: {query}')
                db_design.create_table(new_conn, query)


def populate_tables(model: str) -> None:
    # insert data into tables

    # generate list to ordering insert
    tbl_names = data_tables[model + '_tables']
    inserts = []
    for dict in tbl_names:
        try:
            name = [tbl_name for tbl_name in dict.keys()]
            inserts.append(*name)
        except AttributeError:
            logger.error('You are trying to get key from a list.')

    if model == 'snow_flake':
        # read raw_tables directory to concat files into just one
        # dataset
        for root, dirs, files in os.walk(RAW_TABLES_DIR):
            for tbl_name in inserts:
                # searching for all files into directory
                list_paths = db_action.consolidate_path_files(
                    os.path.join(root, tbl_name))
                # receive a pandas dataframe to insert into the table from
                # dir name
                logger.info(f'Inserting data into {tbl_name}...')
                df = db_action.concat_dataset(list_paths)
                for column in df.columns:
                    # convert date in datetime
                    if column in data_tables['convert_to_datetime']:
                        df[column] = df[column].apply(
                            dateutil.parser.parse)

                # clean none from transfer_ins and outs
                if tbl_name in ['transfer_ins', 'transfer_outs']:
                    try:
                        df['transaction_completed_at'] = df['transaction_completed_at'].replace(
                            'None', 0)
                    except KeyError:
                        logger.error("Key doesn't exist.")

                if tbl_name == 'pix_movements':
                    try:
                        df['pix_completed_at'] = df['pix_completed_at'].replace(
                            'None', 0)
                    except KeyError:
                        logger.error("Key doesn't exist.")

                if tbl_name == 'investments':
                    try:
                        df = read_api.get_json_investments(list_paths)
                        df['investment_completed_at_timestamp'] = df['investment_completed_at_timestamp'].apply(
                            dateutil.parser.parse)
                    except Exception as e:
                        logger.error(f'Error --> {e}')

                # consolidate inserts limit 1000 rows to improve performance
                list_values = df.values.tolist()
                result_list_values = db_action.split_insert(
                    list_values=list_values, begin=0, step=1000)

                # call function to execute insert
                print('Please wait...')
                conn = db_design.db_conn(credentials=credentials_snow)
                db_action.execute_insert(
                    conn,
                    credentials_snow['database'],
                    tbl_name,
                    df.columns.tolist(),
                    result_list_values,
                )
    else:
        # connect with two databases to performe select and then insert
        snow_conn = db_design.db_conn(credentials=credentials_snow)
        star_conn = db_design.db_conn(credentials=credentials_star)

        # process execution
        db_read_query.execute(snow_conn, star_conn,
                              credentials_star, QUERY_DIR)
