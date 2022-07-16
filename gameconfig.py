
def read_config_file(config):
    line = config.readline()
    return line.rstrip("\n").split(",") if line else ['', '']


def config_dic_mod(config_file, config_dic):
    """
    receives config_dic and config_file(already open),
    modifies config_dic based off of what it reads from the csv file.
    """
    min_word_length = 3
    max_word_length = 12
    min_matches_max = 2
    max_matches_max = 10
    try:
        config, value = read_config_file(config_file)
    except ValueError:
        config, value = ['', '']

    while config:
        if config == 'WORD_LENGTH':
            if min_word_length <= int(value) <= max_word_length:
                config_dic['WORD_LENGTH'] = [int(value), 'by config.']

        elif config == 'MATCHES_MAX':
            if min_matches_max <= int(value) <= max_matches_max:
                config_dic['MATCHES_MAX'] = [int(value), 'by config.']

        elif config == 'RESET_MATCHES_FILE':
            if value == 'False':
                config_dic['RESET_MATCHES_FILE'] = [False, 'by config.']
            elif value == 'True':
                config_dic['RESET_MATCHES_FILE'] = [True, 'by config.']

        try:
            config, value = read_config_file(config_file)
        except ValueError:
            config, value = ['', '']

    return config_dic


def config_main():
    """
    returns what it gets from config_dic_mod, if it can't find config_file.csv
    returns a default dict.
    """
    config_default = {'WORD_LENGTH': [5, 'by default.'],
                      'MATCHES_MAX': [5, 'by default.'],
                      'RESET_MATCHES_FILE': [False, 'by default.']}
    config_final = {}
    try:
        with open("used_files/config_file.csv") as config:
            config_final = config_dic_mod(config, config_default)
    except FileNotFoundError:
        config_final = config_default
    return config_final
