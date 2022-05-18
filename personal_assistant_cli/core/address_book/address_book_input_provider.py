from personal_assistant_cli.core.address_book.address_book import AddressBook
from personal_assistant_cli.core.common.identifier import Identifier
from personal_assistant_cli.core.common.verify import phone_verify, email_verify, birthday_verify

from types import FunctionType
from typing import Union


class AddressBookInputProvider:
    def __init__(self):
        self.__identifier = Identifier()
        self.__information_type = {"1": "phone", "2": "email", "3": "birthday", "4": "address"}

    def provide(self, command: Union[FunctionType, None], user_data: str) -> dict:
        if user_data is None or user_data == "":
            return self.__parse_user_data_with_requests(command)
        else:
            return self.__parse_user_data_from_scratch(user_data, command)

    ###############
    # Smart non-request bot:
    ###############

    def __parse_user_data_from_scratch(self, user_data: str, command: Union[FunctionType, None]) -> dict:
        if command == AddressBook.add:
            return self.__parse_add_user_data(user_data)
        elif command == AddressBook.change:
            return self.__parse_change_user_data(user_data)
        elif command == AddressBook.delete:
            return self.__parse_delete_user_data(user_data)
        elif command == AddressBook.filter:
            return self.__parse_filter_user_data(user_data)
        elif command == AddressBook.show_users_birthday:
            return self.__parse_show_birthdays_user_data(user_data)
        elif command == AddressBook.get_records:
            return {}
        else:
            return {"error": "Undefined command provided for AddressBook."}

    def __parse_add_user_data(self, user_data: str) -> dict:
        parsed_user_data = dict()
        parts = user_data.split()
        parsed_user_data["name"] = parts[0]

        address = ""
        error_msg = ""
        for part in parts[1:]:
            if self.__identifier.is_email(part):
                email, _ = email_verify(part)
                parsed_user_data["email"] = email
            elif self.__identifier.is_phone(part):
                phone, _ = phone_verify(part)
                parsed_user_data["phone"] = phone
            elif self.__identifier.is_birthday(part):
                birthday, _ = birthday_verify(part)
                if not birthday:
                    error_msg += "Birthday is not correct.\n"
                else:
                    parsed_user_data["birthday"] = birthday
            else:
                address += part + " "

        if address != "":
            parsed_user_data["address"] = address

        if error_msg:
            return {"error": error_msg}

        return parsed_user_data

    def __parse_change_user_data(self, user_data: str) -> dict:
        parsed_user_data = dict()
        parts = user_data.split()
        parsed_user_data["name"] = parts[0]

        address = ""
        error_msg = ""
        for part in parts[1:]:
            if self.__identifier.is_email(part):
                email, _ = email_verify(part)
                parsed_user_data["email"] = email
            elif self.__identifier.is_phone(part):
                phone, _ = phone_verify(part)
                parsed_user_data["phone"] = phone
            elif self.__identifier.is_birthday(part):
                birthday, _ = birthday_verify(part)
                if not birthday:
                    error_msg += "Birthday is not correct.\n"
                else:
                    parsed_user_data["birthday"] = birthday
            else:
                address += part + " "

        if address != "":
            parsed_user_data["address"] = address

        if error_msg:
            return {"error": error_msg}

        return parsed_user_data

    @staticmethod
    def __parse_delete_user_data(user_data: str) -> dict:
        return {"name": user_data}

    @staticmethod
    def __parse_filter_user_data(user_data: str) -> dict:
        return {"phrase": user_data}

    @staticmethod
    def __parse_show_birthdays_user_data(user_data: str) -> dict:
        if user_data.isnumeric():
            return {"days": int(user_data)}

        return {"error": f"User provide invalid number of days in show birthdays method: {user_data}"}

    ###############
    # Noising asking bot:
    ###############

    def __parse_user_data_with_requests(self, command: Union[FunctionType, None]) -> dict:
        if command == AddressBook.add:
            return self.__parse_add_with_requests()
        elif command == AddressBook.change:
            return self.__parse_change_with_requests()
        elif command == AddressBook.delete:
            return self.__parse_delete_with_requests()
        elif command == AddressBook.filter:
            return self.__parse_filter_with_requests()
        elif command == AddressBook.show_users_birthday:
            return self.__parse_show_birthdays_with_requests()
        elif command == AddressBook.get_records:
            return {}
        else:
            return {"error": "Undefined command provided for AddressBook."}

    def __parse_add_with_requests(self) -> dict:
        name = input("Please input a name: ")
        choice = input("Choose a number: 1 - Phone, 2 - Email, 3 - Birthday, 4 - Address ")
        if choice not in self.__information_type:
            return {"error": f"Wrong number: {choice}, please enter from 1 to 4"}

        if choice == "1":
            information = input(f"Input phone number in format 38XXXXXXXXXX: ")
            phone_verification_result, error_message = phone_verify(information)
            if not phone_verification_result:
                return {"error": error_message}
            else:
                return {"name": name, self.__information_type[choice]: phone_verification_result}
        elif choice == "2":
            information = input(f"Input email in format your_mail@your.domain: ")
            email_verification_result, error_message = email_verify(information)
            if not email_verification_result:
                return {"error": error_message}
            else:
                return {"name": name, self.__information_type[choice]: email_verification_result}
        elif choice == "3":
            information = input(f"Input birthday in format YYYY-MM-DD: ")
            birthday_verification_result, error_message = birthday_verify(information)
            if not birthday_verification_result:
                return {"error": error_message}
            else:
                return {"name": name, self.__information_type[choice]: birthday_verification_result}
        elif choice == "4":
            information = input(f"Input address: ")
            return {"name": name, self.__information_type[choice]: information}

    def __parse_change_with_requests(self) -> dict:
        name = input("Please input a name: ")
        choice = input("Choose a number: 1 - Phone, 2 - Email, 3 - Birthday, 4 - Address ")
        if choice not in self.__information_type:
            return {"error": f"Wrong number: {choice}, please enter from 1 to 4"}

        if choice == "1":
            information = input(f"Input phone number in format 38XXXXXXXXXX: ")
            phone_verification_result, error_message = phone_verify(information)
            if not phone_verification_result:
                return {"error": error_message}
            else:
                return {"name": name, self.__information_type[choice]: phone_verification_result}
        elif choice == "2":
            information = input(f"Input email in format your_mail@your.domain: ")
            email_verification_result, error_message = email_verify(information)
            if not email_verification_result:
                return {"error": error_message}
            else:
                return {"name": name, self.__information_type[choice]: email_verification_result}
        elif choice == "3":
            information = input(f"Input birthday in format YYYY-MM-DD: ")
            birthday_verification_result, error_message = birthday_verify(information)
            if not birthday_verification_result:
                return {"error": error_message}
            else:
                return {"name": name, self.__information_type[choice]: birthday_verification_result}
        elif choice == "4":
            information = input(f"Input address: ")
            return {"name": name, self.__information_type[choice]: information}

    @staticmethod
    def __parse_delete_with_requests() -> dict:
        name = input("Please input a name: ")

        return {"name": name}

    @staticmethod
    def __parse_filter_with_requests() -> dict:
        phrase = input("Please input searching phrase: ")

        return {"phrase": phrase}

    @staticmethod
    def __parse_show_birthdays_with_requests() -> dict:
        number_of_days = input("Please input a number of days: ")
        if number_of_days.isnumeric():
            return {"days": int(number_of_days)}

        return {"error": f"User provide invalid number of days in show birthdays method: {number_of_days}"}
