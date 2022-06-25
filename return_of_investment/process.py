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

    # day
    df_filtered['day'] = df_filtered['investment_completed_at_timestamp'].apply(dateutil.parser.parse).apply(
        get_day)

    # month
    df_filtered['month'] = df_filtered['investment_completed_at_timestamp'].apply(dateutil.parser.parse).apply(
        get_month)

    # generate positive df
    positive_df = filter_df(dataframe=df_filtered, column_to_filter='type', list_values=[
                            'investment_transfer_in'])
    # generate negative df
    negative_df = filter_df(dataframe=df_filtered, column_to_filter='type', list_values=[
                            'investment_transfer_out'])

    # create new dataset joing data from positive an negative movimentations
    result = pd.merge(positive_df.iloc[:, [1, 3, 8, 9]], negative_df.iloc[:, [1, 3, 8, 9]], how='left', on=[
        'account_id', 'day', 'month'])

    # reordering columns
    result = result.loc[:, ['day', 'month',
                            'account_id', 'amount_x', 'amount_y']]

    columns = {'day': 'Day', 'month': 'Month', 'account_id': 'Account ID',
               'amount_x': 'Deposit', 'amount_y': 'Withdrawal'}

    # rename columns
    result.rename(columns=columns, inplace=True)
    # ordering data
    result = result.sort_values(
        by=['Month', 'Day', 'Account ID'])

    result['Withdrawal'] = result['Withdrawal'].fillna(0)
    result['End of Day Income'] = 0
    result['Account Daily Balance'] = 0

    list_df = result.values.tolist()
    calculation_result = []
    for i in range(len(list_df)):
        calculation_result.append(calculate_movements(list_df, i))

    # get last column from processed list
    result_df = pd.DataFrame(calculation_result[-1], columns=['Day', 'Month', 'Account ID',
                                                              'Deposit', 'Withdrawal', 'End of Day Income', 'Account Daily Balance'])

    dir_file = os.path.join(BASE_DIR, 'return_of_investment')
    result_df.to_csv(os.path.join(
        dir_file, 'Investiment_Income.csv'), index=False)
    print('Investiment calculate with success.')
