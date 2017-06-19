import config
import json
from src.Reader import Reader
from src.lol.Formatter import LolFormatter
from src.bajes.Formatter import *

if __name__ == '__main__':
    reader = Reader()
    formatter = LolFormatter()
    matches = reader.read_directory(config.LEARN_DIRECTORY)
    matches = formatter.format_matches(matches)
    # print(json.dumps(matches))
    formated = format_matches(matches)
    # print(formated)