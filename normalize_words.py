
def normalizing_word(current_guess):
    import unicodedata
    """
    normalizes and returns word.
    >>> normalizing_word(héllo)
    HELLO
    """
    normalized_guess = ''
    for c in unicodedata.normalize('NFKD', current_guess):
        if unicodedata.category(c) != 'Mn':
            normalized_guess += c
    return normalized_guess.upper()
