from colors import get_color
import random
import itertools
from datetime import datetime
from gameconfig import config_main
from words_from_files import get_dict_words
from login_signup import main_login
from normalize_words import normalizing_word
import matches


class GlobalVariables:
    """
    only used to store info
    """
    GAME_CONFIG = config_main()
    WORD_LENGTH = GAME_CONFIG['WORD_LENGTH'][0]
    AMOUNT_OF_TRIES = 5
    MATCHES_MAX = GAME_CONFIG['MATCHES_MAX'][0]
    RESET_MATCHES_FILE = GAME_CONFIG['RESET_MATCHES_FILE'][0]
    LIST_FILES = ["used_files/book1.txt", "used_files/book2.txt",
                  "used_files/book3.txt", "used_files/book4.txt"]


def create_dict_info_players(list_players):
    """
    Creates and returns a dict:
    {PlayerName: {points: x, position: y, tries: z, guesses: k}}
    """
    dict_info_players = {}
    for amount in range(len(list_players)):
        dict_info_players[list_players[amount]] = {"points": 0,
                                                   "position": amount + 1,
                                                   "tries": [],
                                                   "guesses": 0}

    return dict_info_players


def initialize_turns(dict_info_players):
    for player in dict_info_players:
        dict_info_players[player]['tries'] = []


def interchange_player_pos(dict_info_players):
    """
    receives a dict with the players' info, and switches their position.
    """
    list_player_positions = []
    available_pos = []

    for player in dict_info_players:
        list_player_positions += [(player, dict_info_players[player]['position'])]
        available_pos.append(dict_info_players[player]['position'])

    for player in dict_info_players:
        positions_without_players = available_pos.copy()
        if dict_info_players[player]['position'] in available_pos:
            positions_without_players.remove(dict_info_players[player]['position'])
        new_pos = random.choice(positions_without_players)
        dict_info_players[player]['position'] = new_pos
        available_pos.remove(new_pos)


def divide_turns(dict_info_players, amount_of_tries):
    """
    receives dict with the players' info & the amount of turns in the match.
    returns a list that contains the name of the player that should play in each turn
    starting with player 1.-> [p1, p2, p1, p2, p1]
    """
    players = sorted(dict_info_players.items(), key=lambda player: player[1]['position'])
    players = [player[0] for player in players]
    turns = []
    toggle = itertools.cycle(players)

    for turn in range(amount_of_tries):
        turns += [next(toggle)]

    return turns


def hide_non_guessed_letters(current_word, current_guess, hidden_word):
    """
    hides non guessed letters replacing them with ?
    """
    letters = ""
    list_guess = current_guess.split(' ')
    list_hidden_word = hidden_word.split(' ')

    for letter in range(len(current_word)):

        if get_color("Green") not in list_guess[letter] and list_hidden_word[letter] == '?':
            letters += '? '
        else:
            letters += current_word[letter] + ' '

    return letters


def create_board():
    """
    creates a list of lists which contain ? * (word length).
    the amount of inner lists is the amount of possible tries.
    """
    board = []
    for i in range(GlobalVariables.AMOUNT_OF_TRIES):
        board.append('? ' * GlobalVariables.WORD_LENGTH)

    return board


def update_board(board, tries, current_guess):
    """
    updates the board replacing the inner list in position [tries],
    with the current guess.
    """
    board[tries] = current_guess

    return board


def show_interface(current_word, hidden_word, board, end=False):
    """
    prints the board with the following format (if it's a 5-letter word):
        Hidden Word: ? ? ? ? ?
        ? ? ? ? ?
        ? ? ? ? ?
        ? ? ? ? ?
        ? ? ? ? ?
        ? ? ? ? ?
        Your guess:
    """
    print(f"Hidden Word: {hidden_word}" if not end
          else f"Hidden Word: {current_word}")

    for c in board:
        print(c)

    if end:
        text = ""
    else:
        text = input("Your guess: ").upper()

    return text


def select_word():
    """
    picks a random word from dict_words.keys()
    """
    dict_words = get_dict_words(GlobalVariables.LIST_FILES, GlobalVariables.WORD_LENGTH)
    list_words = sorted(dict_words.keys(), key=lambda dic: dic[0])
    
    return list_words[random.randint(0, len(list_words))].upper()


def define_victory(current_guess):
    """
    receives the already painted current guess,
    if it's all green returns True else returns False.
    """
    counter = 0
    current_guess = current_guess.split(' ')
    match_state = False

    for i in current_guess:
        if get_color("Green") in i:
            counter += 1
    if counter == GlobalVariables.WORD_LENGTH:
        match_state = True

    return match_state


def count_letters(current_word):
    """
    returns a dict {letter in current word: times that the letter is repeated, ...}
    """
    dict_letters = {}
    for letter in current_word:
        if letter not in dict_letters.keys():
            dict_letters[letter] = 1
        else:
            dict_letters[letter] += 1

    return dict_letters


def validate_letters(current_word, current_guess):
    """
    paints the current guess letter by letter and adds spaces to make it more readable,
    green - if the letter is in the correct spot in current word
    yellow - if the letter is in the word but not in the right spot
    dark gray - if the letter isn't in the word
    """
    dict_letters = count_letters(current_word)
    colored_word = ''

    for i in range(GlobalVariables.WORD_LENGTH):
        if current_guess[i] == current_word[i]:
            colored_word += get_color("Green") + current_guess[i] + " "

        else:
            colored_word += get_color("DarkGray") + current_guess[i] + " "

    for i in range(GlobalVariables.WORD_LENGTH):
        if (current_guess[i] in current_word and
                current_guess[i] != current_word[i] and
                ((colored_word.count(get_color("Yellow") + current_guess[i]) +
                  (colored_word.count(get_color("Green") + current_guess[i])))
                 < dict_letters[current_guess[i]])):
            colored_word = colored_word.replace(
                get_color("DarkGray") +
                current_guess[i], get_color("Yellow") + current_guess[i], 1) + " "

    colored_word += get_color("Default")

    return colored_word


def validate_guess(current_guess):
    """
    validates that the guess has as many letters as the word, and that it is indeed a word,
    if it is valid then returns what normalizing_word() returns else, keeps asking for a new guess.
    """
    while len(current_guess) != GlobalVariables.WORD_LENGTH or not current_guess.isalpha():
        if len(current_guess) != GlobalVariables.WORD_LENGTH:
            print('Error, your guess should have the same length '
                  'as the hidden word.')
        elif not current_guess.isalpha():
            print('Error, your guess should be only letters')
        current_guess = input("Your guess: ").upper()

    return (normalizing_word(current_guess)).upper()


def player_points(player1, winner, dict_info_players, tries):
    """
    receives the player that started first, the winner (if there is no winner then ''),
    the dict with the players' info and the current try.
    modifies the dict[points] accordingly, and returns a list of tuples [(player, points earned), ...]
    """
    dict_points = {1: 50, 2: 40, 3: 30, 4: 20, 5: 10}
    obtained_points_a = 100
    obtained_points_b = 50
    match_points = []

    if winner == '':
        for player in dict_info_players:
            if player == player1:
                dict_info_players[player]['points'] -= obtained_points_a
                match_points.append((player, (-obtained_points_a)))
            else:
                dict_info_players[player]['points'] -= obtained_points_b
                match_points.append((player, (-obtained_points_b)))
    else:
        for player in dict_info_players:

            if player == winner:
                dict_info_players[player]['points'] += dict_points[tries]
                match_points.append((player, dict_points[tries]))
            else:
                dict_info_players[player]['points'] -= dict_points[tries]
                match_points.append((player, (-dict_points[tries])))

    return match_points


def select_winner(dict_info_players):
    """
    receives the dict with the players' info, returns a tuple (name, {inner dict with info}) if
    there is a winner else returns a list [draw, total points]
    """
    list_players = (sorted(dict_info_players.items(), key=lambda player: player[1]['points'], reverse=True))
    if list_players[0][1]['points'] != list_players[1][1]['points']:
        winner = list_players[0]
    else:
        winner = ['draw', list_players[0][1]['points']]
    return winner


def show_match_points(match_points, dict_info_players):
    """
    receives match points -> [(name, points earned), ...] and the dict with the players' info,
    prints the corresponding message depending on the player.
    """
    for player in match_points:
        name = player[0].upper()
        match_points = player[1]
        total_points = dict_info_players[player[0]]['points']
        msg = f"{name} you just got {match_points} points," \
              f" and you have {total_points} accumulated points" if match_points > 0 else \
              f"{name} you lost {-1 * match_points} points," \
              f" and you have {total_points} accumulated points"
        print(msg)


def game_logic(dict_info_players):
    """
    receives the dict with the info of the players.
    Contains the logic of a singular match of WORDLE, not the whole game.
    (runs once per new word)
    """
    tries = 0
    time_start = datetime.now()
    time_end = None
    current_word = select_word()
    hidden_word = "? " * GlobalVariables.WORD_LENGTH
    match_state = False
    list_players = divide_turns(dict_info_players, GlobalVariables.AMOUNT_OF_TRIES)
    initialize_turns(dict_info_players)
    winner = ''
    board = create_board()
    while tries < GlobalVariables.AMOUNT_OF_TRIES and not match_state:
        print(f"\n{list_players[tries].upper()}'s Turn")
        current_guess = show_interface(current_word, hidden_word, board)
        dict_info_players[list_players[tries]]['tries'].append(tries + 1)
        current_guess = validate_guess(current_guess)
        current_guess = validate_letters(current_word, current_guess)
        hidden_word = hide_non_guessed_letters(current_word, current_guess, hidden_word)
        board = update_board(board, tries, current_guess)
        match_state = define_victory(current_guess)
        if match_state or (tries == GlobalVariables.AMOUNT_OF_TRIES - 1):
            board = update_board(board, tries, current_guess)
            show_interface(current_word, hidden_word, board, end=True)
            time_end = datetime.now()
            if match_state:
                winner = list_players[tries]
                dict_info_players[winner]["guesses"] += 1
        tries += 1

    delta_time = time_end - time_start
    mins = int(delta_time.total_seconds() / 60)
    secs = int(delta_time.total_seconds() - (60 * mins))
    match_points = player_points(list_players[0], winner, dict_info_players, tries)

    print(f'The word has been guessed in {mins} minutes and {secs} seconds :)') \
        if match_state else print("The word has not been guessed :(")

    show_match_points(match_points, dict_info_players)


def game_runner():
    """
    Runs the whole game, and allows for several matches to be played (several game_logic invocations).
    """
    print('\n~ WELCOME TO WORDLE ~')
    print(f'Current Config:'
          f'\n  Word length - {GlobalVariables.GAME_CONFIG["WORD_LENGTH"]}'
          f'\n  Matches max - {GlobalVariables.GAME_CONFIG["MATCHES_MAX"]}'
          f'\n  Reset matches file - {GlobalVariables.GAME_CONFIG["RESET_MATCHES_FILE"]}')
    list_players = main_login()
    if list_players[0] and list_players[1]:
        dict_info_players = create_dict_info_players(list_players)
        replay = True
        current_match = 1
        list_matches = []

        while replay and current_match <= GlobalVariables.MATCHES_MAX:
            game_logic(dict_info_players)
            match_date = datetime.now()
            matches.update_list_matches(list_matches, current_match, dict_info_players,
                                        match_date.strftime("%d/%m/%Y"), match_date.strftime("%H:%M:%S"))
            current_match += 1
            if current_match <= GlobalVariables.MATCHES_MAX:
                replay_option = (input('Play again? (Y/N): ')).upper()
                while replay_option not in 'YN':
                    replay_option = (input('Error, only options are (Y/N): ')).upper()
                interchange_player_pos(dict_info_players)
                if replay_option == 'N':
                    replay = False

        matches.show_and_save_matches_info(list_matches, GlobalVariables.RESET_MATCHES_FILE)
        winner = select_winner(dict_info_players)
        if winner[0] != 'draw':
            print(f"\nThe winner is {winner[0].upper()} with a total of {winner[1]['points']} points")
        else:
            print(f"\nDRAW! the game ended in draw with {winner[1]} points!")
        print('Thanks for playing!')
    else:
        print('\nTwo players needed in order to play!')


game_runner()
