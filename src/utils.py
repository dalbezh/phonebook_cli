import sys
from pathlib import Path
from typing import Union

from prettytable import PrettyTable

from .constants import CSV_FILE, FIELDNAMES
from .core import CSVPhonebook
from .pagination import Pagination
from .validator import CreateField


def load_csv(filename):
    """Проверка и подключение csv файла"""
    csv_file = Path().resolve().joinpath(filename)
    if not csv_file.is_file():
        sys.exit("Problem with CSV_FILE !")
    elif csv_file.stat().st_size >= 10485760:
        sys.exit(f"File {csv_file} larger than 10 MB !")
    else:
        return csv_file


def pagination(per_page: int, page: int = 1, pretty_table: PrettyTable = PrettyTable()) -> Union[PrettyTable, str]:
    """
    Функция для постраничного отображения списка справочника
    pretty_table: объект для отображения результирующего набора
    """
    page_index = page - 1
    pg_result = Pagination(collection=phonebook.get_all, items_per_page=per_page)
    try:
        for row in pg_result.total[page_index]:
            pretty_table.add_row(row)

        print(f"Page number {page} of {pg_result.page_count} pages")
        return pretty_table
    except IndexError:
        return f"Out of range. Only {pg_result.page_count} pages in the phone book"


def create_entry(args_data: list):
    """Функция для создания и и проверка на дубли"""
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
    for field in enumerate(FIELDNAMES[1:]):
        print(field[0] + 1, field[1])
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


phonebook = CSVPhonebook(load_csv(CSV_FILE))
