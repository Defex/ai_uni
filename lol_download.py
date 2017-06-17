from src.lol.Fetcher import LolFetcher
from src.lol.APIHelper import LolAPIHelper

data = {
    'ru': [],
    'kr': [],
    'br1': [],
    'oc1': [],
    'jp1': [],
    'na1': ['General Godhogg', 'Mr DolFin', 'Veigar Doom Bot', 'Groupon', 'Hi Can I Support', 'EveCP', 'BananaZac', 'Khalami', 'Stormcleave', 'Jezcp', 'Tobias Fate', 'GL IM SCRIPTING', 'Hentai Kami Sama', 'Ghween', 'Liquid KonKwon', 'Nasteey', 'Lesu', 'Silencee Sucks', 'Japanese Import', 'Annie Bot', 'HellaMoistBrah', 'ily Gen', 'LetsBounceLolis', 'ValCP', 'Biscuit Crusader', 'MeBlueTY', 'LL Stylish', 'SWKM', 'Kazahana', 'Keemö', 'Rekk', 'Robins Pet', 'Screaming', '1 Mìn 1 Sec', 'Korweeabooo', 'RiceLegend', 'KiNG Nidhogg', 'Shajae', 'Morou', 'Freeze', 'AxelsFinalFlame', 'The Harem King', 'Fufu loves duodu', 'ªłº', 'Captain Stevie B', 'Syrian Refuge', 'always plan ahea', 'McCashDollar', 'JeanPie', 'Marko Mid', 'Skaarlet Kledder', 'Uncle', 'Nikjojo', 'Jánna', 'The Best Aatrox ', 'Capriciøus', 'Espir III', 'Quinome', 'MeBlueTY', 'Chàse', 'Papa Smurfing', 'Nillers', 'Jiu Jiu', 'twitchtv Sithu', 'Sasuni', 'Sweaty ASol', 'Palidor', 'PIays With Balls', 'bvcx222', 'Ghalvz', 'SaintKilian', 'Riddler', 'Fufu loves duodu', 'Ward11', 'Gl in Wiisports', 'Scrandor', 'High Boob Yasuo', 'Keloro', 'NoSkillean', 'Keemö', 'Méru', 'Diamond 1 Khazix', 'Janna Windforce', 'sammystinky', 'Boosted bot', 'Katar', 'Zaion', 'Best Xin Player', 'Zeg Prime', 'lilBthebasedG', 'Sithu', 'DeadLee', 'Glory IX', 'Prophase II', 'SkarletEve', 'xIrezz', 'Tayme', 'jbraggs', 'Øsama', 'Teamfighting', 'TAI DRÄVEN XD', 'parnellyx', 'Heroˉ', 'ScrubNoob', 'Photograph', 'SkarletEve', 'LawlietLelouch', 'FirstTimeCaitlyn', 'MrFluffy631', 'The Eggsalad', 'Cat Girl Sakuya', 'Sif is God', 'MICCOY', 'Mr Cleań', 'Unari', 'Sheiden', 'Mr Gimix', 'mamooj', 'Atychi', 'iPav', 'Stuner king', 'Hyorimaru', 'FACEB00K', 'Ryan Mangin', 'Bobjenkins', 'Kkat sucks', 'Best Maid NA', 'S Dlana 2 NA', 'DarkSteelAngel', 'wonderful baboon', 'Rabbithásu', 'Donut Delight', 'Katlife', 'Rabbithasu', 'Gl in Wiisports', 'Dank Pho', 'S D 2 NA', 'TheOddOrange', 'Tangularx', 'WJSN Eunseo', 'xDD', 'Cat Girl Sakuya', 'ItsYourChoice', 'Derp Shaco', 'Back To Paradíse', 'Yamikaze', 'Parrks', 'Useless Champ', 'Keegun', 'Stephen M Ross'],
    'eun1': ['Honzicek', 'SugoiBaka', 'MikeAlpha', 'dudodu', 'Xayira', 'Dekadencja', 'IonlycarryNoona'],
    'euw1': ['Mirko XIII', 'Arabian Princess', 'TheUglyCuckling', 'ssecnirP naibarA', 'Maid of Team', 'IonlycarryNoona', 'S1nwar', 'GFWasTaken', 'eXeF', '2519202613', '5xSQ Solgrynen', 'Sythez', 'Neddus', 'RUR Lešnik', 'Tossy', 'Joe Cat', 'Umoraki', 'Lenish', 'TuEsUnGrosNAZE', 'RomRazor', 'SirBerlinStyle', 'Swordsmanship', 'Delej', 'xAwJChristia', 'KRAKO', 'King Brandon', 'Ryphex', 'InvincibleZen', 'Zizi léane', 'Deserve Victory', 'BlueWingsx3', 'CrocodyIe', 'Drømmegutten', 'DarkestSide', 'Formel1 Bent', 'Sirias', 'Kev1inFromEUNE', 'ι ι', 'EDUCATIONDEMERDE', 'ElUtilitySuite', 'CROWD FAVOUR', 'JameRz', 'Lunatica', 'Ñiii', 's1mpl3', 'Pytangelus', 'TheGodDamnNoob', 'WL YOW', 'Tyrin', 'ArrowsofAlfar', 'Je suis Simon', 'inF Luque', 'Ankan', 'Kemseptyni', 'AMAGAD SÄLIS', 'Zedxsmurf EUW', 'NoseyNoodle', 'Pademelon', 'eGirl Skynia', 'Int machine'],
    'tr1': [],
    'la1': [],
    'la2': [],
}

if __name__ == '__main__':
    # for k,v in data.items():
    #     helper = LolAPIHelper(k)
    #     for name in v:
    #         print(name)
    
    fetcher = LolFetcher()
    fetcher.download_matches_from_regions(data, 100, 'lol_match_data')


