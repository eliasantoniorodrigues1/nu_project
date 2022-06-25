def calculate_movements(list, i):
    if i == 0:
        previous_d = 0
        deposit = list[i][3]
        withdrawal = list[i][4]
        movement = previous_d + deposit - withdrawal
        end_of_day_income = movement * 0.0001 if previous_d > 0 else 0
        account_balance = movement + end_of_day_income

        list[i][5] = end_of_day_income
        list[i][6] = account_balance

        return list
    else:
        previous_d = list[i - 1][6]
        deposit = list[i][3]
        withdrawal = list[i][4]
        movement = previous_d + deposit - withdrawal
        end_of_day_income = movement * 0.0001 if previous_d > 0 else 0
        account_balance = movement + end_of_day_income

        list[i][5] = end_of_day_income
        list[i][6] = account_balance

        return list

