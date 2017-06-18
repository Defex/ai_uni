import urllib
import json
from config import API_KEY
from time import sleep

URL_PROFILE = 'https://{}.api.riotgames.com/lol/summoner/v3/summoners/by-name/{}?api_key={}'
URL_MATCHLIST = 'https://{}.api.riotgames.com/lol/match/v3/matchlists/by-account/{}?api_key={}'
URL_MATCH = 'https://{}.api.riotgames.com/lol/match/v3/matches/{}?api_key={}'

class LolAPIHelper():
    def __init__(self, server='eun1', api_key=API_KEY, debug = False):
        self.server = server
        self.api_key = api_key

    def get_matches_by_name(self, name, match_count = 1):
        summoner = self.get_summoner_by_name(name)
        if summoner is None:
            return
        matchlist = self.get_matchlist(summoner['accountId'])['matches']
        match_count = min(match_count, len(matchlist))
        return self.get_matches_from_matchlist(matchlist[:match_count])

    def get_summoner_by_name(self, name):
            url = URL_PROFILE.format(self.server, urllib.parse.quote_plus(name), self.api_key)
            return self.get_from_api(url)

    def get_matchlist(self, account_id):
        url = URL_MATCHLIST.format(self.server, account_id, self.api_key)
        return self.get_from_api(url)

    def get_matches_from_matchlist(self, matches):
        match_data = []
        for match in matches:
            match_data.append(self.get_match_by_id(match['gameId']))
        return match_data

    def get_match_by_id(self, game):
        url = URL_MATCH.format(self.server, game, self.api_key)
        return self.get_from_api(url)

    def get_from_api(self, url):
        while True:
            try:
                with urllib.request.urlopen(url) as res:
                    return json.loads(res.read())
            except urllib.error.HTTPError as err:
                if err.code == 429:
                    sleep(int(err.getheader('Retry-After')) + 1)
                if err.code == 404:
                    return
            except urllib.error.URLError as err:
                print('url error: {}'.format(url))
                return
