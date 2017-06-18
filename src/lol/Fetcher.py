import os
import threading
from src.lol.APIHelper import LolAPIHelper
from src.Helper import create_folder, json_to_file

PLAYER_FETCH = 'getting player "{}" matches'
PLAYER_SAVE = 'saving player "{}" matches'
PLAYER_ERROR = 'Could not download user {} data'
REGION_DONE = 'region {} done!'
REGIONS_DONE = 'All downloads completed!'

class LolFetcher():
    def download_player_matches(self, lol_helper, directory, user, match_count):
        print(PLAYER_FETCH.format(user))
        match_data = lol_helper.get_matches_by_name(user, match_count)
        if match_data:
            print(PLAYER_SAVE.format(user))
            json_to_file(os.path.join(directory, '{}.json'.format(user)), match_data)
        else:
            print(PLAYER_ERROR.format(user))

    def download_region_matches(self, region, users, match_count, directory):
        region_dir = os.path.join(directory, region)
        create_folder(region_dir)
        lol_helper = LolAPIHelper(region)
        for user in users:
            self.download_player_matches(lol_helper, region_dir, user, match_count)
        print(REGION_DONE.format(region))

    def download_matches_from_regions(self, regions, match_count, directory):
        create_folder(os.path.join(directory))
        threads = [threading.Thread(target= self.download_region_matches, args=(region, users, match_count, directory)) for region, users in regions.items()]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        print(REGIONS_DONE)
