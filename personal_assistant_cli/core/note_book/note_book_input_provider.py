from personal_assistant_cli.core.note_book.note_book import NoteBook
from personal_assistant_cli.core.common.identifier import Identifier

from types import FunctionType
from typing import Union


class NoteBookInputProvider:
    def __init__(self):
        self.__identifier = Identifier()

    def provide(self, command: Union[FunctionType, None], user_data: str) -> dict:
        if user_data is None or user_data == "":
            return self.__provide_data_with_requests(command)
        else:
            return self.__parse_user_data_from_scratch(user_data, command)

    ###############
    # Smart non-request bot:
    ###############

    def __parse_user_data_from_scratch(self, user_data: str, command: Union[FunctionType, None]) -> dict:
        if command == NoteBook.add:
            return self.__parse_add_user_data(user_data)
        elif command == NoteBook.add_tag_to_note:
            return self.__parse_add_tag_user_data(user_data)
        elif command == NoteBook.change:
            return self.__parse_change_user_data(user_data)
        elif command == NoteBook.delete:
            return self.__parse_delete_user_data(user_data)
        elif command == NoteBook.filter_for_tags:
            return self.__parse_filter_for_tags_user_data(user_data)
        elif command == NoteBook.search:
            return self.__parse_search_user_data(user_data)
        elif command == NoteBook.get_table:
            return {}
        else:
            return {"error": "Undefined command provided for NoteBook."}

    @staticmethod
    def __parse_add_user_data(user_data: str) -> dict:
        return {"text": user_data}

    @staticmethod
    def __parse_add_tag_user_data(user_data: str) -> dict:
        parts = user_data.split()
        if len(parts) < 2:
            return {"error": f"Not enough data for adding tag: {user_data}. Required id and tag."}

        identifier = parts[0]
        if not identifier.isnumeric():
            return {"error": f"Provided wrong id: {identifier}. Id should be a number."}
        tag = parts[1]

        return {"id": identifier, "tag": tag}

    @staticmethod
    def __parse_change_user_data(user_data: str) -> dict:
        parts = user_data.split()
        if len(parts) < 2:
            return {"error": f"Not enough data for changing note: {user_data}. Required id and text."}

        identifier = parts[0]
        if not identifier.isnumeric():
            return {"error": f"Provided wrong id: {identifier}. Id should be a number."}
        text = " ".join(parts[1:])

        return {"id": identifier, "text": text}

    @staticmethod
    def __parse_delete_user_data(user_data: str) -> dict:
        if not user_data.isnumeric():
            return {"error": f"Provided wrong id: {user_data}. Id should be a number."}

        return {"id": user_data}

    @staticmethod
    def __parse_filter_for_tags_user_data(user_data: str) -> dict:
        return {"tag": user_data}

    @staticmethod
    def __parse_search_user_data(user_data: str) -> dict:
        return {"phrase": user_data}

    ###############
    # Noising asking bot:
    ###############

    def __provide_data_with_requests(self, command: Union[FunctionType, None]) -> dict:
        if command == NoteBook.add:
            return self.__parse_add_with_requests()
        elif command == NoteBook.add_tag_to_note:
            return self.__parse_add_tag_with_requests()
        elif command == NoteBook.change:
            return self.__parse_change_with_requests()
        elif command == NoteBook.delete:
            return self.__parse_delete_with_requests()
        elif command == NoteBook.filter_for_tags:
            return self.__parse_filter_for_tags_with_requests()
        elif command == NoteBook.search:
            return self.__parse_search_with_requests()
        elif command == NoteBook.get_table:
            return {}
        else:
            return {"error": "Undefined command provided for NoteBook."}

    @staticmethod
    def __parse_add_with_requests() -> dict:
        text = input("Input text for note: ")

        return {"text": text}

    @staticmethod
    def __parse_add_tag_with_requests() -> dict:
        note_table = NoteBook().get_table({})
        print(f"Notes: \n{note_table}")
        identifier = input("Choose id number: ")
        if not identifier.isnumeric():
            return {"error": f"Provided wrong id: {identifier}. Id should be a number."}
        tag = input("Input tag: ")

        return {"tag": tag, "id": identifier}

    @staticmethod
    def __parse_change_with_requests() -> dict:
        note_table = NoteBook().get_table({})
        print(f"Notes: \n{note_table}")
        identifier = input("Choose id number: ")
        if not identifier.isnumeric():
            return {"error": f"Provided wrong id: {identifier}. Id should be a number."}

        text = input("Input text for note: ")
        return {"id": identifier, "text": text}

    @staticmethod
    def __parse_delete_with_requests() -> dict:
        note_table = NoteBook().get_table({})
        print(f"Notes: \n{note_table}")
        identifier = input("Choose id number: ")
        if not identifier.isnumeric():
            return {"error": f"Provided wrong id: {identifier}. Id should be a number."}

        return {"id": identifier}

    @staticmethod
    def __parse_filter_for_tags_with_requests() -> dict:
        tag = input("Input tag: ")

        return {"tag": tag}

    @staticmethod
    def __parse_search_with_requests() -> dict:
        phrase = input("Input phrase for search in notes: ")

        return {"phrase": phrase}
