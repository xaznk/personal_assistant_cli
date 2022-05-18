import personal_assistant_cli.core.common.db_config as db
from personal_assistant_cli.core.common.create_pretty_table import create_pretty_table


class NoteBook:

    def add(self, arg):
        """
        Creates a new record in the notebook by the specified name.
        :param arg: dict - the dictionary with the text of the note (e.g. {‘text’: ‘Lorem ipsum dolor sit amet...’})
        :return: str - returns a string with a message to the user, whether everything is fine and everything is added, or indicates that there is an error and what exactly.
        """

        value = (arg['text'],)

        try:
            db.cur.execute("""INSERT INTO notes(note)
            VALUES(?);""", value)
            db.conn.commit()
        except db.sqlite3.Error as error:
            return f"Something went wrong, {error}"
        return 'Note saved'

    def change(self, arg):
        """
        Changes the record for the specified name in the notebook.
        :param arg: dict - dictionary with the id of the record and new value (e.g. {‘id’: 26, ‘text’: ‘Excepteur sint occaecat...’})
        :return: str - returns a message to the user, whether everything is fine and changed, or indicates that there is an error and what.
        """
        fields = list(arg.keys())
        update_note = (arg[fields[1]], arg[fields[0]])
        try:
            db.cur.execute(
                """UPDATE notes
                SET note = ?
                WHERE id = ?""", update_note)
            db.conn.commit()
        except db.sqlite3.Error as error:
            return f"Something went wrong, {error}"
        return 'Note edited'

    def delete(self, arg):
        """
        Deletes the record for the specified id in the notebook.
        :param arg: dict - a dictionary containing the id of the record to delete (e.g. {‘id’: 76})
        :return: str - returns a message to the user, whether everything is fine and deleted, or indicates that there is an error and what.
        """
        try:
            db.cur.execute("""DELETE FROM notes
              WHERE id = ?""", (arg['id'],))
            db.conn.commit()
        except db.sqlite3.Error as error:
            return f"Something went wrong, {error}"
        return 'Note deleted'

    def filter_for_tags(self, arg):
        """
        Search and sort notes by tags.
        :param arg: dict - the dictionary with the text of the tag (e.g. {‘tag’: ‘#Lorem ipsum dolor sit amet...’})
        :return: str - returns the string, which contains the entire information line.
        """
        result = ''
        try:
            db.cur.execute(
                """SELECT * FROM notes WHERE tag like ?;""", ('%'+arg['tag']+'%',))
            response = db.cur.fetchall()
            if len(response) > 0:
                table_head = ['Id ',  'Tag', 'Note']
                result = create_pretty_table(table_head, response)
        except db.sqlite3.Error as error:
            return f"Something went wrong, {error}"
        if result == '':
            return 'No matches'
        else:
            return result

    def add_tag_to_note(self, arg):
        """
        Add "tags" to notes, keywords describing the topic and subject of the post.
        :param arg: dict - the dictionary with the text of the tag (e.g. {‘tag’: ‘#Lorem ipsum dolor sit amet...’})
        :return: str - returns the string, which contains the entire information line.
        """
        add_tag = (arg['id'], arg['tag'], arg['id'])
        add_tag_second = (arg['tag'], arg['id'])
        try:
            db.cur.execute(
                """SELECT count(tag) FROM notes WHERE id = ?;""", (arg['id'],))
            all_results = db.cur.fetchall()
            if all_results[0][0] == 1:
                db.cur.execute("""UPDATE notes
                        SET tag = ' ' ||(SELECT tag FROM notes WHERE id = ?) || ' ' || ?
                        WHERE id = ?;""", add_tag)
                db.conn.commit()
            else:
                db.cur.execute(
                    """UPDATE notes 
                    SET tag = ? 
                    WHERE id = ?;""", add_tag_second)
                db.conn.commit()
        except db.sqlite3.Error as error:
            return f"Something went wrong, check your id. {error}"
        return 'Tag added'

    def search(self, arg):
        """
        Search and sort notes by keywords.
        :param arg: dict - the dictionary with the text of the phrase (e.g. {‘phrase’: ‘Lorem ipsum dolor sit amet...’})
        :return: str - returns the string, which contains the entire information line.
        """
        result = ''
        try:
            db.cur.execute(
                """SELECT * FROM notes WHERE note LIKE ? ;""", ('%'+arg['phrase']+'%',))
            response = db.cur.fetchall()
            if len(response) > 0:
                table_head = ['Id ',  'Tag', 'Note']
                result = create_pretty_table(table_head, response)
        except db.sqlite3.Error as error:
            return f"Something went wrong, {error}"
        if result == '':
            return 'No matches'
        else:
            return result

    def get_table(self, arg):
        result = ''
        try:
            db.cur.execute(
                """SELECT * FROM notes ;""")
            response = db.cur.fetchall()

            if len(response) > 0:
                table_head = ['Id ',  'Tag', 'Note']
                result = create_pretty_table(table_head, response)

            return result
        except db.sqlite3.Error as error:
            return f"Something went wrong, {error}"
