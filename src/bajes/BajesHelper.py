import os

from src.bajes.Bajes import Bajes
from src.bajes.BajesFormatter import BajesFormatter
from src.lol.Formatter import LolFormatter as MatchFormatter
from src.Reader import Reader
from src.lol.APIHelper import LolAPIHelper
from src.Helper import get_from_json_files, decode_file_text

cwd = os.getcwd()
MATCH_DATA_ALL = os.path.join(cwd, 'data', '*')
MATCH_DATA = os.path.join(cwd, 'data', 'matches1.json')

class BajesHelper():
    def get_data_from_files(self, path):
        reader = Reader()
        text = reader.read_directory_matches(path)
        return self.get_formated_bajes(text)
    
    def get_data_from_url(self):
        text = get_from_json_files()
        text = MatchFormatter.format_files_data(text)
        return self.get_formated_bajes(text)
    
    def get_formated_bajes(self, text):
        match_formatter = MatchFormatter()
        bajes_formatter = BajesFormatter()
        bajes = Bajes()
        formated_data = match_formatter.format_matches(text)
        bajes_data = bajes_formatter.format_for_bajes(formated_data)
        for participant in bajes_data:
            bajes.add_words(participant['data'], participant['outcome'])
        return bajes
    
    def check_match(self, bajes, formatted_match):
        bajes_formatter = BajesFormatter()
        bajes_formated_match = bajes_formatter.format_match(formatted_match)
        test_data = {}
        for participant in bajes_formated_match:
            bajes.add_words_test(participant['data'], 'count', test_data)
        bajes.set_bajes_chance(test_data)
        values = bajes.get_closest_and_farest_values(test_data)
        return bajes.calc_if_is_spam(values)
    
    def check_matches(self, bajes, formatted_matches):
        results = []
        for match in formatted_matches:
            result1 = self.check_match(bajes, match[:5])
            result2 = self.check_match(bajes, match[5:])
            results.append(result1)
            results.append(result2)
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

    def bajes_learn_from_files(self):
        bajes = self.get_data_from_files(MATCH_DATA_ALL)
        bajes.calculate_spam_probabilities()
        return bajes
    
    def bajes_learn_from_url(self):
        return self.get_data_from_url()

    def bajes_test_from_file(self, bajes):
        reader = Reader()
        match_formatter = MatchFormatter()
        user_matches = reader.read_file(MATCH_DATA)['matches']
        self.get_results(bajes, user_matches)
    
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

    def execute(self):
        print('Welcome to Bajes algorithm calculation!')
        print('Commands: L - learn bajes from files, U - learn from url, F - test bajes from file, A - test bajes from api, Q - exit bajes')
        bajes = Bajes()
        val = input('Selecty your option: ').lower()
        while val != 'q':
            if val == 'f':
                self.bajes_test_from_file(bajes)
                print('testing data from file')
            elif val == 'a':
                user = input('user: ')
                match_count = int(input('match_count: '))
                print('testing from url..')
                self.bajes_test_from_url(bajes, user, match_count)
            elif val == 'l':
                print('learning bajes from files')
                bajes = self.bajes_learn_from_files()
                print('learning from files complete')
            elif val == 'u':
                print('learning bajes from url')
                bajes = self.bajes_learn_from_url()
            elif val == 'q':
                return
            else:
                print('Uknown input option')
            print('Commands: L - learn bajes, F - test bajes from file, A - test bajes from api, Q - exit bajes')
            val = input('Selecty your option: ').lower()
