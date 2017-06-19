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

FORMAT_FROM = os.path.join('D:', 'lol_match_data' ,'*', '*.json')
FORMAT_TO = os.path.join('D:', 'f_lol_match_data')

DOWNLOAD_DIRECTORY = 'D:\lol_match_data'
LEARN_DIRECTORY = os.path.join('D:', 'f_lol_match_data' , '*.json')
