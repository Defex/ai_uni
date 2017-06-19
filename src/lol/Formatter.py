keys = {
    'spell1Id', 'spell2Id', 'championId', 'highestAchievedSeasonTier'
}

class LolFormatter():
    def format_participants(self, participants):
        formated = []
        for participant in participants:
            formated.append(self.format_participant(participant))
        return formated

    def format_participant(self, p):
        participant = {}
        for key in keys:
            if key in p:
                participant[key] = p[key]
        if 'stats' in p:
            if 'winner' in p['stats']:
                participant['is_winner'] = p['stats']['winner']
            else:
                participant['is_winner'] = p['stats']['win']
        return participant
    
    def format_match(self, match):
        return self.format_participants(match['participants'])
    
    def format_matches(self, matches):
        matches_data = []
        for match in matches:
            if match is not None:
                formated = self.format_match(match)
                if len(formated) == 10:
                    matches_data.append(formated)
        return matches_data

lol_formatter = LolFormatter()
