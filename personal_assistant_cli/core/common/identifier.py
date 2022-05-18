from personal_assistant_cli.core.common.verify import phone_verify, email_verify, birthday_verify
import re


class Identifier:
    @staticmethod
    def is_phone(input_data: str) -> bool:
        phone_verification_result, _ = phone_verify(input_data)
        return phone_verification_result is not None

    @staticmethod
    def is_email(input_data: str) -> bool:
        email_verification_result, _ = email_verify(input_data)
        return email_verification_result is not None

    @staticmethod
    def is_birthday(input_data: str) -> bool:
        return bool(re.fullmatch(r'\d{4}-\d{1,2}-\d{1,2}', input_data))

    def identify(self, input_data: str) -> str:
        if self.is_phone(input_data):
            return "phone"

        if self.is_email(input_data):
            return "email"

        if self.is_birthday(input_data):
            return "birthday"

        return "address"
