import json
import os
import log


logger = log.get_logger('migration_plan')

BASE_DIR = os.path.abspath(os.path.dirname('main.py'))
MODEL_DIR = os.path.join(BASE_DIR, 'model')
QUERY_DIR = os.path.join(MODEL_DIR, 'query')
SETTINGS_DIR = os.path.join(BASE_DIR, 'settings')
RAW_TABLES_DIR = os.path.join(BASE_DIR, 'raw_tables')

# credentials
with open(os.path.join(SETTINGS_DIR, 'credentials_snow.json'), 'r') as f:
    credentials_snow = json.load(f)

with open(os.path.join(SETTINGS_DIR, 'credentials_star.json'), 'r') as f:
    credentials_star = json.load(f)

# table conf
with open(os.path.join(SETTINGS_DIR, 'tables.json'), 'r') as f:
    data_tables = json.load(f)

d = data_tables['snow_flake_tables']
for v in d:
    print(v)