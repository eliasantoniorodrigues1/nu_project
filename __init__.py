import sys
import os


# append my base dir into a system path to make python see my packages
BASE_DIR = os.path.dirname(os.path.abspath('__init__'))
API_DIR = os.path.join(BASE_DIR, 'api')
MODEL_DIR = os.path.join(BASE_DIR, 'model')

# my dir list
my_dirs = [str(BASE_DIR), str(API_DIR), str(MODEL_DIR)]
# insert into path list
sys.path.append(my_dirs)
