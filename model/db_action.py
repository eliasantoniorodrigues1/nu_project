import os
import pandas as pd
from db_design import db_conn
import json


def execute_insert(conn, database, table, dataset):
    """ 
        function to execute insert with dynamic columns
        params: conn: connection with database
                database: str with the name of database
                table: str with the name of table
                dataset: raw data to be iterate and insert into the table
    """
    columns = ', '.join([str(column) for column in dataset.columns.tolist()])
    # loop througut dataset
    for _, row in dataset.iterrows():
        # print(tuple(row))
        # query = f'INSERT INTO {database}.{table} ({columns}) VALUES ({"%s, " * (len(row)-1) + "%s"});'
        query = f'INSERT INTO {database}.{table} ({columns}) VALUES {tuple(row)};'
        print(query)
        cursor = conn.cursor()
        cursor.execute(query)
        # cursor.execute(query, tuple(row))
        cursor.commit()
    print('Insert execute with success.')


def concat_dataset(list_path: str) -> pd.DataFrame:
    if len(list_path) > 1:
        df_list = []
        for file in list_path:
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
        return pd.concat(df_list)

    # if my list contains just one path, the script
    # don't will concatenate
    file = list_path[0]
    if file.endswith('.csv'):
        return pd.read_csv(file)
    elif file.endswith('.xlsx'):
        return pd.read_excel(file)

    return pd.DataFrame()


def consolidate_path_files(fullpath: str):
    list_datasets = []
    for root, _, files in os.walk(fullpath):
        for file in files:
            # print(file)
            list_datasets.append(os.path.join(root, file))
    return list_datasets


if __name__ == '__main__':
    BASE_DIR = os.path.abspath(os.path.dirname('main.py'))
    MODEL_DIR = os.path.join(BASE_DIR, 'model')
    RAW_TABLE_DIR = os.path.join(BASE_DIR, 'raw_tables')

    # file to string connection
    with open(os.path.join(MODEL_DIR, 'credentials.json'), 'r') as f:
        credentials = json.load(f)

    # read raw_tables directory to concat files into just one
    # dataset
    for root, dirs, files in os.walk(RAW_TABLE_DIR):
        for dir in dirs:
            # searching for all files into directory
            list_paths = consolidate_path_files(os.path.join(root, dir))
            print(dir)
            # receive a pandas dataframe to insert into the table from
            # dir name
            df = concat_dataset(list_paths)
            # print(df.head())
            # call function to execute insert
            conn = db_conn(credentials=credentials)
            execute_insert(
                conn=conn,
                database=credentials['database'],
                table=dir,
                dataset=df
            )
