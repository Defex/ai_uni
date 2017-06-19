import os

from src.bajes.Bajes import Bajes
from src.bajes.Formatter import *
from src.bajes.BajesFormatter import BajesFormatter
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
MSG_LEARN_SIMPLE = 'learning bajes from files'
MSG_LEARN_WITH_NOISE = 'learning bajes from files'
MSG_LEARN_COMPLETE = 'learning from files complete'
MSG_TEST_FILE = 'testing data from file'
MSG_TEST_URL = 'testing from url..'
MSG_TEST_COMPLETE = 'testing completed'

class BajesHelper():
    def execute(self):
        print(MSG_WELCOME)
        print(MSG_COMMANDS)
        bajes = Bajes()
        test_matches = []
        val = input('Selecty your option: ').lower()
        while val != 'q':
            if val == 'f':
                print(MSG_TEST_FILE)
                test_matches = self.get_test_matches_from_file()
            elif val == 'a':
                user = input('user: ')
                match_count = int(input('match_count: '))
                print(MSG_TEST_URL)
                test_matches = self.get_test_matches_from_url(user, match_count)
            elif val == 'l':
                print(MSG_LEARN_SIMPLE)
                bajes = self.learn_simple()
                print(MSG_LEARN_COMPLETE)
            elif val == 'n':
                print(MSG_LEARN_WITH_NOISE)
                bajes = self.learn_noisy()
                print(MSG_LEARN_COMPLETE)
            elif val == 's':
                print('testing_simple')
                self.test_simple(bajes, test_matches)
            elif val == 't':
                print('testing with noise')
                self.test_noisy(bajes, test_matches)
            elif val == 'q':
                return
            else:
                print(MSG_UKNOWN)
            print(MSG_COMMANDS)
            val = input('Selecty your option: ').lower()

#   LEARNING
    def learn_simple(self):
        matches = self.read_formated_data(MATCH_DATA_ALL)
        simple_data = self.get_simple_bajes_data(matches)
        bajes = Bajes()
        self.add_simple_words(bajes, simple_data)
        bajes.calculate_spam_probabilities()
        return bajes
    
    def learn_noisy(self):
        matches = self.read_formated_data(MATCH_DATA_ALL)
        # simple_data = self.get_simple_bajes_data(matches)
        noisy_data = self.get_noisy_bajes_data(matches)
        bajes = Bajes()
        # for x in range(0, 5):
        # self.add_simple_words(bajes, simple_data)
        self.add_noisy_words(bajes, noisy_data)
        bajes.calculate_spam_probabilities()
        return bajes

    def read_formated_data(self, path):
        return Reader().read_directory(path)
    
    def get_simple_bajes_data(self, matches):
        return format_matches(matches)
    
    def get_noisy_bajes_data(self, matches):
        return BajesFormatter().format_for_bajes(matches)
    
    def add_simple_words(self, bajes, simple_data):
        for match in simple_data:
            for team in match:
                words = self.get_simple_words(team)
                bajes.add_words(words, team['outcome'])
        return bajes

    def get_simple_words(self, team):
        words = []
        for k, v in team.items():
            if k != 'outcome':
                words.append(v)
        return words
    
    def add_noisy_words(self, bajes, noisy_data):
        for p in noisy_data:
            bajes.add_words(p['data'], p['outcome'])
        return bajes
    
#   TESTING

    def test_simple(self, bajes, test_matches):
        results = self.calc_simple(bajes, test_matches)
        results = self.get_result_data(results, test_matches)
        self.print_results(results)

    def calc_simple(self, bajes, test_matches):
        results = []
        test_matches = self.get_simple_bajes_data(test_matches)
        for match in test_matches:
            for team in match:
                test_data = {}
                words = self.get_simple_words(team)
                bajes.add_words_test(words, 'count', test_data)
                bajes.set_bajes_chance(test_data)
                values = bajes.get_closest_and_farest_values(test_data)
                results.append(bajes.calc_if_is_spam(values))
        return results

    def test_noisy(self, bajes, test_matches):
        results = self.calc_noisy(bajes, test_matches)
        results = self.get_result_data(results, test_matches)
        self.print_results(results)
    
# here
    def calc_noisy(self, bajes, test_matches):
        results = []
        for match in test_matches:
            result1 = self.check_match(bajes, match[:5])
            result2 = self.check_match(bajes, match[5:])
            results.append(result1)
            results.append(result2)
        return results

    def check_match(self, bajes, formatted_match):
        bajes_formatter = BajesFormatter()
        bajes_formated_match = bajes_formatter.format_match(formatted_match)
        test_data = {}
        for participant in bajes_formated_match:
            bajes.add_words_test(participant['data'], 'count', test_data)
        bajes.set_bajes_chance(test_data)
        values = bajes.get_closest_and_farest_values(test_data)
        return bajes.calc_if_is_spam(values)

    def get_test_matches_from_url(self, user, match_count):
        test_matches = LolAPIHelper().get_matches_by_name(user, match_count)
        return MatchFormatter().format_matches(test_matches)
    
    def get_test_matches_from_file(self):
        test_matches = Reader().read_file(MATCH_DATA)
        return MatchFormatter().format_matches(test_matches)
    
#   PRINTING
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

    def is_correct_guess(self, value, is_winner):
        if value > 0.5 and is_winner:
            return False
        elif value > 0.5 and not is_winner:
            return True
        elif value < 0.5 and is_winner:
            return True
        elif value < 0.5 and not is_winner:
            return False

    def print_results(self, results):
        print('{:<20} | {} | {}'.format('Bajes Chance', 'Outcome', 'Is correct?'))
        for r in results[0]:
            print('{:<20} | {:<7} | {}'.format(r[0], 'win' if r[1] == True else 'loss', r[2]))
        total = len(results[1])
        correct = results[1].count(True)
        incorrect = total - correct
        percentage_correct = correct * 100 / total
        print('total guesses - {}, correct - {}, incorrect - {}'.format(total, correct, incorrect))
        print('Correct percentage - {}'.format(percentage_correct))
