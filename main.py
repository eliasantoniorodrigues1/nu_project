from datetime import datetime
from dateutil import parser
import os
import json
import pandas as pd
from typing import List
from math import ceil
import time
from datetime import datetime


def execute_insert(conn, database: str, table: str, dataset: pd.DataFrame) -> None:
    """ 
        function to execute insert with dynamic columns
        params: conn: connection with database
                database: str with the name of the database
                table: str with the name of the table
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
        try:
            cursor.execute(query)
            # cursor.execute(query, tuple(row))
        except Exception as e:
            print(e)
        finally:
            conn.commit()

    print('Insert execute with success.')


def divide_insert(lista, inicio, passo):
    # Essa função recebe uma lista contendo os values do seu insert
    # inicio e passo, para dividir em uma sublista para fazer insert
    # por lotes. Exemplo realizar um insert de 1000 em 1000
    # inicio = 0 passo = 1000
    # print(f'Lista recebida -->> {lista}')
    tamanho = len(lista)
    fim = passo
    qtde = ceil(len(lista) / passo)
    lista_consolidada = []

    for i in range(qtde):
        print(i)
        if fim > tamanho:
            fim = tamanho

        lista_consolidada.append(tuple(*lista[inicio:fim]))

        inicio = fim
        fim += passo
    # print(f'Lista retornada --> {lista_consolidada}')
    return lista_consolidada


""" data = '2019-04-19T01:34:25.000Z'


def iso8601_to_datetime(str_date: str) -> datetime:
    fmt = '%Y-%m-%dT%H:%M:%S.%fZ'
    return datetime.strptime(str_date, fmt)


BASE_DIR = os.path.abspath(os.path.dirname('main.py'))
MODEL_DIR = os.path.join(BASE_DIR, 'model')
RAW_TABLE_DIR = os.path.join(BASE_DIR, 'raw_tables')

# file to string connection
with open(os.path.join(MODEL_DIR, 'tables.json'), 'r') as f:
    data_tables = json.load(f)

d = data_tables['snow_flake_tables']
ordering_insert = []
for dict in d:
    name = [tbl_name for tbl_name in dict.keys()]
    ordering_insert.append(*name)

print(ordering_insert) """

""" 
def slip_insert(dataset: pd.DataFrame, begin: int, step: int):
    '''
        function to iterate for dataset consolidating values to performe an
        insert in batch
        params: datase: a pandas dataframe containing values for insert into
        database
        params: begin: int containing initial step
        params: step: int to limit the max rows os insert
    '''
    lenght = len(dataset)
    count = ceil(lenght / step)
    consolidate_list = []
    list_insert_values = []
    end = step
    for i in range(count):
        if end > lenght:
            end = lenght

        df_values = dataset.iloc[begin:end].iterrows()
        for _, row in df_values:
            list_insert_values.append(tuple(row))

        consolidate_list.append(list_insert_values[:])
        list_insert_values.clear()
        begin = end
        end += step

    return consolidate_list


def divide_insert(lista, inicio, passo):
    # Essa função recebe uma lista contendo os values do seu insert
    # inicio e passo, para dividir em uma sublista para fazer insert
    # por lotes. Exemplo realizar um insert de 1000 em 1000
    # inicio = 0 passo = 1000
    tamanho = len(lista)
    fim = passo
    qtde = ceil(len(lista) / passo)
    lista_consolidada = []
    lista_to_insert = []
    total = 0

    for i in range(qtde):
        if fim > tamanho:
            fim = tamanho

        lista_to_insert = lista[inicio:fim]
        total += len(lista_to_insert)

        lista_consolidada.append(lista_to_insert[:])
        lista_to_insert.clear()

        inicio = fim
        fim += passo
    return lista_consolidada, total

 """
if __name__ == '__main__':
    #path_file = r'D:\Projetos\17 - Programação\Projeto_Nu\Nubank_Analytics_Engineer_Case_4.0\project\raw_tables\accounts\part-00000-tid-2834924781296170616-a9b7a53c-b8f1-417c-876b-22ce8ab4c825-11024507-1-c000.csv'
    #df = pd.read_csv(path_file)
    # print(df.head())
    #l, t = slip_insert(df, 0, 10)
    # print(t)
    # print(l)
    # l = [[('Brasil', 1811589392032273152)]]
    start = datetime.now()
    time.sleep(2)

    print(f'Execution time was {datetime.now() - start}')