import os
import json
from Bajes import Bajes
from BajesFormatter import BajesFormatter
from MatchFormatter import MatchFormatter
from BajesHelper import BajesHelper
from Reader import Reader
from UrlReader import UrlReader

cwd = os.getcwd()
SINGLE_MATCH = os.path.join(cwd, 'single_match.json')
MATCH_DATA = os.path.join(cwd, 'data', 'matches1.json')
MATCH_DATA_ALL = os.path.join(cwd, 'data', '*')

if __name__ == '__main__':
    # reader = Reader() #reads data from file
    # match_formatter = MatchFormatter() #formats match data
    # url_reader = UrlReader() #get data from api

    # choice = input('press B for bajes algorithm calculation ').lower()
    # if choice == 'b':
    bajes_helper = BajesHelper()
    bajes_helper.execute()