import json
import pandas as pd


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
