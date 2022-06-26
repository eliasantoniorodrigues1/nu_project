from numpy import append
from .calculate import calculate_movements
import json
from datetime import datetime
import dateutil.parser
import pandas as pd
import os
import warnings
warnings.simplefilter(action='ignore')
# from api.read_api import get_json_investments


BASE_DIR = os.path.abspath(os.path.dirname('main.py'))
MODEL_DIR = os.path.join(BASE_DIR, 'model')
QUERY_DIR = os.path.join(MODEL_DIR, 'query')
SETTINGS_DIR = os.path.join(BASE_DIR, 'settings')
RAW_TABLES_DIR = os.path.join(BASE_DIR, 'raw_tables')


def get_json_investments(list_paths: list) -> pd.DataFrame:
    '''
        this function receives data from a json file
        and then return a data frame with the rows
        to insert into the table investments
        params: full_path_file: path to json file
    '''
    for file in list_paths:
        file = str(file)
        with open(file, 'r') as f:
            list_data = json.load(f)

        # create header for dataframe
        columns = [column for column in list_data[0]['transactions'][0].keys()]
        columns.insert(1, 'account_id')
        consolidate = []
        for data in list_data:
            investments_accounts = []
            for value in data.values():
                new_list = []
                if isinstance(value, str):
                    account_id = value
                if isinstance(value, list):
                    for element in value:
                        new_list = [v for v in element.values()]
                        new_list.insert(1, account_id)
                        # consolidate transaction with account_id
                        investments_accounts.append(new_list)
            try:
                df = pd.DataFrame(investments_accounts, columns=columns)
                # clean columns before return
                df['account_id'] = [int(id) for id in df['account_id']]
                df['transaction_id'] = [int(id) for id in df['transaction_id']]
                df['amount'] = [float(id) for id in df['amount']]
                df['investment_completed_at'] = df['investment_completed_at'].replace(
                    'None', 0)
                df['investment_completed_at_timestamp'] = df['investment_completed_at_timestamp'].fillna(
                    '1900-01-1 00:00:00.000')
                consolidate.append(df)
                investments_accounts.clear()
            except Exception as e:
                print(f'Error --> {e}')

    return pd.concat(consolidate)


def get_day(date: datetime):
    return date.day


def get_month(date: datetime):
    return date.month


def filter_df(dataframe: pd.DataFrame, column_to_filter: str, list_values: list) -> pd.DataFrame:
    return dataframe.loc[dataframe[column_to_filter].isin(list_values)]


def calculation_process():
    print('Please wait, processing calculation...')

    # load base file with accounts
    df_accounts = pd.read_csv(os.path.join(
        RAW_TABLES_DIR, 'investment_accounts_to_send.csv'))

    # accounts to be filtered
    accounts = []
    for account in df_accounts.values.tolist():
        for ac in account:
            accounts.append(ac)

    # read json file with investments
    df = get_json_investments(
        [os.path.join(RAW_TABLES_DIR, 'investments\\investments_json.json')])

    # filter df by account_id
    df_filtered = filter_df(
        dataframe=df, column_to_filter='account_id', list_values=accounts)

    # filter transaction completed
    df_filtered = filter_df(
        dataframe=df_filtered, column_to_filter='status', list_values=['completed'])

    # day
    df_filtered['day'] = df_filtered['investment_completed_at_timestamp'].apply(dateutil.parser.parse).apply(
        get_day)

    # month
    df_filtered['month'] = df_filtered['investment_completed_at_timestamp'].apply(dateutil.parser.parse).apply(
        get_month)

    # generate positive df
    positive_df = filter_df(dataframe=df_filtered, column_to_filter='type', list_values=[
                            'investment_transfer_in'])

    positive_df = positive_df.loc[:, [
        'investment_completed_at_timestamp', 'day', 'month', 'account_id', 'amount']]
    positive_df['Withdrawal'] = 0

    columns_p = {'day': 'Day', 'month': 'Month', 'account_id': 'Account ID',
                 'amount': 'Deposit'}
    positive_df.rename(columns=columns_p, inplace=True)

    # generate negative df
    negative_df = filter_df(dataframe=df_filtered, column_to_filter='type', list_values=[
                            'investment_transfer_out'])

    negative_df = negative_df.loc[:, [
        'investment_completed_at_timestamp', 'day', 'month', 'account_id', 'amount']]
    negative_df.insert(3, 'Deposit', 0)

    columns_n = {'day': 'Day', 'month': 'Month', 'account_id': 'Account ID',
                 'amount': 'Withdrawal'}
    negative_df.rename(columns=columns_n, inplace=True)

    # concatenate dfs
    result = pd.concat([positive_df, negative_df])
    result = result.sort_values(
        by=['Account ID', 'investment_completed_at_timestamp'])

    result = result.drop(columns=['investment_completed_at_timestamp'])

    # create new columns
    result['End of Day Income'] = 0
    result['Account Daily Balance'] = 0

    # sort account list
    accounts = sorted(accounts)
    calculation_result = []
    for account in accounts:
        # filter df for actual account_id
        df = filter_df(dataframe=result,
                       column_to_filter='Account ID', list_values=[account])

        # transform to list to calculate balance by row
        list_df = df.values.tolist()
        p_result = []
        for i in range(len(list_df)):
            p_result.append(calculate_movements(list_df, i))

            # if len(p_result) == i:
            # adding just the last calculation in the result list
        calculation_result.append(p_result[-1])

    # concat dfs
    # columns for final result
    final_df_columns = result.columns.tolist()
    r = []
    for row_data in calculation_result:
        r.append(pd.DataFrame(row_data, columns=final_df_columns))

    result_df = pd.concat(r)
    print(result_df.head(10))
    dir_file = os.path.join(BASE_DIR, 'return_of_investment')
    result_df.to_csv(os.path.join(
        dir_file, 'Investiment_Income.csv'), index=False)
    print('Investiment calculate with success.')
