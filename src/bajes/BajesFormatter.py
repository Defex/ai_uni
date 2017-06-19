# old class nothing fancy
class BajesFormatter():
    def format_for_bajes(self, matches):
        participants_data = []
        for match in matches:
            participants_data.extend(self.format_match(match))
        return participants_data
    
    def format_match(self, match):
        p_data = []
        for participant in match:
            participant_data = self.format_match_participant(participant)
            p_data.append(participant_data)
        return p_data

    def format_match_participant(self, participant):
        participant_data = {
            'data': [],
            'outcome': ''
        }
        self.get_k_v(participant_data, 'k', participant)
        return participant_data

    def get_k_v(self, data, k, v):
        if type(v) is dict:
            for key, val in v.items():
                self.get_k_v(data, key, val)
        elif type(v) is list:
            for i in v:
                self.get_k_v(data, k, i)
        elif k is 'is_winner':
            if v:
                data['outcome'] = 'not_spam'
            else:
                data['outcome'] = 'spam'
        else:
            data['data'].append(self.print_key_value(k, v))

    def print_key_value(self, k, v):
        return '{}:{}'.format(k, v)
