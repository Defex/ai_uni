import glob
import json

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

    def format_file_data(self, file_data):
        return file_data['matches']

    def format_files_data(self, files):
        files_data = []
        for f in files:
            files_data.extend(self.format_file_data(f))
        return files_data
    
    def read_directory_matches(self, path):
        matches = self.read_directory(path)
        return self.format_files_data(matches)