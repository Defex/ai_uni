
# split into teams
# sort by champ id
# champId:champId:champId:champId:champId
# sort each players spellId
# champId:SpellId:SpellId:ChampId:SpellId:SpellId
# champId:highghestSeasonRating:ChampId
# champId:SpellId:SpellId:HighestSeasonRating

def format_matches(matches):
    f_matches = []
    for match in matches:
        match = add_missing_match_keys(match)
        f_matches.append(format_match(match))
    return f_matches

def add_missing_match_keys(match):
    for p in match:
        if 'highestAchievedSeasonTier' not in p:
            p['highestAchievedSeasonTier'] = 'None'
    return match

def format_match(match):
    teams = get_team_fields(match)
    champs = [teams[0]['champ_string'], teams[1]['champ_string']]
    spells = [teams[0]['spells_string'], teams[1]['spells_string']]
    ranks = [teams[0]['rank_string'], teams[1]['rank_string']]
    is_winner = [teams[0]['is_winner'], teams[1]['is_winner']]
    formated = format_fields(champs, spells, ranks, is_winner)
    return format_mult_fields(formated)

def get_team_fields(match):
    half = int(len(match)/2)
    teams = [{ 'data': match[:half] }, { 'data': match[half:] }]
    for team in teams:
        team['data'] = sort_by_champ(team['data'])
        team['champ_string'] = join_values(team['data'], 'championId')
        team['spells_string'] = get_spell_string(team['data'])
        team['rank_string'] = join_values(team['data'], 'highestAchievedSeasonTier')
        team['is_winner'] = is_winner(team['data'])
    return teams

# check for keys

def format_fields(champs, spells, ranks, outcome):
    formated = [{}, {}]
    formated[0]['champs'] = format_field('ch', champs)
    formated[1]['champs'] = format_field('ch', list(reversed(champs)))
    formated[0]['spells'] = format_field('sp', spells)
    formated[1]['spells'] = format_field('sp', list(reversed(spells)))
    formated[0]['ranks'] = format_field('r', ranks)
    formated[1]['ranks'] = format_field('r', list(reversed(ranks)))
    formated[0]['outcome'] = 'not_spam' if outcome[0] else 'spam'
    formated[1]['outcome'] = 'not_spam' if outcome[1] else 'spam'
    return formated

def format_mult_fields(formated):
    formated[0]['ch_sp'] = join_list([formated[0]['champs'], formated[0]['spells']])
    formated[1]['ch_sp'] = join_list([formated[1]['champs'], formated[1]['spells']])
    formated[0]['ch_r'] = join_list([formated[0]['champs'], formated[0]['ranks']])
    formated[1]['ch_r'] = join_list([formated[1]['champs'], formated[1]['ranks']])
    formated[0]['ch_sp_r'] = join_list([formated[0]['champs'], formated[0]['spells'], formated[0]['ranks']])
    formated[1]['ch_sp_r'] = join_list([formated[1]['champs'], formated[1]['spells'], formated[1]['ranks']])
    return formated

def sort_by_champ(team):
    return sorted(team, key=lambda k: k['championId'])

def join_values(team, key):
    return ':'.join(str(player[key]) for player in team)

def get_spell_string(team):
    player_strings = []
    for p in team:
        spells = [p['spell1Id'], p['spell2Id']]
        player_strings.append('{}:{}'.format(min(spells), max(spells)))
    return ':'.join(s for s in player_strings)

def is_winner(team):
    return team[0]['is_winner']

def format_field(name, values):
    return '{}:{};{}'.format(name, values[0], values[1])

def join_list(l):
    return ':'.join(s for s in l)
