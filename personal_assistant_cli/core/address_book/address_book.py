import personal_assistant_cli.core.common.db_config as db
from personal_assistant_cli.core.common.create_pretty_table import create_pretty_table


class AddressBook:
    def add(self, arg):
        """
        Creates a new record in the address book by the specified name.
        :param arg: dict - dictionary, where first the name goes, and then one or more information in any order: address, phone number, email, birthday (e.g. {‘name’: ‘John’, ‘email’: john@gmail.com})
        :return: str - returns a string with a message to the user, whether everything is fine and everything is added, or indicates that there is an error and what exactly.
        """

        fields = list(arg.keys())
        try:
            db.cur.execute(
                """SELECT count(*) FROM contacts WHERE name = ?;""", (arg['name'],))
            all_results = db.cur.fetchall()
            if all_results[0][0] == 1:
                db.cur.execute(
                    f"""SELECT {fields[1]} FROM contacts WHERE name = ?;""", (arg['name'],))
                all_results = db.cur.fetchall()
                if all_results[0][0] == None:
                    AddressBook.change(self, arg)
                    return f'{fields[1]} changed'
                else:
                    return f'For record {arg["name"]}, {fields[1]} is already exist. Please use the next command: "change"'
            else:

                add_record = (arg[fields[0]], arg[fields[1]])
                db.cur.execute(f"""INSERT INTO contacts(name, {fields[1]})
                    VALUES(?, ?);""", add_record)
                db.conn.commit()
                return 'Record added'
        except db.sqlite3.Error as error:
            return f"Something went wrong, {error}"

    def change(self, arg):
        """
        Changes the record for the specified name in the address book.
        :param arg: dict - dictionary, where first the name must be followed, and then new information (address, phone number, email or birthday)
        :return: str - returns a message to the user, whether everything is fine and changed, or indicates that there is an error and what.
        """

        try:
            db.cur.execute(
                """SELECT count(*) FROM contacts WHERE name = ?;""", (arg['name'],))
            all_results = db.cur.fetchall()
            if all_results[0][0] == 0:
                return f'Sorry, AddressBook has no record {arg["name"]}'
            for key in arg.keys():
                if key != "name":
                    update_note = (arg[key], arg["name"])
                    sql = f"""UPDATE contacts
                    SET {key} = ?
                    WHERE name = ?"""
                    field = key
            db.cur.execute(sql, update_note)
            db.conn.commit()
        except db.sqlite3.Error as error:
            return f"Something went wrong, {error}"
        return f'{field} changed'

    def delete(self, arg):
        """
        Deletes the record for the specified name in the address book.
        :param arg: dict - a dictionary containing the name for which you want to delete the record (e.g. {‘name’: ‘John’})
        :return: str - returns a message to the user, whether everything is fine and deleted, or indicates that there is an error and what.
        """

        try:
            db.cur.execute(
                """SELECT count(*) FROM contacts WHERE name = ?;""", (arg['name'],))
            all_results = db.cur.fetchall()
            if all_results[0][0] == 0:
                return f'Sorry, AddressBook has no record {arg["name"]}'
            else:
                db.cur.execute("""DELETE FROM contacts
              WHERE name = ?""", (arg['name'],))
                db.conn.commit()
        except db.sqlite3.Error as error:
            return f"Something went wrong, {error}"
        return f'Record {arg["name"]} deleted'

    def filter(self, arg):
        """
        Searches for information in the address book by coincidence on the entered string.
        :param arg: dict - the dictionary with the value we are searching for (e.g. {‘phrase’: ‘John’})
        :return: str - returns the string, which contains the entire information line (name, email, phone, birthday), in which there was a match. If there are several such lines,
        they are all separated in the string by a sign \n. If there is no match, or an error, it returns a message about it.
        """
        result = ''
        try:
            db.cur.execute(
                """SELECT * FROM contacts WHERE name like ? OR phone like ? OR address like? OR email like ? OR birthday like ?;""",
                ('%' + arg['phrase'] + '%', '%' + arg['phrase'] + '%', '%' + arg['phrase'] + '%', '%' + arg['phrase'] + '%', '%' + arg['phrase'] + '%'))
            response = db.cur.fetchall()
            if len(response) > 0:
                table_head = ["Name", "Phone", "Address", "Email", "Birthday"]
                table_data = []
                for i in response:
                    table_data.append([i[1], i[2], i[3], i[4], i[5]])
                result = create_pretty_table(table_head, table_data)
        except db.sqlite3.Error as error:
            return f"Something went wrong, {error}"
        if result == '':
            return 'No matches'
        else:
            return result

    def show_users_birthday(self, arg):
        """
        Finds users whose birthday is a specified number of days from the current date.
        :param arg: dict - the number of days (type: int) added to the current date (e.g. {‘days’: 36}).
        :return:  returns a string with all names of users and their birthdays, for example "name: yyyy-mm-dd, \n name: yyyy-mm-dd, \n ...".
        """
        result = ''
        val = arg['days'] + 1
        try:
            db.cur.execute(
                f"""SELECT name, birthday FROM contacts WHERE strftime('%j', birthday) BETWEEN strftime('%j', date('now', '+1 day')) AND strftime('%j', (date('now','+{val} day')));""")
            response = db.cur.fetchall()
            if len(response) > 0:
                table_head = ["Name", "Birthday"]
                table_data = []
                for i in response:
                    table_data.append([i[0], i[1]])
                result = create_pretty_table(table_head, table_data)

        except db.sqlite3.Error as error:
            return f"Something went wrong, {error}"
        if result == '':
            return 'No birthdays in this day'
        else:
            return result

    def get_records(self, arg):
        result = ''
        try:
            db.cur.execute(
                f"""SELECT * FROM contacts ;""")
            response = db.cur.fetchall()
            if len(response) > 0:

                table_head = ["Name", "Phone", "Address", "Email", "Birthday"]
                table_data = []
                for i in response:
                    table_data.append([i[1], i[2], i[3], i[4], i[5]])
                result = create_pretty_table(table_head, table_data)

        except db.sqlite3.Error as error:
            return f"Something went wrong, {error}"
        if result == '':
            return 'Address book is empty yet'
        else:
            return result
