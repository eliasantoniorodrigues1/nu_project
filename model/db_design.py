from typing import Dict
import mysql.connector
import json
import os


def db_conn(credentials: Dict):
    '''
    this function receives a dictionary with all parameter
    to make a connection with the database.
    param: {
            'host': 'host',
            'user': 'username',
            'password': 'psw'
        }
    '''
    host = credentials['host']
    user = credentials['user']
    password = credentials['password']
    database = credentials['database'] if credentials['database'] != '' else None

    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
    except Exception as e:
        print(f"Database doesn't exist {database}...creating...")
        print(f'Error message --> {e}')
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )

    return conn


def create_database(conn, name: str, collation='utf8mb4'):
    '''
        this function receives a connection with a server
        and a string that contains a name to create a database.
    '''
    query = f'CREATE DATABASE IF NOT EXISTS {name} DEFAULT CHARACTER SET {collation};'
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    print(f'Database {name} create successful with {collation} configuration.')


def drop_database(conn, name: str):
    '''
        drop database
    '''
    cursor = conn.cursor()
    cursor.execute(f'DROP DATABASE IF EXISTS {name};')
    print(f'Database {name} was deleted with successful.')


def create_table(conn, query: str):
    '''
        this function will create a table with the
        name parameter sended by user.
        *args can be a dictionary with all settings for the columns of
        table
    '''
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    print(f'Query {query} executed successeful.')


if __name__ == '__main__':
    BASE_DIR = os.path.abspath(os.path.dirname('main.py'))
    MODEL_DIR = os.path.join(BASE_DIR, 'model')

    # drop
    # drop_database(conn, 'nu_snow_flake_2')

    # file to string connection
    with open(os.path.join(MODEL_DIR, 'credentials.json'), 'r') as f:
        credentials = json.load(f)

    # file with table configurations
    with open(os.path.join(MODEL_DIR, 'tables.json'), 'r') as f:
        data_tables = json.load(f)

    # create schema
    conn = db_conn(credentials=credentials)
    create_database(conn, credentials['database'])

    # create all tables
    new_conn = db_conn(credentials)
    tables = data_tables['snow_flake_tables']
    for table in tables:
        for v in table.values():
            query = f"{v}"
            print(query)
            create_table(new_conn, query)
