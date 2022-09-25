from gameconfig import config_main

GAME_CONFIG = config_main()
WORD_LENGTH = GAME_CONFIG['WORD_LENGTH'][0]
AMOUNT_OF_TRIES = 5
MATCHES_MAX = GAME_CONFIG['MATCHES_MAX'][0]
RESET_MATCHES_FILE = GAME_CONFIG['RESET_MATCHES_FILE'][0]
LIST_FILES = ["used_files/book1.txt", "used_files/book2.txt", "used_files/book3.txt", "used_files/book4.txt"]
