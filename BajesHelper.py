    reader = Reader() #reads data from file
    match_formatter = MatchFormatter() #formats match data
    url_reader = UrlReader() #get data from api
    bajes_formatter = BajesFormatter() #formats data for bajes
    bajes = Bajes() #calculates by bajes algorithm
    
    # reading from file
    text = reader.read_file(MATCH_DATA)
    file_data = match_formatter.format_matches(text['matches'])
    bajes_data = bajes_formatter.format_for_bajes(file_data)
    # adding bajes learn data
    for participant in bajes_data:
        bajes.add_words(participant['data'], participant['outcome'])
    bajes.calculate_spam_probabilities()
    #  getting online match data
    game_id=1684320341
    match = url_reader.get_match_by_game_id(game_id)
    formated_match = match_formatter.format_match(match)
    bajes_formated_match = bajes_formatter.format_match(formated_match[0:5])
    test_data = {}
    for participant in bajes_formated_match:
        bajes.add_words_test(participant['data'], 'count', test_data)
    bajes.set_bajes_chance(test_data)
    values = bajes.get_closest_and_farest_values(test_data)
    result = bajes.calc_if_is_spam(values)
    print(result)
    # print(json.dumps(test_data))
    # print(json.dumps(formated_match[5:10]))
    print(json.dumps(bajes_formated_match))