from Reader import Reader, UrlReader
from Bajes import Bajes
from BajesFormatter import BajesFormatter
from MatchFormatter import MatchFormatter

class BajesHelper():
    def get_data_from_files(self, path):
        reader = Reader()
        text = reader.read_directory(path)
        return self.get_formated_bajes(text)
    
    def get_data_from_url(self):
        url_reader = UrlReader()
        text = url_reader.get_from_json_files()
        return self.get_formated_bajes(text)
    
    def get_formated_bajes(self, text):
        match_formatter = MatchFormatter()
        bajes_formatter = BajesFormatter()
        bajes = Bajes()
        files_data = []
        for f in text:
            files_data.extend(f['matches'])
        formated_data = match_formatter.format_matches(files_data)
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
    
    def print_results(self, results, formatted_matches):
        for x in range(0, len(formatted_matches)):
            print('{} - {}'.format(results[x*2], formatted_matches[x][0]['is_winner']))
            print('{} - {}'.format(results[x*2+1], formatted_matches[x][-1]['is_winner']))