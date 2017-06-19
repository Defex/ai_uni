import os

from src.bajes.Bajes import Bajes
from src.bajes.Formatter import *
from src.lol.Formatter import LolFormatter as MatchFormatter
from src.Reader import Reader
from src.lol.APIHelper import LolAPIHelper
from src.Helper import get_from_json_files, decode_file_text
from format_match_data import *
import config

cwd = os.getcwd()
MATCH_DATA_ALL = config.LEARN_DIRECTORY
MATCH_DATA = os.path.join(cwd, 'data', 'dudodu.json')

MSG_WELCOME = 'Welcome to Bajes algorithm calculation!'
MSG_COMMANDS = 'Commands: L - learn bajes from files, U - learn from url, F - test bajes from file, A - test bajes from api, Q - exit bajes'
MSG_UKNOWN = 'Uknown input option'
MSG_LEARNING = 'learning bajes from files'
MSG_LEARNING_COMPLETE = 'learning from files complete'
MSG_TEST_FILE = 'testing data from file'
MSG_TEST_URL = 'testing from url..'
MSG_TEST_COMPLETE = 'testing completed'

class BajesHelper():
    def execute(self):
        print(MSG_WELCOME)
        print(MSG_COMMANDS)
        bajes = Bajes()
        val = input('Selecty your option: ').lower()
        while val != 'q':
            if val == 'f':
                print(MSG_TEST_FILE)
                self.bajes_test_from_file(bajes)
            elif val == 'a':
                user = input('user: ')
                match_count = int(input('match_count: '))
                print(MSG_TEST_URL)
                self.bajes_test_from_url(bajes, user, match_count)
            elif val == 'l':
                print(MSG_LEARNING)
                bajes = self.bajes_learn_from_files()
                print(MSG_LEARNING_COMPLETE)
            elif val == 'q':
                return
            else:
                print(MSG_UKNOWN)
            print(MSG_COMMANDS)
            val = input('Selecty your option: ').lower()


    def bajes_learn_from_files(self):
        bajes = self.get_formated_data_from_files(MATCH_DATA_ALL)
        bajes.calculate_spam_probabilities()
        return bajes

    def get_formated_data_from_files(self, path):
        reader = Reader()
        formated_data = reader.read_directory(path)
        bajes = Bajes()
        bajes_data = format_matches(formated_data)
        for match in bajes_data:
            for team in match:
                words = self.get_words(team)
                bajes.add_words(words, team['outcome'])
        return bajes

    def bajes_test_from_url(self, bajes, user = 'dudodu', match_count = 10):
        url_reader = LolAPIHelper()
        user_matches = url_reader.get_matches_by_name(user, match_count)
        self.get_results(bajes, user_matches)

    def get_results(self, bajes, user_matches):
        match_formatter = MatchFormatter()
        formatted_matches = match_formatter.format_matches(user_matches)
        results = self.check_matches(bajes, formatted_matches)
        results = self.get_result_data(results, formatted_matches)
        self.print_results(results)
        print(bajes.count)
    
    def check_matches(self, bajes, formatted_matches):
        results = []
        for match in formatted_matches:
            results.extend(self.check_match(bajes, match))
        return results

    def check_match(self, bajes, match):
        results = []
        match = format_match(match)
        for team in match:
            test_data = {}
            words = self.get_words(team)
            bajes.add_words_test(words, team['outcome'], test_data)
            bajes.set_bajes_chance(test_data)
            values = bajes.get_closest_and_farest_values(test_data)
            print(values)
            results.append(sum(values)/len(values))
        return results

    def is_correct_guess(self, value, is_winner):
        if value > 0.5 and is_winner:
            return False
        elif value > 0.5 and not is_winner:
            return True
        elif value < 0.5 and is_winner:
            return True
        elif value < 0.5 and not is_winner:
            return False

    def get_result_data(self, results, formatted_matches):
        data = []
        correct = []
        for x in range(0, len(formatted_matches)):
            score1 = results[x*2] #team1
            score2 = results[x*2+1] #team2
            is_winn1 = formatted_matches[x][0]['is_winner']
            is_winn2 = formatted_matches[x][-1]['is_winner']
            correct1 = self.is_correct_guess(score1, is_winn1)
            correct2 = self.is_correct_guess(score2, is_winn2)
            data.append([score1, is_winn1, correct1])
            data.append([score2, is_winn2, correct2])
            correct.append(correct1)
            correct.append(correct2)
        return [data, correct]

    def get_words(self, team):
        words = []
        for k, v in team.items():
            if k != 'outcome':
                words.append(v)
        return words

    def print_results(self, results):
        print('{:<20} | {} | {}'.format('Bajes Chance', 'Outcome', 'Is correct?'))
        for r in results[0]:
            print('{:<20} | {:<7} | {}'.format(r[0], 'win' if r[1] == True else 'loss', r[2]))
        total = results[1].count(True) + results[1].count(False)
        correct = results[1].count(True)
        incorrect = total - correct
        percentage_correct = correct * 100 / total
        print('total guesses - {}, correct - {}, incorrect - {}'.format(total, correct, incorrect))
        print('Correct percentage - {}'.format(percentage_correct))
    
    def bajes_learn_from_url(self):
        return self.get_data_from_url()

    def bajes_test_from_file(self, bajes):
        reader = Reader()
        match_formatter = MatchFormatter()
        user_matches = reader.read_file(MATCH_DATA)
        self.get_results(bajes, user_matches)
