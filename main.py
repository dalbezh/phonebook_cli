import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Union

from prettytable import PrettyTable

from src.core import CSVPhonebook, FIELDNAMES
from src.pagination import Pagination
from src.validator import CreateField

CSV_FILE = Path().resolve().joinpath('phonebook.csv')
ITEMS_PER_PAGE = 5

# Проверка csv:
if not CSV_FILE.is_file():
    sys.exit("Problem with CSV_FILE !")
if CSV_FILE.stat().st_size >= 10485760:
    sys.exit(f"File {CSV_FILE} larger than 10 MB !")

parser = ArgumentParser(
    prog='Phonebook CLI',
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
phonebook = CSVPhonebook(CSV_FILE)


def pagination(per_page: int = ITEMS_PER_PAGE, page: int = 0) -> Union[PrettyTable, str]:
    """Функция для постраничного отображения списка справочника"""
    page_index = page - 1
    pg_result = Pagination(collection=phonebook.get_all, items_per_page=per_page)
    try:
        for row in pg_result.total[page_index]:
            table.add_row(row)

        print(f"Page number {page} of {pg_result.page_count} pages")
        return table
    except IndexError:
        return f"Out of range. Only {pg_result.page_count} pages in the phone book"


def create_entry(args_data: list):
    try:
        entry = CreateField(
            id=phonebook.get_last_id + 1,
            last_name=args_data[0],
            first_name=args_data[1],
            personal_phone=args_data[2]
        )
        for row in phonebook.get_all:
            if entry.personal_phone in row:
                print(f"A row with this phone number already exists: id {row[0]}")
                raise ValueError
    except ValueError:
        print("Phone number error")
        return []
    return entry


def update_field(id: int):
    """Функция для обновления данных"""
    for x in enumerate(FIELDNAMES[1:]):
        print(x[0] + 1, x[1])
    try:
        field_number = input("Input a number from 1 to 6 for the field you want to change: ")
        if int(field_number) in range(1, 7):
            fieldname = FIELDNAMES[int(field_number)]
            print(fieldname)
            new_data = input("Now, input new field value: ")
            if int(field_number) not in range(6, 7):
                update_data = phonebook.update(id=id, fieldname=fieldname, data=new_data.title())
            else:
                raise ValueError
            return update_data
        else:
            print("number from 1 to 6!")
    except ValueError:
        return ''


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
        print(pagination(page=args.page))
    else:
        print(pagination(page=1))
