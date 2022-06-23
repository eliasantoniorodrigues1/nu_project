from datetime import datetime
import os
import pandas as pd
from db_design import db_conn
import json
from typing import List
from math import ceil
from datetime import datetime
import itertools


def split_insert(list_values: list, begin: int, step: int):
    '''
        function to iterate for dataset consolidating values to performe an
        insert in batch
        params: datase: a pandas dataframe containing values for insert into
        database
        params: begin: int containing initial step
        params: step: int to limit the max rows os insert
    '''
    lenght = len(list_values)
    end = step
    count = ceil(lenght / step)
    consolidate_list = []
    for i in range(count):
        if end > lenght:
            end = lenght

        consolidate_list.append([tuple(value_l)
                                for value_l in list_values[begin:end]])
        begin = end
        end += step
    # print(*consolidate_list)
    return consolidate_list


def execute_insert(conn, database: str, table: str, list_columns: List, record_list) -> None:
    """
        function to execute insert with dynamic columns
        params: conn: connection with database
                database: str with the name of the database
                table: str with the name of the table
                dataset: raw data to be iterate and insert into the table
    """
    # print(f'--->>>> {record_list[0]}')
    columns = ', '.join([str(column) for column in list_columns])
    for r in record_list:
        # values = ', '.join([str(tuple(list_v)) for list_v in r])
        values = [tuple(list_v) for list_v in r]
        query = f'INSERT IGNORE INTO {database}.{table} ({columns}) VALUES ({"%s, " * (len(list_columns)-1) + "%s"});'
        # query = f'INSERT INTO {database}.{table} ({columns}) VALUES {values};'

        try:
            cursor = conn.cursor()
            cursor.executemany(query, values)
        except Exception as e:
            print(f'Register already inserted. {e}')
        finally:
            conn.commit()
    print('Insert execute successful.')


def concat_dataset(list_path: str) -> pd.DataFrame:
    '''
        function performe an append of two datasets
        param: list_path: a list containing all the files in a directory
    '''
    if len(list_path) > 1:
        df_list = []
        for file in list_path:
            try:
                if file.endswith('.csv'):
                    # read file
                    df = pd.read_csv(file)
                    # insert dataset into my list
                    df_list.append(df)
                elif file.endswith('.xlsx'):
                    # read xlsx
                    df = pd.read_excel(file)
                    # insert dataset into my list
                    df_list.append(df)
            except PermissionError:
                print(
                    'File not read. Please close the file to continue and then run again.')

        return pd.concat(df_list)

    # if my list contains just one path, the script
    # don't will concatenate
    try:
        file = list_path[0]
    except:
        return pd.DataFrame()

    if file.endswith('.csv'):
        return pd.read_csv(file)
    elif file.endswith('.xlsx'):
        return pd.read_excel(file)

    return pd.DataFrame()


def iso8601_to_datetime(str_date: str) -> datetime:
    '''
        function convert date utc iso8601 in datetime
        param: str_date: string containig the date value
    '''
    fmt = '%Y-%m-%dT%H:%M:%S.%fZ'
    return datetime.strptime(str_date, fmt)


def consolidate_path_files(fullpath: str):
    '''
        function create to walk trogh directory
        and consolidate into a list the full path o
        a dataset file
        param: fullpath: str containing the raw database
    '''
    list_datasets = []
    for root, _, files in os.walk(fullpath):
        for file in files:
            # print(file)
            list_datasets.append(os.path.join(root, file))
    return list_datasets


if __name__ == '__main__':
    # execution time
    start = datetime.now()

    BASE_DIR = os.path.abspath(os.path.dirname('main.py'))
    MODEL_DIR = os.path.join(BASE_DIR, 'model')
    RAW_TABLE_DIR = os.path.join(BASE_DIR, 'raw_tables')

    # file to string connection
    with open(os.path.join(MODEL_DIR, 'credentials.json'), 'r') as f:
        credentials = json.load(f)

    # file with table configurations
    with open(os.path.join(MODEL_DIR, 'tables.json'), 'r') as f:
        data_tables = json.load(f)

    # generate list to ordering insert
    tbl_names = data_tables['snow_flake_tables']
    inserts = []
    for dict in tbl_names:
        name = [tbl_name for tbl_name in dict.keys()]
        inserts.append(*name)
    # read raw_tables directory to concat files into just one
    # dataset
    for root, dirs, files in os.walk(RAW_TABLE_DIR):
        for tbl_name in inserts:
            # searching for all files into directory
            list_paths = consolidate_path_files(os.path.join(root, tbl_name))
            # receive a pandas dataframe to insert into the table from
            # dir name
            print(f'Inserting data into {tbl_name}...')
            df = concat_dataset(list_paths)
            for column in df.columns:
                # convert date in datetime
                if column in data_tables['convert_to_datetime']:
                    df[column] = df[column].apply(iso8601_to_datetime)

            # clean none from transfer_ins and outs
            if tbl_name in ['transfer_ins', 'transfer_outs']:
                try:
                    df['transaction_completed_at'] = df['transaction_completed_at'].replace(
                        'None', 0)
                except KeyError:
                    print("Key doesn't exist.")

            if tbl_name == 'pix_movements':
                try:
                    df['pix_completed_at'] = df['pix_completed_at'].replace(
                        'None', 0)
                except KeyError:
                    print("Key doesn't exist.")

            # consolidate inserts limit 1000 rows
            list_values = df.values.tolist()
            result_list_values = split_insert(
                list_values=list_values, begin=0, step=1000)


            # call function to execute insert
            print('Please wait...')
            conn = db_conn(credentials=credentials)
            execute_insert(
                conn,
                credentials['database'],
                tbl_name,
                df.columns.tolist(),
                result_list_values,
            )
    print(f'Execution time was {datetime.now() - start}')
