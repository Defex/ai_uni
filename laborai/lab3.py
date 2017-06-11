#IFF 4/1 Lukas Vanagas
import os
import glob
import sys
import re

cwd = os.getcwd()
SPAM_PATH = os.path.join(cwd, 'Spamas', '*')
NOT_SPAM_PATH = os.path.join(cwd, 'Ne spamas', '*')
TEST_SPAM_PATH = os.path.join(cwd, 'test spam', '*')

data = {}
count = {}

def format_text(text):
    return re.sub(r'[^a-zA-Z0-9$\'"]', " ", text)

def get_words_from_text(text):
    text = format_text(text)
    return text.split()

def add_word_to_data(data, word, spam_key):
    word = word.lower()
    if word not in data:
        data[word] = {}
    if spam_key in data[word]:
        data[word][spam_key] += 1
    else:
        data[word][spam_key] = 1
    return data

def add_word_count(words, spam_key):
    if spam_key not in count:
        count[spam_key] = 0
    count[spam_key] += len(words)

def add_words_to_data(data, words, spam_key = 'spam'):
    for word in words:
        data = add_word_to_data(data, word, spam_key)
    return data

def read_file(file):
    try:
        with open(file) as f:
            return f.read()
    except UnicodeDecodeError:
        with open(file, encoding='ISO-8859-1') as f:
            return f.read()

def read_files_get_words(files, spam_key):
    for fle in files:
        text = read_file(fle)
        words = get_words_from_text(text)
        add_words_to_data(data, words, spam_key)
        add_word_count(words, spam_key)

def calculate_spam_probabilities(data, count):
    for k, v in data.items():
        if 'not_spam' not in v:
            v['bajes_chance'] = 0.99
        elif 'spam' not in v:
            v['bajes_chance'] = 0.01
        else:
            v['chance_spam'] = v['spam'] / count['spam']
            v['chance_not_spam'] = v['not_spam'] / count['not_spam']
            v['bajes_chance'] = v['chance_spam'] /( v['chance_spam'] + v['chance_not_spam'] )
    return data

def sort_by_bajes_chance(data, reverse = False):
    return sorted(data.keys(), key=lambda k: data[k]['bajes_chance'], reverse=reverse)

def print_highest_bajes_chance(data):
    sortedData = sort_by_bajes_chance(data, True)
    for k in sortedData[0:10]:
        print(k, data[k]['spam'], data[k]['not_spam'], data[k]['bajes_chance'])

def set_bajes_chance(data, test_data, default_value = 0.5):
    for k,v in test_data.items():
        if k in data:
            test_data[k]['bajes_chance'] = data[k]['bajes_chance']
        else:
            test_data[k]['bajes_chance'] = default_value
    return test_data

def get_closest_and_farest_values(data, count = 10):
    values = []
    if len(data) < count:
        for v in data.values():
            values.append(v['bajes_chance'])
    else:
        sorted_data = sort_by_bajes_chance(data, True)
        high = sorted_data[:5]
        low = sorted_data[-5:]
        for k in high:
            values.append(data[k]['bajes_chance'])
        for k in low:
            values.append(data[k]['bajes_chance'])
    return values

def calc_if_is_spam(values):
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

if __name__ == '__main__':
    spam_files = glob.glob(SPAM_PATH)
    not_spam_files = glob.glob(NOT_SPAM_PATH)
    test_spam_files = glob.glob(TEST_SPAM_PATH)
    read_files_get_words(spam_files, 'spam')
    read_files_get_words(not_spam_files, 'not_spam')
    calculate_spam_probabilities(data, count)
    print(count)
    print_highest_bajes_chance(data)
    test_files(test_spam_files)
