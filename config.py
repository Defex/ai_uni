import os
# API helper settings
API_KEY = os.environ['LOL_API_KEY'] 
#crawler settings
SERVERS = [
    'ru',
    # 'kr',
    'br1',
    # 'oc1',
    # 'jp1',
    'na1',
    'eun1',
    'euw1',
    # 'tr1',
    'la1',
    'la2',
]
MATCH_COUNT = 200
PAGE_COUNT = 50
DOWNLOAD_DIRECTORY = 'D:\lol_match_data'
cwd = os.getcwd()
# LEARN_DIRECTORY = os.path.join(cwd, 'data', '*')
# LEARN_DIRECTORY = os.path.join('D:', 'eun1', '*.json')
LEARN_DIRECTORY = os.path.join('D:', 'data' ,'*', '*.json')
