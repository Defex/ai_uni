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
SAMPLE_DATA_URL = 'https://s3-us-west-1.amazonaws.com/riot-developer-portal/seed-data/matches1.json'

if __name__ == '__main__':
    reader = Reader() #reads data from file
    match_formatter = MatchFormatter() #formats match data
    url_reader = UrlReader() #get data from api
    bajes_formatter = BajesFormatter() #formats data for bajes
    bajes = Bajes() #calculates by bajes algorithm
    
    # # reading from file
    # text = reader.read_file(MATCH_DATA)
    # file_data = match_formatter.format_matches(text['matches'])
    # bajes_data = bajes_formatter.format_for_bajes(file_data)
    # # adding bajes learn data
    # for participant in bajes_data:
    #     bajes.add_words(participant['data'], participant['outcome'])
    # bajes.calculate_spam_probabilities()
    # #  getting online match data
    # game_id=1684320341
    # match = url_reader.get_match_by_game_id(game_id)
    # formated_match = match_formatter.format_match(match)
    # bajes_formated_match = bajes_formatter.format_match(formated_match[5:10])
    # test_data = {}
    # for participant in bajes_formated_match:
    #     bajes.add_words_test(participant['data'], 'count', test_data)
    # bajes.set_bajes_chance(test_data)
    # values = bajes.get_closest_and_farest_values(test_data)
    # result = bajes.calc_if_is_spam(values)
    # # print(json.dumps(bajes.data))
    # # print(json.dumps(test_data))
    # print(json.dumps(formated_match[5:10]))
    # # print(json.dumps(bajes_formated_match))
    # # print(bajes.count)
    # # print(json.dumps(file_data))
    # print(result)

    bajes_helper = BajesHelper()
    url_reader = UrlReader()
    bajes = bajes_helper.get_data_from_files(MATCH_DATA_ALL)
    bajes.calculate_spam_probabilities()
    # bajes = bajes_helper.get_data_from_url()
    # user_matches = url_reader.get_matches_by_user('dudodu', 10)
    user_matches = reader.read_file(MATCH_DATA)['matches']
    formatted_matches = match_formatter.format_matches(user_matches)
    results = bajes_helper.check_matches(bajes, formatted_matches)
    bajes_helper.print_results(results, formatted_matches)
    