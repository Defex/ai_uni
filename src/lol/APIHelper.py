from src.Helper import get_json
import urllib.request
import urllib

URL_PROFILE = 'https://{}.api.riotgames.com/lol/summoner/v3/summoners/by-name/{}?api_key={}'
URL_MATCHLIST = 'https://{}.api.riotgames.com/lol/match/v3/matchlists/by-account/{}?api_key={}'
URL_MATCH = 'https://{}.api.riotgames.com/lol/match/v3/matches/{}?api_key={}'
API_KEY = 'RGAPI-8a418372-2657-4265-841d-651768dc130c'

class LolAPIHelper():
    def __init__(self, server='eun1', api_key=API_KEY, debug = False):
        self.server = server
        self.api_key = api_key

    def get_summoner_by_name(self, name):
            url = URL_PROFILE.format(self.server, urllib.parse.quote_plus(name), self.api_key)
            return get_json(url, 1)

    def get_matchlist(self, account_id):
        url = URL_MATCHLIST.format(self.server, account_id, self.api_key)
        return get_json(url)

    def get_match_by_id(self, game):
        url = URL_MATCH.format(self.server, game, self.api_key)
        return get_json(url, 1)
    
    def get_matches_from_matchlist(self, matches):
        match_data = []
        for match in matches:
            match_data.append(self.get_match_by_id(match['gameId']))
        return match_data

    def get_matches_by_name(self, name, match_count = 1):
        print( match_count)
        summoner = self.get_summoner_by_name(name)
        matchlist = self.get_matchlist(summoner['accountId'])['matches']
        match_count = min(match_count, len(matchlist))
        return self.get_matches_from_matchlist(matchlist[:match_count])
    
    # def is_name_good(self, name):
    #     url = URL_PROFILE.format(self.server, urllib.parse.quote_plus(name), self.api_key)
    #     try:
    #         with urllib.request.urlopen(url) as res:
    #             return True
    #     except urllib.error.HTTPError as err:
    #         print(err)
    #         return False
