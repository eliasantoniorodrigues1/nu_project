#import model.db_design as db_design
#import model.db_action as db_action
import model.db_migration_plan as migration
#import api.read_api as read_api
#from calculate_earnings import calc_investment_earning
import dateutil.parser
from datetime import datetime
import os
import json
import log

logger = log.get_logger('main_execution')

if __name__ == '__main__':
    """ 
    BASE_DIR = os.path.abspath(os.path.dirname('main.py'))
    MODEL_DIR = os.path.join(BASE_DIR, 'model')
    SETTINGS_DIR = os.path.join(BASE_DIR, 'settings')
    RAW_TABLES_DIR = os.path.join(BASE_DIR, 'raw_tables')
     """
    # execution time
    start = datetime.now()
    logger.info(f'Proccess started at {start}')

    # process creation of schemas
    migration.execute_migration_plan()

    # load files from settins
    # credentials


    """     
    with open(os.path.join(SETTINGS_DIR, 'credentials.json'), 'r') as f:
        credentials = json.load(f)

    # original schema
    credentials = credentials['original_schema']

    # table conf
    with open(os.path.join(SETTINGS_DIR, 'tables.json'), 'r') as f:
        data_tables = json.load(f)

    # create schema
    conn = db_design.db_conn(credentials=credentials)
    db_design.create_database(conn, credentials['database'])

    # create all tables
    new_conn = db_design.db_conn(credentials)
    tables = data_tables['snow_flake_tables']
    for table in tables:
        for v in table.values():
            query = f"{v}"
            print(query)
            db_design.create_table(new_conn, query)

    """    
    """ 
    # insert data into tables
    # generate list to ordering insert
    tbl_names = data_tables['snow_flake_tables']
    inserts = []
    for dict in tbl_names:
        name = [tbl_name for tbl_name in dict.keys()]
        inserts.append(*name)
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
                        db_action.iso8601_to_datetime)

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
            conn = db_design.db_conn(credentials=credentials)
            db_action.execute_insert(
                conn,
                credentials['database'],
                tbl_name,
                df.columns.tolist(),
                result_list_values,
            ) """

    # logger.info(f'Execution time takes {datetime.now() - start}')

    # calculate investments earning
