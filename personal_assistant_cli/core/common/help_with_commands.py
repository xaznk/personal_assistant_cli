path_address_book = "personal_assistant_cli/doc/AddressBook_commands.txt"
path_note_book = "personal_assistant_cli/doc/NoteBook_commands.txt"
path_sort_manager = "personal_assistant_cli/doc/SortManager_commands.txt"


def read_file(path):
    with open(path, "r") as file:
        return file.read()


def help_with_commands():
    choice = input("What do you need help with? Please choose a number: \n "
                   "1 - AddressBook, 2 - NoteBook, 3 - SortManager, 4 - show all commands: ")
    if choice == '1':
        return read_file(path_address_book)
    elif choice == '2':
        return read_file(path_note_book)
    elif choice == '3':
        return read_file(path_sort_manager)
    elif choice == '4':
        all_commands = [read_file(path_address_book), read_file(path_note_book), read_file(path_sort_manager)]
        return "\n".join(all_commands)
    else:
        return f"Incorrect number of choice!"
