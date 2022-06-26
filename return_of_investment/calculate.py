def calculate_movements(list, i):
    '''
        this function receives a list to performe
        a slice, and then calculate the moviments account
        movements = previous day balance + deposit - withdrawal
        end of day income = movements * income rate
        account daily balance = moviments + end of day income

    '''
    if i == 0:
        previous_d = 0
        deposit = list[i][3]
        withdrawal = list[i][4]
        movement = previous_d + deposit - withdrawal
        end_of_day_income = movement * 0.0001 if movement >= 0 else 0
        account_balance = movement + end_of_day_income

        list[i][5] = end_of_day_income if end_of_day_income >= 0 else 0
        list[i][6] = account_balance

        return list
    else:
        previous_d = list[i - 1][6]
        deposit = list[i][3]
        withdrawal = list[i][4]
        movement = previous_d + deposit - withdrawal
        end_of_day_income = movement * 0.0001 if movement >= 0 else 0
        account_balance = movement + end_of_day_income

        list[i][5] = end_of_day_income if end_of_day_income >= 0 else 0
        list[i][6] = account_balance

    return list
