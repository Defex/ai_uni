from lib.lol.Fetcher import LolFetcher

data = {
    'ru': [],
    'kr': [],
    'br1': [],
    'oc1': [],
    'jp1': [],
    'na1': [],
    'eun1': ['Honzicek', 'SugoiBaka', 'MikeAlpha', 'dudodu', 'Xayira', 'Dekadencja', 'IonlycarryNoona'],
    'euw1': [],
    'tr1': [],
    'la1': [],
    'la2': [],
}





if __name__ == '__main__':
    fetcher = LolFetcher()
    fetcher.download_matches_from_regions(data, 10, 'lol_match_data')


