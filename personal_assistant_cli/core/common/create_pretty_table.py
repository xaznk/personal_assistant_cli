from prettytable import PrettyTable


def create_pretty_table(head, data):
    table = PrettyTable(head)
    for i in data:
        table.add_row(i)

    return str(table)
