from src.lol.Fetcher import LolFetcher
from src.crawler.Crawler import LolCrawler
from src.Helper import json_to_file
import json
import config

servers = {
    'ru',
    # 'kr',
    'br1',
    # 'oc1',
    # 'jp1',
    'na1',
    'eun1',
    'euw1',
    # 'tr1',
    'la1',
    'la2',
}

if __name__ == '__main__':
    crawler = LolCrawler()
    # a page contains 20 players
    server_names = crawler.run(servers, 50)
    fetcher = LolFetcher()
    fetcher.download_matches_from_regions(server_names, 200, config.MATCH_DIRECTORY)
