from personal_assistant_cli.core.address_book.address_book import AddressBook
from personal_assistant_cli.core.note_book.note_book import NoteBook
from personal_assistant_cli.core.sort_manager.sort_manager import SortManager
from personal_assistant_cli.core.context_analyzer.fuzz import check_command

import types


class ContextAnalyzer:

    def analyze(self, request: str) -> (type, types.FunctionType, str):
        """
        Get string-request from user and return from this the following:
            - responsible_module - what module should do a command (AddressBook, NoteBook or SortManager);
            - command - a command for responsible_module;
            - user_data - everything else left in the string-request
        """

        if request == "":
            return None, None, None

        responsible_module, command, user_data = None, None, None
        words = request.split()

        check_answer, check_text = check_command(" ".join(words[0:2]))
        if check_answer:
            if check_text in ["off", "help", "sort"]:
                if check_text == "sort":
                    words[0] = check_text
                else:
                    request = check_text
            else:
                new_command_text = check_text.split()
                words[0], words[1] = new_command_text[0], new_command_text[1]
                request = " ".join(words)

        if request == "off":
            responsible_module = "main"
            command = "off"
        elif request == "help":
            responsible_module = "main"
            command = "help"
        elif "show birthday" in request:
            responsible_module = AddressBook
            command = AddressBook.show_users_birthday
            user_data = " ".join(words[2:])
        elif "show record" in request:
            responsible_module = AddressBook
            command = AddressBook.get_records
            user_data = " ".join(words[2:])
        elif "show note" in request:
            responsible_module = NoteBook
            command = NoteBook.get_table
            user_data = " ".join(words[2:])
        elif "add tag" in request:
            responsible_module = NoteBook
            command = NoteBook.add_tag_to_note
            user_data = " ".join(words[2:])
        elif "sort" == words[0]:
            responsible_module = SortManager
            command = SortManager.sort
            user_data = " ".join(words[1:])
        elif len(words) > 1:
            if "record" == words[1]:
                responsible_module = AddressBook
                if "add" == words[0]:
                    command = AddressBook.add
                elif "change" == words[0]:
                    command = AddressBook.change
                elif "delete" == words[0]:
                    command = AddressBook.delete
                elif "search" == words[0]:
                    command = AddressBook.filter

                user_data = " ".join(words[2:])
            elif "note" == words[1]:
                responsible_module = NoteBook
                if "add" == words[0]:
                    command = NoteBook.add
                elif "change" == words[0]:
                    command = NoteBook.change
                elif "delete" == words[0]:
                    command = NoteBook.delete
                elif "filter" == words[0]:
                    command = NoteBook.filter_for_tags
                elif "tag" == words[0]:
                    command = NoteBook.add_tag_to_note
                elif "search" == words[0]:
                    command = NoteBook.search

                user_data = " ".join(words[2:])

        return responsible_module, command, user_data
