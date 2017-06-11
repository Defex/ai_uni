class Bajes():
    def __init__(self):
        self.data = {}
        self.count = {}

    def add_words(self, words, spam_key):
        for word in words:
            self.add_word(word, spam_key)

    def add_word(self, word, spam_key, data):
        word = word.lower()
        if word not in data:
            data[word] = {}
        if spam_key in data[word]:
            data[word][spam_key] += 1
        else:
            data[word][spam_key] = 1
    
    def add_words(self, words, spam_key):
        for word in words:
            self.add_word(word, spam_key, self.data)
            self.increase_count(spam_key)

    def add_words_test(self, words, spam_key, test_data):
        for word in words:
            self.add_word(word, spam_key, test_data)

    def increase_count(self, spam_key):
        if spam_key not in self.count:
            self.count[spam_key] = 0
        self.count[spam_key] += 1
    
    def calculate_spam_probabilities(self):
        for k, v in self.data.items():
            if 'not_spam' not in v:
                v['bajes_chance'] = 0.99
            elif 'spam' not in v:
                v['bajes_chance'] = 0.01
            else:
                v['chance_spam'] = v['spam'] / count['spam']
                v['chance_not_spam'] = v['not_spam'] / count['not_spam']
                v['bajes_chance'] = v['chance_spam'] /( v['chance_spam'] + v['chance_not_spam'] )

    def sort_by_bajes_chance(self, data, reverse = False):
        return sorted(data.keys(), key=lambda k: data[k]['bajes_chance'], reverse=reverse)

    def print_highest_bajes_chance(self, data):
        sortedData = sort_by_bajes_chance(data, True)
        for k in sortedData[0:10]:
            print(k, data[k]['spam'], data[k]['not_spam'], data[k]['bajes_chance'])

    def set_bajes_chance(self, test_data, default_value = 0.5):
        for k,v in test_data.items():
            if k in self.data:
                print(k, v)
                test_data[k]['bajes_chance'] = self.data[k]['bajes_chance']
            else:
                test_data[k]['bajes_chance'] = default_value
        return test_data

    def get_closest_and_farest_values(self, data, count = 10):
        values = []
        if len(data) < count:
            for v in data.values():
                values.append(v['bajes_chance'])
        else:
            sorted_data = self.sort_by_bajes_chance(data, True)
            high = sorted_data[:5]
            low = sorted_data[-5:]
            for k in high:
                values.append(data[k]['bajes_chance'])
            for k in low:
                values.append(data[k]['bajes_chance'])
        return values

    def calc_if_is_spam(self, values):
        mult = 1
        for v in values:
            mult *= v
        added = [1 - x for x in values]
        mult_added = 1
        for v in added:
            mult_added *= v
        result = mult / ( mult + mult_added )
        return result

    def test_files(files):
        for fle in files:
            test_data = {}
            text = read_file(fle)
            words = get_words_from_text(text)
            test_data = add_words_to_data(test_data, words, 'count')
            test_data = set_bajes_chance(data, test_data)
            values = get_closest_and_farest_values(test_data)
            result = calc_if_is_spam(values)
            print('{} {} {}'.format(fle, result, 'SPAM' if result > 0.5 else 'NOT SPAM'))