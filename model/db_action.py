import os
import pandas as pd
import json
from typing import List
from math import ceil
from datetime import datetime
import log

# log obj
logger = log.get_logger('actions_database')


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

    # logger info
    logger.info(f'List Lengh {lenght} - step {step} - repetitions - {count}')

    for i in range(count):
        if end > lenght:
            end = lenght

        consolidate_list.append([tuple(value_l)
                                for value_l in list_values[begin:end]])
        begin = end
        end += step
    return consolidate_list


def execute_insert(conn, database: str, table: str, list_columns: List, record_list) -> None:
    """
        function to execute insert with dynamic columns
        params: conn: connection with database
                database: str with the name of the database
                table: str with the name of the table
                dataset: raw data to be iterate and insert into the table
    """
    columns = ', '.join([str(column) for column in list_columns])
    # log columns
    logger.info(f'Columns: {columns}')
    try:
        logger.info(f'Sample of values: {record_list[0]}')
    except IndexError:
        logger.error(f'Index error')

    for r in record_list:
        values = [tuple(list_v) for list_v in r]
        query = f'INSERT IGNORE INTO {database}.{table} ({columns}) VALUES ({"%s, " * (len(list_columns)-1) + "%s"});'
        try:
            cursor = conn.cursor()
            cursor.executemany(query, values)
        except Exception as e:
            logger.error(f'Register already inserted. {e}')
        finally:
            conn.commit()
    logger.info('Insert execute successful.')


def concat_dataset(list_path: str) -> pd.DataFrame:
    '''
        function performe an append of two datasets
        param: list_path: a list containing all the files in a directory
        extensions: csv, xlsx, json
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
                elif file.endswith('.json'):
                    with open(file, 'r') as f:
                        investment_data = json.load(f)
                    df = pd.DataFrame(investment_data)
                    df_list.append(df)

            except PermissionError:
                logger.error(
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
    try:
        fmt = '%Y-%m-%dT%H:%M:%S.%fZ'
        date = datetime.strptime(str_date, fmt)
    except ValueError:
        print(str_date)
        fmt = '%Y-%m-%dT%H:%M:%SS.%fZ'
        date = datetime.strptime(str_date, fmt)
    return date


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
            list_datasets.append(os.path.join(root, file))
    return list_datasets
