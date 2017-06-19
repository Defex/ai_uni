import glob
import json
import ntpath
import os
from src.Reader import Reader
from src.lol.Formatter import lol_formatter
from src.Helper import *
import config
import threading

def format_fetched_data(input_dir, output_dir):
    create_folder(output_dir)
    files = glob.glob(input_dir)
    chunks = get_chunks(files, int(len(files)/7))
    # format_data_from_files(chunks[0], output_dir)
    threads = [threading.Thread(target=format_data_from_files, args=(fls, output_dir)) for fls in chunks]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def format_data_from_files(files, output_dir):
    for file in files:
        f_match = read_and_format(file)
        save_path = get_save_path(output_dir, file)
        save_json(save_path, f_match)

def get_chunks(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]

def get_save_path(output_dir, path):
    head, name = ntpath.split(path)
    head, server = ntpath.split(head)
    return os.path.join(output_dir, '{}_{}'.format(server,name))

def read_and_format(file):
    matches = read_json(file)
    return lol_formatter.format_matches(matches)

def save_json(file, text):
    with open(file, 'w') as f:
        json.dump(text, f)

def read_json(file):
    with open(file, encoding='utf8', errors='replace') as f:
        return json.load(f)

if __name__ == '__main__':
    format_fetched_data(config.FORMAT_FROM, config.FORMAT_TO)
