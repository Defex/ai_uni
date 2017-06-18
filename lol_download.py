from src.lol.Fetcher import LolFetcher
from src.crawler.Crawler import LolCrawler
from src.Helper import json_to_file
import json
import config
from src.lol.APIHelper import LolAPIHelper

if __name__ == '__main__':
    crawler = LolCrawler()
    # a page contains 20 players
    server_names = crawler.run(config.SERVERS, config.PAGE_COUNT)
    fetcher = LolFetcher()
    fetcher.download_matches_from_regions(config.SERVERS, config.MATCH_COUNT, config.MATCH_DIRECTORY)
