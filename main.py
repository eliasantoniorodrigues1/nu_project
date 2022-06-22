from datetime import datetime

data = '2019-04-19T01:34:25.000Z'


print(datetime.strptime(data, '%Y-%m-%d %H:%M:%S'))