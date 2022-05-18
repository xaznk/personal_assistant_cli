from personal_assistant_cli.core.common.db_config import conn, cur

from personal_assistant_cli.core.address_book.address_book import AddressBook
from personal_assistant_cli.core.address_book.address_book_input_provider import AddressBookInputProvider

from personal_assistant_cli.core.note_book.note_book import NoteBook
from personal_assistant_cli.core.note_book.note_book_input_provider import NoteBookInputProvider

from personal_assistant_cli.core.sort_manager.sort_manager import SortManager
from personal_assistant_cli.core.context_analyzer.context_analyzer import ContextAnalyzer

from personal_assistant_cli.core.common.help_with_commands import help_with_commands


def main():
    address_book = AddressBook()
    address_book_input_provider = AddressBookInputProvider()

    note_book = NoteBook()
    note_book_input_provider = NoteBookInputProvider()

    sort_manager = SortManager()
    context_analyzer = ContextAnalyzer()
    hello_phrase = "Hello! \n" \
                   "I'm your bot - a personal assistant.\n" \
                   "I can help you with three areas: the AddressBook, the NoteBook, and the SortManager. \n" \
                   "Just remind that you can use:\n" \
                   " help - to view a list of all commands and how to use them; \n" \
                   " off - to end our communication. \n" \
                   "Let's start! \n"

    print(hello_phrase)
    while True:
        user_request = input(">>> : ")
        responsible_module, command, user_data = context_analyzer.analyze(user_request)
        if responsible_module == AddressBook:
            if command:
                parsed_user_data = address_book_input_provider.provide(command, user_data)
                if "error" in parsed_user_data:
                    answer = parsed_user_data["error"]
                else:
                    answer = command(address_book, parsed_user_data)
            else:
                answer = "Wrong command for AddressBook module."
        elif responsible_module == NoteBook:
            if command:
                parsed_user_data = note_book_input_provider.provide(command, user_data)
                if "error" in parsed_user_data:
                    answer = parsed_user_data["error"]
                else:
                    answer = command(note_book, parsed_user_data)
            else:
                answer = "Wrong command for NoteBook module."
        elif responsible_module == SortManager:
            if command:
                answer = command(sort_manager, user_data)
            else:
                answer = "Wrong command for SortManager module."
        elif responsible_module == "main":
            if command == "help":
                answer = help_with_commands()
            elif command == "off":
                cur.close()
                conn.close()
                print("Good bye!")
                break
            else:
                answer = "Wrong command for Main module."
        else:
            answer = "Can not understand what you mean."

        print(answer)


if __name__ == "__main__":
    main()

