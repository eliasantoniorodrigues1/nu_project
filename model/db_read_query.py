import os
from . import db_design
from . import db_action
import json
import log

# log obj
logger = log.get_logger('populating_star_model')

'''
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

'''


def execute(conn_select, conn_insert, credentials_star, query_dir: str):
    '''
        this function receives two connection to perform
        select from database and then insert into star model
        database.
        param: conn_select: connection to perform select
        param: conn_insert: connection to perform insert
        param: query_dir: directory from files .sql
    '''
    cursor = conn_select.cursor()
    for root, _, files in os.walk(query_dir):
        for file in files:
            print(f'Inserindo dados em {file[:-4]}')
            if file.endswith('.sql'):
                with open(os.path.join(root, file), 'r') as f:
                    query = f.read()
                    cursor.execute(query)
                    r = cursor.fetchall()

                    # removing datetime from query result
                    # df = pd.DataFrame(r)
                    list_insert = db_action.split_insert(
                        list(r), begin=0, step=1000)
                    logger.info(f'Inserting {len(list_insert)} registers.')
                    db_action.execute_insert_simple(
                        conn_insert, credentials_star['database'], file[:-4],
                        list_insert)
