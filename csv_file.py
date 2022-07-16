def create_csv_file(content, file_name, mode):
    """
    creates used_words.csv and saves the content in it line by line, according to the mode.
    """
    csv_file = open(file_name, mode, encoding='utf8')
    for line in content:
        csv_file.write(f'{line}\n')

    csv_file.close()
