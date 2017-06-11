import glob
import json
from time import sleep
import urllib.request

API_KEY = 'RGAPI-8a418372-2657-4265-841d-651768dc130c'

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

class UrlReader():
    def get_json(self, url):
        with urllib.request.urlopen(url) as res:
            data = json.loads(res.read().decode())
            return data
    
    def get_json_from_file(self, url):
        res = urllib.request.urlopen(url)
        data = res.read()
        decoded = data.decode('cp1252').encode('utf-8')
        return json.loads(decoded)
    
    def get_from_json_files(self, to = 11):
        text = []
        for x in range(1, to):
            url = 'https://s3-us-west-1.amazonaws.com/riot-developer-portal/seed-data/matches{}.json'.format(x)
            print(url)
            text.append(url_reader.get_json_from_file(url))
        return text
    
    def get_profile_by_name(self, name, api_key=API_KEY, server='eun1'):
        url = 'https://{}.api.riotgames.com/lol/summoner/v3/summoners/by-name/{}?api_key={}'.format(server, name, api_key)
        return self.get_json(url)
    
    def get_ranked_match_list_by_account_id(self, account_id, api_key=API_KEY, server='eun1'):
        url = 'https://{}.api.riotgames.com/lol/match/v3/matchlists/by-account/{}?api_key={}'.format(server, account_id, api_key)
        return self.get_json(url)
    
    def get_match_by_game_id(self, game, api_key=API_KEY, server='eun1'):
        url = 'https://{}.api.riotgames.com/lol/match/v3/matches/{}?api_key={}'.format(server, game, api_key)
        return self.get_json(url)
    
    def get_matches_by_user(self, user, match_count=10, api_key=API_KEY, server='eun1'):
        summoner_profile = self.get_profile_by_name(user)
        print(summoner_profile)
        account_id = summoner_profile['accountId']
        ranked_matches = self.get_ranked_match_list_by_account_id(account_id)
        games_data = []
        for rm in ranked_matches['matches']:
            if match_count <= 0:
                break
            match = self.get_match_by_game_id(rm['gameId'])
            games_data.append(match)
            sleep(2)
            match_count -= 1
        return games_data