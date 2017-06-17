import json
import os
import urllib.request
from time import sleep

def decode_file_text(text):
    return text.decode('cp1252').encode('utf-8')

def get_from_json_files(to = 2):
    text = []
    for x in range(1, to):
        url = 'https://s3-us-west-1.amazonaws.com/riot-developer-portal/seed-data/matches{}.json'.format(x)
        print(url)
        formated = decode_file_text(get_text_from_url(url))
        formated = json.loads(formated)
        text.append(formated)
    return text

def get_text_from_url(url):
    while True:
        try:
            with urllib.request.urlopen(url) as res:
                return res.read()
        except urllib.error.HTTPError as err:
            print(err.code)
            if err.code == 404:
                raise err
            sleep(5)

def get_json(url, delay = 0):
    sleep(delay)
    return json.loads(get_text_from_url(url))

def create_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def json_to_file(file, data):
    with open(file, 'w') as f:
        json.dump(data, f)
