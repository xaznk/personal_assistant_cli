from fuzzywuzzy import process

ONE_WORD_COMMANDS = ['sort', 'help', 'off']
TWO_WORDS_COMMANDS = ['show records', 'show notes', 'add record', 'add note', 'change record', 'add tag',
                      'change note', 'delete record', 'delete note', 'search record', 'search note', 'show birthdays',
                      'filter note']


def check_command(comm):
    one_word_check, two_word_check = process.extractOne(comm.split()[0], ONE_WORD_COMMANDS), process.extractOne(comm, TWO_WORDS_COMMANDS)
    check = one_word_check if one_word_check[1] > two_word_check[1] else two_word_check
    if 70 <= check[1] < 100:
        choice = input(f'Maybe you mean: {check[0]}? Please, choose a number: 1 - yes, 2 - no: ')
        if choice == '1':
            return True, check[0]
        else:
            return True, comm
    elif check[1] == 100:
        return True, comm
    elif check[1] < 70:
        return False, 'Unknown command'
