from csv_file import *


def update_list_matches(list_matches, current_match, dict_info_players, match_date, match_time):
    for players in dict_info_players:
        list_matches.append((current_match, match_date, match_time, players, dict_info_players[players]['guesses'],
                             len(dict_info_players[players]["tries"])))


def show_and_save_matches_info(list_matches, reset_matches_file):
    list_data = []
    dict_summary = {}
    #Match    MatchDate    MatchTime    PlayerName    Guesses    Tries
    list_matches.sort(key=lambda info_tuple: info_tuple[4], reverse=True)
    for match in list_matches:
        if match[3] not in dict_summary.keys():
            dict_summary[match[3]] = [match[4], match[5]]
        else:
            dict_summary[match[3]][0] += match[4]
            dict_summary[match[3]][1] += match[5]
        list_data.append(f'{match[1]},{match[2]},{match[3]},{match[4]},{match[5]}')

    mode = 'w' if reset_matches_file else 'a'
    create_csv_file(list_data, 'used_files/matches.csv', mode)
    for i in dict_summary.keys():
        print(f"Name - {i}\tGuesses - {dict_summary[i][0]}\tTries - {dict_summary[i][1]}")
