from normalize_words import normalizing_word


def add_word_to_dict(dict_words, word, word_length, index_file):
    """
    receives the dict_words and adds the received word(upper) to it as a key
    if it is indeed a word and has the same length as word_length, and the value would be
    the number of times that word appears in the current file being read.
    """
    only_letters_word = only_letters(word)
    if (only_letters_word.isalpha() and
            (len(only_letters_word) == word_length)):
        if only_letters_word not in dict_words.keys():
            dict_words[only_letters_word] = {index_file: 1}
        elif index_file not in dict_words[only_letters_word.upper()].keys():
            dict_words[only_letters_word][index_file] = 1
        else:
            dict_words[only_letters_word][index_file] += 1


def only_letters(word):
    """
    normalizes word and gets rid of punctuation characters.
    """
    normalized_word = normalizing_word(word)
    no_sp_chars = ''
    sp_chars = ',.:;¡!¿?-_'

    for c in normalized_word:
        if c not in sp_chars:
            no_sp_chars += c
    
    return normalized_word.upper()


def get_words_from_file(dict_words, file_name, index_file,
                        word_length):
    """
    reads file and invokes add_word_to_dict per read word.
    """
    with open(file_name, 'r', encoding="utf8") as current_file:
        for line in current_file:
            list_words = line.rstrip("\n").split(' ')

            for word in list_words:
                add_word_to_dict(dict_words, word,
                                 word_length, index_file)


def create_csv_file(dict_words, amount_of_files):
    """
    creates used_words.csv and writes all the info from dict_words on it.
    """
    csv_file = open('used_files/used_words.csv', 'w', encoding='utf8')
    sorted_dict = sorted(dict_words.items(), key=lambda jdict: jdict[0])
    for key in sorted_dict:
        list_quantity = ''
        for item in range(amount_of_files):
            if item in key[1]:
                list_quantity += f'{str(key[1][item])},'
            else:
                list_quantity += '0,'
        csv_file.write(f'{key[0].lower()},{list_quantity.rstrip(",")} \n')

    csv_file.close()


def get_dict_words(list_files, word_length):
    """
    main function that runs the module, receives a list of files to be read and the length of the word,
    returns a dict with all the read words as keys and the amount of times they appear per file
    as values.
    """
    dict_words = {}
    for index_file in range(len(list_files)):
        get_words_from_file(dict_words, list_files[index_file],
                            index_file, word_length)

    create_csv_file(dict_words, len(list_files))

    return dict_words
