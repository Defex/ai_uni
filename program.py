import os
import json

from Reader import Reader, UrlReader
from MatchFormatter import MatchFormatter
from BajesFormatter import BajesFormatter
from Bajes import Bajes

cwd = os.getcwd()
SINGLE_MATCH = os.path.join(cwd, 'data', 'single_match.json')
MATCH_DATA = os.path.join(cwd, 'data', 'matches1.json')
SAMPLE_DATA_URL = 'https://s3-us-west-1.amazonaws.com/riot-developer-portal/seed-data/matches1.json'

if __name__ == '__main__':
    # reader = Reader() #reads data from file
    # match_formatter = MatchFormatter() #formats match data
    # url_reader = UrlReader() #get data from api
    # bajes_formatter = BajesFormatter() #formats data for bajes
    # bajes = Bajes() #calculates by bajes algorithm
    # # reading from file
    # text = reader.read_file(MATCH_DATA)
    # match_formatter = MatchFormatter()
    # file_data = match_formatter.format_matches(text['matches'])
    # # reading from url sample data
    # api_data = url_reader.get_json_from_file(SAMPLE_DATA_URL)
    # # getting summoner match
    # summoner_profile = url_reader.get_profile_by_name('dudodu')
    # print(summoner_profile)
    # account_id = '218065372'
    # ranked_matches = url_reader.get_ranked_match_list_by_account_id(account_id)
    # print(ranked_matches['matches'])
    # for rm in ranked_matches['matches']:
    #     print(rm['gameId'])
    # game_id=1684320341
    # match = url_reader.get_match_by_game_id(game_id)
    # print(match)

    reader = Reader() #reads data from file
    match_formatter = MatchFormatter() #formats match data
    url_reader = UrlReader() #get data from api
    bajes_formatter = BajesFormatter() #formats data for bajes
    bajes = Bajes() #calculates by bajes algorithm
    
    # reading from file
    text = reader.read_file(MATCH_DATA)
    file_data = match_formatter.format_matches(text['matches'])
    bajes_data = bajes_formatter.format_for_bajes(file_data)
    # adding bajes learn data
    for participant in bajes_data:
        bajes.add_words(participant['data'], participant['outcome'])
    bajes.calculate_spam_probabilities()
    #  getting online match data
    game_id=1684320341
    match = url_reader.get_match_by_game_id(game_id)
    formated_match = match_formatter.format_match(match)
    bajes_formated_match = bajes_formatter.format_match(formated_match[0:5])
    test_data = {}
    for participant in bajes_formated_match:
        bajes.add_words_test(participant['data'], 'count', test_data)
    bajes.set_bajes_chance(test_data)
    values = bajes.get_closest_and_farest_values(test_data)
    result = bajes.calc_if_is_spam(values)
    print(result)
    # print(json.dumps(test_data))
    # print(json.dumps(formated_match[5:10]))
    print(json.dumps(bajes_formated_match))
