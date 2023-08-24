from argparse import ArgumentParser, Namespace

from prettytable import PrettyTable

from src.constants import FIELDNAMES, ITEMS_PER_PAGE
from src.utils import create_entry, phonebook, update_field, pagination


parser = ArgumentParser(
    prog='python3 main.py',
    description='Программа CRUD для записей в телефонном справочнике'
)

parser.add_argument('-c', '--create', help='Create entry', action='store', nargs=3)
parser.add_argument('-u', '--update', help='Update entry', action='store', type=int)
parser.add_argument('-d', '--delete', help='Delete entry', action='store', type=int)
parser.add_argument('-s', '--search', help='Search entry', action='store', type=str)
parser.add_argument('-p', '--page', help='Pagination method', action='store', type=int)

args: Namespace = parser.parse_args()

table = PrettyTable()
table.field_names = FIELDNAMES


if __name__ == '__main__':
    if args.create:
        if data := create_entry(args.create):
            phonebook.create(data=data)
            table.add_row(phonebook.get_one(phonebook.get_last_id))
            print(table)

    elif args.update:
        if args.update <= phonebook.get_last_id:
            update = update_field(args.update)
            phonebook.overwrite(update)
            table.add_row(phonebook.get_one(args.update))
            print(table)

    elif args.search:
        search = phonebook.search(args.search)
        table.add_rows(search)
        print(table)

    elif args.delete:
        delete = phonebook.delete(args.delete)
        phonebook.overwrite(delete)

    elif args.page:
        print(pagination(page=args.page, per_page=ITEMS_PER_PAGE, pretty_table=table))
    else:
        print(pagination(per_page=ITEMS_PER_PAGE, pretty_table=table))
