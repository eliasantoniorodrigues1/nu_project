from typing import Dict
import mysql.connector
import log

# log creation schema
logger = log.get_logger('design_database')


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

    # log credentials
    logger.info(
        f'Credentials: host={host}, user={user}, password=*****, database={database}')

    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
    except Exception as e:
        logger.info(f"Database doesn't exist {database}...creating...")
        logger.error(f'Error message --> {e}')
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

    # drop database before create
    drop_database(conn=conn, name=name)

    query = f'CREATE DATABASE IF NOT EXISTS {name} DEFAULT CHARACTER SET {collation};'
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    logger.info(
        f'Database {name} create successful with {collation} configuration.')


def drop_database(conn, name: str):
    '''
        drop database
    '''
    cursor = conn.cursor()
    cursor.execute(f'DROP DATABASE IF EXISTS {name};')
    logger.info(f'Database {name} was deleted with successful.')


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
    logger.info(f'Query {query} executed successeful.')



