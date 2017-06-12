keys = {
    'spell1Id', 'spell2Id', 'championId', 'highestAchievedSeasonTier'
}

class MatchFormatter():
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
            matches_data.append(self.format_match(match))
        return matches_data
    
    @staticmethod
    def format_file_data(file_data):
        return file_data['matches']
    
    @staticmethod
    def format_files_data(files):
        files_data = []
        for f in files:
            files_data.extend(MatchFormatter.format_file_data(f))
        return files_data
