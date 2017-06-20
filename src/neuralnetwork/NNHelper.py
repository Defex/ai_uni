import os
import numpy as np

# from MatchFormatter import MatchFormatter
from src.Reader import Reader
# from UrlReader import UrlReader
from src.neuralnetwork.NeuralNetwork import NeuralNetwork
from src.neuralnetwork.NeuralNetwork50 import NeuralNetwork50

cwd = os.getcwd()
MATCH_DATA_ALL = os.path.join(cwd, 'formated', '*')
MATCH_DATA = os.path.join(cwd, 'formated', 'data_dudodu.json')
MATCH_DATA_TEST = os.path.join(cwd, 'test', 'data_Xayira.json')

def extractTime(json):
    return json['id']

def getChamps():
    url_reader = UrlReader() #get data from api
    text = url_reader.get_champion_data()
    champs = {}
    champs50 = {}
    text = text['champions']
    text.sort(key=extractTime)
    i = 0
    for ch in text:
        if 'id' in ch:
            champs[ch['id']] = i
            i += 1
    return champs

class NNHelper():
    def __init__(self):
        self.nn = NeuralNetwork()
        self.nn50 = NeuralNetwork50()
        self.champs = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10, 12: 11, 13: 12, 14: 13, 15: 14, 16: 15, 17: 16, 18: 17, 19: 18, 20: 19, 21: 20, 22: 21, 23: 22, 24: 23, 25: 24, 26: 25, 27: 26, 28: 27, 29: 28, 30: 29, 31: 30, 32: 31, 33: 32, 34: 33, 35: 34, 36: 35, 37: 36, 38: 37, 39: 38, 40: 39, 41: 40, 42: 41, 43: 42, 44: 43, 45: 44, 48: 45, 50: 46, 51: 47, 53: 48, 54: 49, 55: 50, 56: 51, 57: 52, 58: 53, 59: 54, 60: 55, 61: 56, 62: 57, 63: 58, 64: 59, 67: 60, 68: 61, 69: 62, 72: 63, 74: 64, 75: 65, 76: 66, 77: 67, 78: 68, 79: 69, 80: 70, 81: 71, 82: 72, 83: 73, 84: 74, 85: 75, 86: 76, 89: 77, 90: 78, 91: 79, 92: 80, 96: 81, 98: 82, 99: 83, 101: 84, 102: 85, 103: 86, 104: 87, 105: 88, 106: 89, 107: 90, 110: 91, 111: 92, 112: 93, 113: 94, 114: 95, 115: 96, 117: 97, 119: 98, 120: 99, 121: 100, 122: 101, 126: 102, 127: 103, 131: 104, 133: 105, 134: 106, 136: 107, 143: 108, 150: 109, 154: 110, 157: 111, 161: 112, 163: 113, 164: 114, 201: 115, 202: 116, 203: 117, 222: 118, 223: 119, 236: 120, 238: 121, 240: 122, 245: 123, 254: 124, 266: 125, 267: 126, 268: 127, 412: 128, 420: 129, 421: 130, 427: 131, 429: 132, 432: 133, 497: 134, 498: 135}
        self.champs50 = {3 : 0, 8 : 1, 11 : 2, 19 : 3, 21 : 4, 22 : 5, 24 : 6, 25 : 7, 29 : 8, 38 : 9, 40 : 10, 43 : 11, 51 : 12, 53 : 13, 58 : 14, 59 : 15, 60 : 16, 61 : 17, 63 : 18, 64 : 19, 67 : 20, 79 : 21, 80 : 22, 81 : 23, 89 : 24, 92 : 25, 99 : 26, 103 : 27, 104 : 28, 105 : 29, 110 : 30, 114 : 31, 117 : 32, 119 : 33, 121 : 34, 122 : 35, 134 : 36, 154 : 37, 157 : 38, 201 : 39, 202 : 40, 222 : 41, 236 : 42, 238 : 43, 245 : 44, 267 : 45, 412 : 46, 432 : 47, 497 : 48, 498 : 49}

    def only_train_network(self):
        self.nn.train_times(100)
        self.nn50.train_times(100)

    def train_network(self, text):
        # mf = MatchFormatter()
        for m in text:
            # m = mf.format_match(match)
            self.nn.load_one_match(self.format_match_for_training(m))
            self.nn50.load_one_match(self.format_match_for_training50(m))
        self.nn.train_times(1)
        self.nn50.train_times(1)

    def train_netrwork50(self, text):
        for m in text:
            self.nn50.load_one_match(self.format_match_for_training50(m))
        self.nn50.train_times(1)

    def only_train_netrwork50(self, text):
        self.nn50.train_times(1)

    def network_teach_from_files(self):
        reader = Reader()
        print(MATCH_DATA_ALL)
        text = reader.read_directory(MATCH_DATA_ALL)
        self.train_network(text)

    def network_teach_from_file(self):
        reader = Reader()
        text = reader.read_file(MATCH_DATA)
        self.train_network(text)

    def format_match_for_training(self, match):
        training_data = np.zeros(136*2 + 1)
        training_data[136*2] = match[0]['is_winner']
        i = 0
        for participant in match:
            id = self.champs[participant['championId']]
            if i < 5:
                training_data[id] = 1
            else:
                training_data[136+id] = 1
            i += 1
        return training_data

    def format_match_for_training50(self, match):
        training_data = np.zeros(50*2 + 1)
        training_data[50*2] = match[0]['is_winner']
        i = 0
        for participant in match:
            id = self.champs50.get(participant['championId'])
            if id is not None:
                if i < 5:
                    training_data[id] = 1
                else:
                    training_data[50+id] = 1
            i += 1
        return training_data

    # def network_test_from_url(self, bajes, user = 'dudodu', match_count = 10):
    #     url_reader = UrlReader()
    #     user_matches = url_reader.get_matches_by_user(user, match_count)
    #     self.test_network(user_matches)

    def network_test_from_file(self):
        reader = Reader()
        text = reader.read_file(MATCH_DATA_TEST)
        self.test_network(text)

    def test_network(self, text):
        # mf = MatchFormatter()
        for m in text:
            # m = mf.format_match(match)
            self.nn.load_test_match(self.format_match_for_training(m))
            self.nn50.load_test_match(self.format_match_for_training50(m))
        self.nn.test()
        self.nn50.test()

    def test_network50(self, text):
        for m in text:
            # m = mf.format_match(match)
            self.nn50.load_test_match(self.format_match_for_training50(m))
        self.nn50.test()

    def clear_test_network50(self, text):
        self.nn50.clear_test_match()

    def execute(self):
        print('Welcome to Neural Network algorithm calculation!')
        # print('Commands: L - teach network from files, F - test network from file, A - test network from api, Q - exit program')
        print('Commands: L - load and teach network from files, K - load and teach network from single file, T - teach network 100 times, F - test network from file, Q - exit program')
        val = input('Selecty your option: ').lower()
        while val != 'q':
            if val == 'f':
                self.network_test_from_file()
                print('testing data from file')
            # elif val == 'a':
            #     user = input('user: ')
            #     match_count = int(input('match_count: '))
            #     print('testing from url..')
            #     self.network_test_from_url(user, match_count)
            elif val == 'l':
                print('teaching network from files')
                self.network_teach_from_files()
            elif val == 'k':
                print('teaching network from file')
                self.network_teach_from_file()
            # elif val == 'u':
            #     print('teaching network from url')
            #     self.network_teach_from_url()
            elif val == 't':
                print('teaching network')
                self.only_train_network()
            elif val == 'q':
                return
            else:
                print('Uknown input option')
            print('Commands: L - load and teach network from files, K - load and teach network from single file, T - teach network, F - test network from file, Q - exit program')
            val = input('Selecty your option: ').lower()