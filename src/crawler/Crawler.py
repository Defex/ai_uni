from bs4 import BeautifulSoup
import urllib
import threading

CRAW_URL = 'http://www.lolskill.net/top/highest-lolskillscore/page-{}?filterChampion=&filterRealm={}'

HEADERS = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11' }

server_keys = {
    'euw1':'EUW',
    'eun1': 'EUNE',
    'na1': 'NA',
    'ru': 'RU',
    'tr1': 'TR',
    'br1': 'br',
    'oc1': 'OCE',
    'jp1': 'JP',
    'kr': 'KR',
    'la1': 'LAN',
    'la2': 'LAS',
}

SERVER_FETCH = 'Getting {} server names'
SERVER_FETCH_DONE = 'Finished getting {} server names'

class LolCrawler():
    def __init__(self):
        self.names = {}

    def run(self, servers, page_count = 1):
        threads = [threading.Thread(target= self.get_server_names, args=(server, page_count)) for server in servers]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return self.names
    
    def get_server_names(self, server, page_count):
        print(SERVER_FETCH.format(server))
        self.names[server] = []
        for x in range(1, page_count+1):
            page = self.get_page(server, x)
            self.names[server].extend(self.get_page_names(page))
        print(SERVER_FETCH_DONE.format(server))

    def get_page_names(self, page):
        names = []
        soup = BeautifulSoup(page, 'html.parser')
        for i in soup.select('.summoner.left a'):
            names.append(i.text)
        return names

    def get_page(self, server, page_count):
        url = CRAW_URL.format(page_count, server_keys[server])
        return self.get_text_from_url(url)
    

    def get_text_from_url(self, url):
        request=urllib.request.Request(url, None, HEADERS)
        response = urllib.request.urlopen(request)
        return response.read()
