import glob
import json
from src.lol.Formatter import LolFormatter as MatchFormatter

class Reader():
    def read_file(self, file):
        with open(file, encoding='utf8', errors='replace') as f:
            return json.load(f)

    def read_files(self, files):
        text = []
        for file in files:
            text.append(self.read_file(file))
        return text
            
    def read_directory(self, path):
        files = glob.glob(path)
        return self.read_files(files)
    
    def read_directory_matches(self, path):
        matches = self.read_directory(path)
        return MatchFormatter.format_files_data(matches)
